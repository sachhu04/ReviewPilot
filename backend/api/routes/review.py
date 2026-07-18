from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import hashlib

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.file import UploadedFile
from models.review import Review
from services.parser import DiffParser
from services.pipeline import ReviewPipeline
from fastapi import BackgroundTasks

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
