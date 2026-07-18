import subprocess
import json
import os
from typing import List, Dict, Any

class StaticAnalyzer:
    """Base class for static analysis runners."""
    def __init__(self, workspace_dir: str):
        self.workspace_dir = workspace_dir

    def run(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

class RuffAnalyzer(StaticAnalyzer):
    def run(self) -> List[Dict[str, Any]]:
        # Ruff outputs JSON format easily
        try:
            result = subprocess.run(
                ["ruff", "check", self.workspace_dir, "--output-format=json"],
                capture_output=True,
                text=True
            )
            if not result.stdout:
                return []
            
            issues = json.loads(result.stdout)
            formatted_issues = []
            for issue in issues:
                formatted_issues.append({
                    "tool": "Ruff",
                    "severity": "High" if issue.get("severity") == "error" else "Medium",
                    "message": issue.get("message"),
                    "file": issue.get("filename"),
                    "line": issue.get("location", {}).get("row")
                })
            return formatted_issues
        except (subprocess.SubprocessError, FileNotFoundError, json.JSONDecodeError):
            # Fallback or mock if ruff is not installed
            return []

class ESLintAnalyzer(StaticAnalyzer):
    def run(self) -> List[Dict[str, Any]]:
        try:
            result = subprocess.run(
                ["npx", "eslint", self.workspace_dir, "--format=json"],
                capture_output=True,
                text=True
            )
            if not result.stdout:
                return []
            
            issues = json.loads(result.stdout)
            formatted_issues = []
            for file_issue in issues:
                for msg in file_issue.get("messages", []):
                    formatted_issues.append({
                        "tool": "ESLint",
                        "severity": "High" if msg.get("severity") == 2 else "Medium",
                        "message": msg.get("message"),
                        "file": file_issue.get("filePath"),
                        "line": msg.get("line")
                    })
            return formatted_issues
        except (subprocess.SubprocessError, FileNotFoundError, json.JSONDecodeError):
            return []

class CppCheckAnalyzer(StaticAnalyzer):
    def run(self) -> List[Dict[str, Any]]:
        # Mocking for C++ as cppcheck might not be installed
        return []

class AnalyzerFactory:
    @staticmethod
    def get_analyzers(language: str, workspace_dir: str) -> List[StaticAnalyzer]:
        lang_map = {
            "python": [RuffAnalyzer(workspace_dir)],
            "javascript": [ESLintAnalyzer(workspace_dir)],
            "typescript": [ESLintAnalyzer(workspace_dir)],
            "c++": [CppCheckAnalyzer(workspace_dir)],
            "cpp": [CppCheckAnalyzer(workspace_dir)]
        }
        return lang_map.get(language.lower(), [])

def run_static_analysis(language: str, workspace_dir: str) -> List[Dict[str, Any]]:
    """Runs all applicable static analyzers for a given language."""
    analyzers = AnalyzerFactory.get_analyzers(language, workspace_dir)
    all_issues = []
    for analyzer in analyzers:
        all_issues.extend(analyzer.run())
    return all_issues
