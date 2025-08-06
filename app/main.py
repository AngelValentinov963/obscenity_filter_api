from fastapi import FastAPI, File, UploadFile, HTTPException
import io

from .model_loader import classify_image_bytes, detect_weapons_in_bytes

app = FastAPI()

@app.get("/")
def root():
    return {"message": "NSFW Detector API is live"}

@app.post("/nsfw_detector/")
async def nsfw(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('png', 'jpg', 'jpeg')):
        raise HTTPException(status_code=400, detail="Only image files are supported")

    try:
        contents = await file.read()
        result = classify_image_bytes(contents)
        return {"predictions": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect-guns/")
async def detect_guns(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('png', 'jpg', 'jpeg')):
        raise HTTPException(status_code=400, detail="Only image files are supported")
    
    contents = await file.read()
    try:
        result = detect_weapons_in_bytes(contents)
        return {"gun_detections": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))