from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import hashlib

from core.database import get_db
from core.security import get_current_user
from core.security import get_current_user
from models.user import User
from models.file import UploadedFile
from models.review import Review
from models.issue import Issue
from services.parser import DiffParser
from services.pipeline import ReviewPipeline
from fastapi import BackgroundTasks
from sqlalchemy import func

router = APIRouter()

@router.post("/upload")
async def upload_code(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(None),
    pasted_code: str = Form(None),
    github_url: str = Form(None),
    language: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint for uploading code to be reviewed.
    Handles file upload, pasted code, or a GitHub PR URL.
    """
    content = ""
    file_type = "unknown"
    filename = "unknown"

    if file:
        content = (await file.read()).decode("utf-8")
        file_type = "file"
        filename = file.filename
    elif pasted_code:
        content = pasted_code
        file_type = "paste"
        filename = "pasted_code.diff"
    elif github_url:
        # We would fetch the diff from GitHub API here
        content = "mock github diff content"
        file_type = "github_pr"
        filename = github_url
    else:
        raise HTTPException(status_code=400, detail="No code provided")

    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    
    # Create the base Review object
    review = Review(
        user_id=1,  # Hardcoding for testing since we aren't passing the real JWT easily in the frontend stub
        overall_score=0.0,
        status="Processing"
    )
    # If current_user was guaranteed, we'd use current_user.id
    # review.user_id = current_user.id
    
    db.add(review)
    db.commit()
    db.refresh(review)

    uploaded = UploadedFile(
        review_id=review.id,
        filename=filename,
        file_type=file_type,
        content_hash=content_hash
    )
    db.add(uploaded)
    db.commit()
    
    # Execute the pipeline in the background
    files_dict = DiffParser.extract_files_from_diff(content)
    
    def run_pipeline(r_id, lang, f_dict):
        # We need a new session for the background task
        from core.database import SessionLocal
        bg_db = SessionLocal()
        try:
            pipeline = ReviewPipeline(bg_db, r_id)
            pipeline.execute(lang, f_dict)
            
            # Update status
            bg_review = bg_db.query(Review).filter(Review.id == r_id).first()
            if bg_review:
                bg_review.status = "Completed"
                bg_db.commit()
        except Exception as e:
            bg_review = bg_db.query(Review).filter(Review.id == r_id).first()
            if bg_review:
                bg_review.status = "Failed"
                bg_db.commit()
        finally:
            bg_db.close()

    background_tasks.add_task(run_pipeline, review.id, language, files_dict)
    
    return {
        "status": "success", 
        "message": "Code uploaded and review started", 
        "review_id": review.id,
        "hash": content_hash,
        "language": language
    }

@router.get("/history")
def get_review_history(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    """Fetch recent reviews for the user."""
    # Hardcoded user_id=1 for testing
    reviews = db.query(Review).filter(Review.user_id == 1).order_by(Review.created_at.desc()).limit(20).all()
    
    result = []
    for r in reviews:
        # Get filename if available
        file_obj = db.query(UploadedFile).filter(UploadedFile.review_id == r.id).first()
        filename = file_obj.filename if file_obj else "Unknown"
        
        result.append({
            "id": r.id,
            "filename": filename,
            "status": r.status,
            "score": r.overall_score,
            "created_at": r.created_at,
            "language": r.language
        })
    return result

@router.get("/statistics")
def get_statistics(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    """Fetch aggregated statistics for the user."""
    # Hardcoded user_id=1 for testing
    total_reviews = db.query(Review).filter(Review.user_id == 1).count()
    
    avg_score = db.query(func.avg(Review.overall_score)).filter(Review.user_id == 1).scalar()
    avg_score = round(avg_score, 1) if avg_score else 0.0
    
    critical_issues = db.query(Issue).join(Review).filter(Review.user_id == 1, Issue.severity == "Critical").count()
    
    ready_count = db.query(Review).filter(Review.user_id == 1, Review.merge_ready == True).count()
    merge_ready_pct = round((ready_count / total_reviews * 100)) if total_reviews > 0 else 0
    
    return {
        "total_reviews": total_reviews,
        "average_score": avg_score,
        "critical_issues": critical_issues,
        "merge_ready_percentage": merge_ready_pct
    }
