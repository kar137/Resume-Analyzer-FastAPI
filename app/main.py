from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from app.models.resume import ResumeAnalysis
from app.services.analyzer import analyze_resume
import uuid
import json
from pathlib import Path

app = FastAPI(title="Resume Analyzer API")

@app.get("/")
def read_root():
    return {"message": "Resume Analyzer API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

RESULTS_DIR = Path("Results")
RESULTS_DIR.mkdir(exist_ok=True)

def save_analysis_to_file(analysis: dict):
    """save analysis result to a file"""
    analysis_id = str(uuid.uuid4())
    filepath = RESULTS_DIR/ f"{analysis_id}.json"
    with open(filepath, "w") as f:
        json.dump(analysis, f)
    return analysis_id

@app.post("/upload")
async def upload_resume(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Endpoint to upload resume files"""
    try:
        contents = await file.read()
        analysis = analyze_resume(contents, file.filename)

        analysis_id = background_tasks.add_task(
            save_analysis_to_file,
            analysis
        )
        return {"message": "Analysis started", "id": analysis_id}
    
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )