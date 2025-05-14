from pydantic import BaseModel

class ResumeAnalysis(BaseModel):
    filename: str
    word_count: int
    skills: list[str] = []
