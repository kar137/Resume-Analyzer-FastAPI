from sqlalchemy import Column, String, Integer, JSON
from app.core.config import settings
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ResumeAnalyses(Base):
    __tablename__ = "Resume_analysis"
    id = Column(String, primary_key=True, index= True )
    original_filename = Column(String)
    status = Column(String, default="pending")  # "processing", "completed", "failed"
    word_count = Column(Integer)
    skills = Column(JSON)  # Stores list of skills as JSON
    raw_content = Column(String)  # Stores extracted text
    analysis_result = Column(JSON)

    def to_dict(self):
        content = getattr(self, "raw_content", None)
        if isinstance(content, str):
            trimmed = content[:500] + "..." if len(content) > 500 else content
        else:
            trimmed = ""
        return {
            "id": self.id,
            "original_filename": self.original_filename,
            "status": self.status,
            "word_count": self.word_count,
            "skills": self.skills,
            "content": trimmed,
            "analysis": self.analysis_result
        }