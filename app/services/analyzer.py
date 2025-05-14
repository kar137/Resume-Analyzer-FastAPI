from app.services.parser import FileParser

from app.services.parser import FileParser

def analyze_resume(file_contents: bytes, filename: str) -> dict:
    """Improved resume analyzer with proper file parsing"""
    try:
        # Extract text from file
        text = FileParser.parse_file(file_contents, filename)

        word_count = len(text.split())
        
        skills = []
        if "python" in text.lower():
            skills.append("Python")
        if "fastapi" in text.lower():
            skills.append("FastAPI")
        if "sql" in text.lower():
            skills.append("SQL")
        
        return {
            "filename": filename,
            "word_count": word_count,
            "skills": skills,
            "content": text[:500] + "..." if len(text) > 500 else text  # Sample content
        }
    except ValueError as e:
        raise  # Re-raise the error to be handled by the endpoint