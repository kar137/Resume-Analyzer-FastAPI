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

@app.post("/upload")
async def upload_resume(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Endpoint to upload resume files"""
    analysis_id = str(uuid.uuid4())
    try:
        contents = await file.read()
        analysis = analyze_resume(contents, file.filename)

        analysis_id = background_tasks.add_task(
            save_analysis_to_file,
            analysis,
            analysis_id
        )
        return {"message": "Analysis started", "id": analysis_id}
    
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
    
def save_analysis_to_file(analysis: dict, analysis_id: str):
    """save analysis result to a file"""
    filepath = RESULTS_DIR/ f"{analysis_id}.json"
    with open(filepath, "w") as f:
        json.dump(analysis, f)
    return analysis_id

    
@app.get("/result/{analysis_id}")
def get_result(analysis_id: str):
    """Get analysis result by id"""
    filepath = RESULTS_DIR/ f"{analysis_id}.json"

    if not filepath.exists():
        return JSONResponse(
            content= {"error": "Analysis not found."},
            status_code=404
        )
    with open(filepath, "r") as f:
        result = json.load(f)
    
    return result