from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI(title="Resume Analyzer API")

@app.get("/")
def read_root():
    return {"message": "Resume Analyzer API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """Endpoint to upload resume files"""
            
    try:
        contents = await file.read()
        return JSONResponse(
            content={
                "filename": file.filename,
                "size": len(contents),
                "message": "File uploaded successfully"
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )