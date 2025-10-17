# yawning_detector.py (assuming this is yawn.py)
import cv2
import mediapipe as mp
import numpy as np
from collections import deque

mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=False, max_num_faces=1, refine_landmarks=True,
    min_detection_confidence=0.5, min_tracking_confidence=0.5
)

mar_history = deque(maxlen=10)

def detect(frame):
    status_text = "Not Yawning"
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_face_mesh.process(rgb_frame)

    if not results.multi_face_landmarks:
        return frame, status_text

    for face_landmarks in results.multi_face_landmarks:
        upper_lip_idx = 13
        lower_lip_idx = 14
        left_mouth_idx = 78
        right_mouth_idx = 308

        try:
            upper_lip_y = int(face_landmarks.landmark[upper_lip_idx].y * h)
            lower_lip_y = int(face_landmarks.landmark[lower_lip_idx].y * h)
            left_x = int(face_landmarks.landmark[left_mouth_idx].x * w)
            right_x = int(face_landmarks.landmark[right_mouth_idx].x * w)

            vertical_dist = max(lower_lip_y - upper_lip_y, 1)
            horizontal_dist = max(right_x - left_x, 1)
            mouth_ratio = vertical_dist / horizontal_dist
            mar_history.append(mouth_ratio)

            avg_mar = np.mean(mar_history)

            if avg_mar > 0.22:
                status_text = "Yawning"
            else:
                status_text = "Not Yawning"

            # REMOVED: cv2.putText(frame, status_text, (50, 50), ...)
        except Exception as e:
            continue

    return frame, status_text