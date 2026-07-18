from sqlalchemy.orm import Session
from models.review import Review
from models.issue import Issue
from services.parser import DiffParser
from services.analyzer import run_static_analysis
import os

class ReviewPipeline:
    def __init__(self, db: Session, review_id: int):
        self.db = db
        self.review_id = review_id

    def execute(self, language: str, files_dict: dict):
        """
        Executes the full review pipeline.
        1. Setup workspace
        2. Run Static Analysis
        3. Build Prompt (Milestone 7)
        4. Call Groq (Milestone 7)
        5. Store Results (Milestone 7)
        """
        review = self.db.query(Review).filter(Review.id == self.review_id).first()
        if not review:
            raise Exception("Review not found")

        review.language = language
        self.db.commit()

        # Step 1: Setup workspace
        workspace_dir = DiffParser.create_temp_workspace(files_dict)
        
        try:
            # Step 2: Run static analysis
            static_issues = run_static_analysis(language, workspace_dir)
            
            # TODO: Step 3-5 will be implemented in Milestones 6 & 7
            # For now, we just log the static issues to the review if any.
            
            for s_issue in static_issues:
                issue = Issue(
                    review_id=self.review_id,
                    severity=s_issue.get("severity", "Medium"),
                    category="Static Analysis",
                    title=f"{s_issue.get('tool')} Alert",
                    description=s_issue.get("message", ""),
                    file_path=s_issue.get("file", ""),
                    line_number=s_issue.get("line")
                )
                self.db.add(issue)
            
            review.overall_score = 9.0  # Mock score for now
            self.db.commit()

        finally:
            DiffParser.cleanup_workspace(workspace_dir)

        return {"status": "completed", "static_issues_found": len(static_issues)}
