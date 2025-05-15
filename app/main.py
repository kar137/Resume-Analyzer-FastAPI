from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.models.resume import ResumeAnalysis
from app.models.db_models import ResumeAnalyses
from app.services.analyzer import analyze_resume
import uuid
import json
import os
from pathlib import Path
from typing import Dict, Any, Union
from app.db.database import init_db
from sqlalchemy.orm import Session
from app.db.database import SessionLocal

app = FastAPI(title="Resume Analyzer API")

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Resume Analyzer API is running"}


RESULTS_DIR = Path("Results")
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_FILE_TYPES = {'.pdf', '.docx'}

RESULTS_DIR.mkdir(exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload", response_model=None)
async def upload_resume(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a resume for analysis with improved error handling and validation.
    """
    analysis_id = str(uuid.uuid4())

    db_record = ResumeAnalyses(
        id=analysis_id,
        status="processing",
        original_filename=file.filename
    )
    db.add(db_record)
    db.commit()

    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Uploaded file has no filename.")

        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed types: {', '.join(ALLOWED_FILE_TYPES)}"
            )
        # Check file size
        file.file.seek(0, 2)
        file_size = file.file.tell()
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size is {MAX_FILE_SIZE/1024/1024}MB"
            )
        file.file.seek(0)  # Reset file pointer after checking size

        # Read and analyze file
        contents = await file.read()
        analysis = analyze_resume(contents, file.filename)
        db_record = db.query(ResumeAnalyses).filter(ResumeAnalyses.id == analysis_id).first()
        if db_record:
            db_record.status = analysis.get("status", "completed")
            db_record.word_count = analysis.get("word_count")
            db_record.skills = analysis.get("skills", [])
            db_record.raw_content = analysis.get("raw_content", "")
            db_record.analysis_result = analysis
            db.commit()
        
        # Add analysis metadata
        analysis.update({
            "id": analysis_id,
            "original_filename": file.filename,
            "status": "completed"
        })

        # Save in background
        background_tasks.add_task(
            save_analysis_to_file,
            analysis,
            analysis_id,
            db
        )

        return {
            "message": "Analysis started successfully",
            "id": analysis_id,
            "status": "processing",
            "filename": file.filename
        }

    except HTTPException:
        # Re-raise HTTP exceptions (for our validation errors)
        raise
        
    except Exception as e:
        # Log the error (you should add proper logging here)
        print(f"Error processing file: {str(e)}")
        db_record.status = "failed"
        db_record.analysis_result = {"error": str(e)}
        db.commit()
        raise HTTPException(500, detail=str(e))

    
def save_analysis_to_file(analysis: Dict[str, Any], analysis_id: str, db: Session) -> None:
    """
    Save analysis result to a JSON file.
    
    Parameters:
    - analysis: The analysis results dictionary
    - analysis_id: The unique ID for this analysis
    
    Returns:
    - None (just saves the file)
    """
    try:
        filepath = RESULTS_DIR / f"{analysis_id}.json"
        
        # Create temp file first to ensure atomic write
        temp_filepath = filepath.with_suffix('.tmp')
        
        with open(temp_filepath, "w") as f:
            json.dump(analysis, f, indent=2)
            
        # Rename temp file to final filename
        os.replace(temp_filepath, filepath)
        
    except Exception as e:
        print(f"Failed to save analysis {analysis_id}: {str(e)}")
        raise

    
@app.get("/result/{analysis_id}", response_model=None)
def get_result(analysis_id: str, db: Session = Depends(get_db)):
    """
    Retrieve analysis results by ID.
    
    Parameters:
    - analysis_id: The analysis ID to retrieve
    
    Returns:
    - The analysis results or error message
    """
    db_record = db.query(ResumeAnalyses).filter(ResumeAnalyses.id == analysis_id).first()
    
    if db_record.status != "completed":
        return {"status": db_record.status, "id": analysis_id}
    
    if not db_record:
        raise HTTPException(404, detail="Analysis not found")
    
    
    return db_record.to_dict()