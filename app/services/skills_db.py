TECH_SKILLS = {
    "python": ["python", "django", "flask", "fastapi"],
    "javascript": ["javascript", "typescript", "node.js", "react"],
    "database": ["sql", "mysql", "postgresql", "mongodb"],
    "devops": ["docker", "kubernetes", "aws", "azure"]
}

def detect_skills(text: str) -> list[str]:
    """Detect skills from text using simple keyword matching"""
    detected = set()
    text_lower = text.lower()
    
    for category, keywords in TECH_SKILLS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected.add(keyword)
                break  # Only need one match per category
    
    return sorted(list(detected))