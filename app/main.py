from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from app.models.resume import ResumeAnalysis
from app.services.analyzer import analyze_resume
import uuid
import json
import os
from pathlib import Path
from typing import Dict, Any, Union

app = FastAPI(title="Resume Analyzer API")

@app.get("/")
def read_root():
    return {"message": "Resume Analyzer API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

RESULTS_DIR = Path("Results")
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_FILE_TYPES = {'.pdf', '.docx'}

RESULTS_DIR.mkdir(exist_ok=True)

@app.post("/upload", response_model=None)
async def upload_resume(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...)
):
    """
    Upload a resume for analysis with improved error handling and validation.
    """
    analysis_id = str(uuid.uuid4())

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
        
        # Add analysis metadata
        analysis.update({
            "id": analysis_id,
            "original_filename": file.filename,
            "status": "completed"
        })

        # Save in background
        background_tasks.add_task(
            save_analysis_to_file,
            analysis=analysis,
            analysis_id=analysis_id
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
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to process resume",
                "details": str(e),
                "id": analysis_id,
                "status": "failed"
            }
        )

    
def save_analysis_to_file(analysis: Dict[str, Any], analysis_id: str) -> None:
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
def get_result(analysis_id: str):
    """
    Retrieve analysis results by ID.
    
    Parameters:
    - analysis_id: The analysis ID to retrieve
    
    Returns:
    - The analysis results or error message
    """
    try:
        # Validate analysis_id format
        try:
            uuid.UUID(analysis_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid analysis ID format"
            )

        filepath = RESULTS_DIR/ f"{analysis_id}.json"

        if not filepath.exists():
            return JSONResponse(
                status_code=404,
                content= {"error": "Analysis not found."}
                
            )
        with open(filepath, "r") as f:
            result = json.load(f)
        
        return {
                **result,
                "status": "completed"
            }

    except HTTPException:
        raise
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve analysis: {str(e)}"
        )