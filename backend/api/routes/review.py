from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import hashlib

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.file import UploadedFile
from services.parser import DiffParser

router = APIRouter()

@router.post("/upload")
async def upload_code(
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

    uploaded = UploadedFile(
        review_id=0, # This would be tied to a newly created Review, which we will handle in the pipeline
        filename=filename,
        file_type=file_type,
        content_hash=content_hash
    )
    
    # Normally we wouldn't commit the file here without the review,
    # but for now we just return success to move to the next phase.
    
    return {
        "status": "success", 
        "message": "Code uploaded successfully", 
        "hash": content_hash,
        "language": language
    }
