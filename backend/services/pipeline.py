from sqlalchemy.orm import Session
from models.review import Review
from models.issue import Issue
from services.parser import DiffParser
from services.analyzer import run_static_analysis
from prompts.builder import PromptBuilder
from providers.groq_provider import GroqProvider
import os
import json

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
            
            # Generate Prompt
            system_msg = PromptBuilder.build_system_message()
            
            # Reconstruct code content from files_dict for the prompt
            code_content = "\n".join([f"--- {filename} ---\n{content}" for filename, content in files_dict.items()])
            user_msg = PromptBuilder.build_user_prompt(language, code_content, static_issues)
            
            # Call Groq AI Provider
            provider = GroqProvider()
            ai_response = provider.generate_review(prompt=user_msg, system_message=system_msg)
            
            # Store Results
            review.overall_score = ai_response.get("overall_score", 0.0)
            review.merge_ready = ai_response.get("merge_ready", False)
            review.confidence = ai_response.get("confidence", 0)
            review.summary = ai_response.get("summary", "")
            
            # Handle Issues from AI
            ai_issues = ai_response.get("issues", [])
            for ai_issue in ai_issues:
                issue = Issue(
                    review_id=self.review_id,
                    severity=ai_issue.get("severity", "Medium"),
                    category=ai_issue.get("category", "General"),
                    title=ai_issue.get("title", "Issue"),
                    description=ai_issue.get("description", ""),
                    evidence=ai_issue.get("evidence", ""),
                    recommendation=ai_issue.get("recommendation", ""),
                    confidence=ai_issue.get("confidence", 0),
                    file_path=ai_issue.get("file", ""),
                    line_number=ai_issue.get("line")
                )
                self.db.add(issue)
            
            self.db.commit()

        finally:
            DiffParser.cleanup_workspace(workspace_dir)

        return {"status": "completed", "static_issues_found": len(static_issues), "ai_issues_found": len(ai_issues)}
