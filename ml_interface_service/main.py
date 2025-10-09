from fastapi import FastAPI
from pydantic import BaseModel
import cv2
import numpy as np
import base64
from datetime import datetime

from utils.mediapipe_helpers import extract_landmarks
from utils.safety_checks import validate_landmarks
from models.eye_status import check_eye_status
from models.yawning import check_yawn
from models.head_tilt import check_head_tilt
from models.phone_usage import check_phone_usage

app = FastAPI()

class FrameData(BaseModel):
    frame: str

@app.post("/predict")
async def predict(data: FrameData):
    try:
        # ----- Decode Base64 frame -----
        encoded = data.frame.split(",")[1] if "," in data.frame else data.frame
        img_bytes = base64.b64decode(encoded)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # ----- Extract landmarks -----
        landmarks = extract_landmarks(frame)
        if not landmarks:
            log_msg = f"[{datetime.now().strftime('%H:%M:%S')}] ❌ No face detected"
            print(log_msg)
            return {"activity": "no_face_detected"}

        required_indices = list(range(0, 468))  # all Mediapipe landmarks
        if not validate_landmarks(landmarks, required_indices):
            log_msg = f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ Incomplete landmarks"
            print(log_msg)
            return {"activity": "incomplete_landmarks"}

        # ----- Run all detectors -----
        eye_status, EAR = check_eye_status(landmarks)
        yawn_status, yawn_ratio = check_yawn(landmarks)
        head_tilted, tilt_angle = check_head_tilt(landmarks)
        phone_used = check_phone_usage(landmarks)

        # ----- Prepare activity summary -----
        activity_summary = {
            "eye_status": eye_status,
            "EAR": round(EAR, 2),
            "yawning": yawn_status,
            "yawn_ratio": round(yawn_ratio, 2),
            "head_tilted": head_tilted,
            "tilt_angle": round(tilt_angle, 1),
            "phone_used": phone_used
        }

        # ----- Print concise log on console -----
        log_msg = (
            f"[{datetime.now().strftime('%H:%M:%S')}] "
            f"Eye: {eye_status}, Yawn: {yawn_status}, "
            f"Head Tilted: {head_tilted}, Phone: {phone_used}"
        )
        print(log_msg)

        return activity_summary

    except Exception as e:
        log_msg = f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error: {str(e)}"
        print(log_msg)
        return {"error": str(e)}
