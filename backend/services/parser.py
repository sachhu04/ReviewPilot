import tempfile
import os
import shutil

class DiffParser:
    @staticmethod
    def extract_files_from_diff(diff_content: str) -> dict:
        """
        Parses a raw diff and extracts the files.
        Returns a dict mapping filename to its content.
        This is a rudimentary mock for now.
        """
        # In a real scenario, this would use a library like `unidiff`
        # and if the user uploads a diff against a base, we can't fully 
        # reconstruct the file without the base code. We might only have the diff.
        # But for static analysis to work properly, we need full files or we run
        # analysis on the diff lines only if the tool supports it.
        
        return {"example.py": "def test():\n    pass\n"}
    
    @staticmethod
    def create_temp_workspace(files_dict: dict) -> str:
        """
        Creates a temporary directory with the files for static analysis.
        Returns the path to the temp directory.
        """
        temp_dir = tempfile.mkdtemp(prefix="reviewpilot_")
        for filename, content in files_dict.items():
            file_path = os.path.join(temp_dir, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(content)
        return temp_dir

    @staticmethod
    def cleanup_workspace(temp_dir: str):
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
