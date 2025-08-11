from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel

import io

from .model_loader import classify_image_bytes, detect_weapons_in_bytes
from .word_detector.words_detector import ahocorasick, automaton,find_words_aho
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Obscenity Detector API is live"}

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
        

class TextInput(BaseModel):
    text: str

@app.post("/detect-obscene/")
def detect_obscene(input_data: TextInput):
    try:
        matches = find_words_aho(input_data.text, automaton)
        return {
            "input": input_data.text,
            "matches_found": bool(matches),
            "matched_words": matches
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))