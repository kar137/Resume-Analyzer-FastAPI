from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from app.models.resume import ResumeAnalysis
from app.services.analyzer import analyze_resume

app = FastAPI(title="Resume Analyzer API")

@app.get("/")
def read_root():
    return {"message": "Resume Analyzer API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/upload", response_model=ResumeAnalysis)
async def upload_resume(file: UploadFile = File(...)):
    """Endpoint to upload resume files"""
    try:
        contents = await file.read()
        analysis = analyze_resume(contents, file.filename)
        return analysis
    
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )