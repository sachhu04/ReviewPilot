import json
from typing import List, Dict, Any

class PromptBuilder:
    @staticmethod
    def build_system_message() -> str:
        return """You are a Staff Software Engineer, AI Systems Architect, and Product Designer. 
Your task is to review the provided code changes (diff or raw code) like an experienced Staff Software Engineer.
Do not just explain the code. Identify bugs, performance issues, security vulnerabilities, scalability concerns, maintainability problems, code smells, and architectural issues.
You MUST output your review strictly as a JSON object that matches the following expected structure.
The AI should never invent issues. Every issue must contain evidence.

EXPECTED JSON FORMAT:
{
  "overall_score": 8.9,
  "merge_ready": false,
  "confidence": 95,
  "summary": "...",
  "strengths": ["...", "..."],
  "improvements": ["...", "..."],
  "issues": [
    {
      "severity": "High", // Must be one of: Critical, High, Medium, Low
      "category": "Security", // e.g., Security, Performance, Logic, Maintainability, Architecture
      "title": "...",
      "description": "...",
      "evidence": "...", // The exact line(s) of code causing the issue
      "recommendation": "...",
      "confidence": 94,
      "file": "main.cpp",
      "line": 82 // or null if not applicable
    }
  ]
}
"""

    @staticmethod
    def build_user_prompt(language: str, code_content: str, static_analysis_issues: List[Dict[str, Any]]) -> str:
        prompt = f"Language: {language}\n\n"
        
        if static_analysis_issues:
            prompt += "The following issues were detected by static analysis tools. Consider them in your review and elaborate if necessary:\n"
            prompt += json.dumps(static_analysis_issues, indent=2)
            prompt += "\n\n"
        
        prompt += "Code to Review:\n"
        prompt += "```\n"
        prompt += code_content
        prompt += "\n```\n"
        
        return prompt
