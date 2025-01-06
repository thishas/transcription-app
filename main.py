from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="Transcription App")

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Endpoint to transcribe uploaded audio files.
    To be implemented with audio processing and transcription logic.
    """
    return JSONResponse(
        content={"message": "Transcription endpoint ready for implementation"}
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the Transcription App API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
