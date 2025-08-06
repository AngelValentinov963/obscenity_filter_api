import os
import numpy as np
import io
from PIL import Image
from ultralytics import YOLO
from nsfw_detector import predict

# Get absolute path to the project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Absolute model path
NSFW_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'nsfw_model','nsfw_mobilenet_v2_140_224', 'mobilenet_v2_140_224')

# Load model once
nsfw_model = predict.load_model(NSFW_MODEL_PATH)

def classify_image_bytes(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image = image.resize((224, 224))
    image_array = np.array(image).astype(np.float32) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    
    predictions = nsfw_model.predict(image_array)[0]
    
    return {
        "drawings": float(predictions[0]),
        "hentai": float(predictions[1]),
        "neutral": float(predictions[2]),
        "porn": float(predictions[3]),
        "sexy": float(predictions[4])
    }


# Load YOLO gun detection model
GUN_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'gun_model', 'Weapon-Detection-YOLO','best (3).pt')


# Load your pretrained model once (do this globally)

gun_model = YOLO(GUN_MODEL_PATH)

def detect_weapons_in_bytes(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    results = gun_model.predict(image, conf=0.25,verbose=False)

    detections = []
    for result in results:
        for box in result.boxes.data.tolist():
            x1, y1, x2, y2, conf, cls = box
            detections.append({
                "label":'Weapon',
                "confidence": float(conf)
                #"bbox": [float(x1), float(y1), float(x2), float(y2)]
            })

    return {"detections": detections}

