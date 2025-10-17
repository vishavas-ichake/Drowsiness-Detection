import cv2
import mediapipe as mp
import time
from scipy.spatial import distance
import numpy as np

EAR_THRESH = 0.25
CONSEC_FRAMES = 5
DROWSY_THRESHOLD = 8.0

frame_counter = 0
closed_start_time = None

mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(eye_points):
    A = distance.euclidean(eye_points[1], eye_points[5])
    B = distance.euclidean(eye_points[2], eye_points[4])
    C = distance.euclidean(eye_points[0], eye_points[3])
    return (A + B) / (2.0 * C)

def detect(frame):
    global frame_counter, closed_start_time

    h, w = frame.shape[:2]
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = mp_face_mesh.process(rgb_frame)
    status_text = "Eyes Open" # Default status

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            left_eye = [(int(face_landmarks.landmark[i].x * w),
                         int(face_landmarks.landmark[i].y * h)) for i in LEFT_EYE]
            right_eye = [(int(face_landmarks.landmark[i].x * w),
                          int(face_landmarks.landmark[i].y * h)) for i in RIGHT_EYE]

            leftEAR = eye_aspect_ratio(left_eye)
            rightEAR = eye_aspect_ratio(right_eye)
            ear = (leftEAR + rightEAR) / 2.0

            # **KEEP** visual indicator (polylines)
            cv2.polylines(frame, [np.array(left_eye)], True, (0,255,0), 1)
            cv2.polylines(frame, [np.array(right_eye)], True, (0,255,0), 1)

            if ear < EAR_THRESH:
                frame_counter += 1
                if closed_start_time is None:
                    closed_start_time = time.time()
                time_closed = time.time() - closed_start_time

                if frame_counter >= CONSEC_FRAMES and time_closed >= DROWSY_THRESHOLD:
                    status_text = "DROWSY ALERT"
                    # **KEEP** visual indicator (red border and WAKE UP text)
                    cv2.rectangle(frame, (0,0), (w,h), (0,0,255), 6)
                    cv2.putText(frame, "WAKE UP!", (w//2 - 100, h//2),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 3)
                else:
                    status_text = f"Eyes Closed (EAR: {ear:.2f})"
            else:
                frame_counter = 0
                closed_start_time = None
                status_text = f"Eyes Open (EAR: {ear:.2f})"

            # REMOVED: cv2.putText(frame, f"EAR: {ear:.2f} | Count: {frame_counter}", (10, 60), ...)

    # REMOVED: cv2.putText(frame, status_text, (10, 30), ...)
    
    return frame, status_text