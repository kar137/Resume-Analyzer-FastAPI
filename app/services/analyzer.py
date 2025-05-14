def analyze_resume(filecontents:bytes, filename:str) -> dict:
    """Basic resume analyzer"""
    text = filecontents.decode('utf-8')  # text extraction from document
    word_count = len(text.split())
    skills = ["Python", "FastAPI"] if "python" in text.lower() else []

    return {
        "filename": filename,
        "word_count": word_count,
        "skills": skills
    }