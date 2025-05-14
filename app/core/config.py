# app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Resume Analyzer"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str                # Loaded from .env
    REDIS_URL: str = "redis://localhost:6379/0"
    DEBUG: bool = False              # Default False if not in .env

    class Config:
        env_file = "env"           # File from which to load variables

settings = Settings()