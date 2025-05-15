TECH_SKILLS = ["python", "django", "flask", "fastapi", "javascript", "typescript", "node.js", "react", "sql", "mysql", "postgresql", "mongodb", "docker", "kubernetes", "aws", "azure"]


def detect_skills(text: str) -> list[str]:
    """Detect skills from text using simple keyword matching"""
    detected = set()
    text_lower = text.lower()
    
    for keyword in TECH_SKILLS:
        if keyword in text_lower:
            detected.add(keyword)
    
    return sorted(list(detected))