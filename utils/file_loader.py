import json
import PyPDF2
import os

SUPPORTED_FORMATS = ["pdf", "json", "txt", "eml"]

def detect_format(extension: str, content: str) -> str:
    """
    Detects document format based on file extension and content.
    """
    ext = extension.lower()
    
    if ext == "pdf":
        return "PDF"
    elif ext == "json":
        return "JSON"
    elif ext in ["txt", "eml"]:
        return "Email"
    else:
        # Fallback: check if it's JSON
        try:
            json.loads(content)
            return "JSON"
        except:
            return "Email"

def load_file(file_path: str) -> str:
    """
    Reads content from PDF, JSON, TXT, or EML files.
    
    Args:
        file_path (str): Path to the input file.

    Returns:
        str: Extracted plain text content.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    ext = file_path.split(".")[-1].lower()

    if ext == "pdf":
        try:
            reader = PyPDF2.PdfReader(file_path)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            raise RuntimeError(f"Error reading PDF: {e}")
    
    elif ext in ["txt", "eml", "json"]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"Error reading {ext.upper()} file: {e}")
    
    else:
        raise ValueError(f"Unsupported file format: .{ext}")
