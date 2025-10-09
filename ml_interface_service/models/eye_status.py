from scipy.spatial import distance
from time import time

EAR_THRESH = 0.25
CONSEC_FRAMES = 5
DROWSY_DURATION = 8.0

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

frame_counter = 0
closed_start_time = None

def eye_aspect_ratio(eye_points):
    try:
        A = distance.euclidean(eye_points[1], eye_points[5])
        B = distance.euclidean(eye_points[2], eye_points[4])
        C = distance.euclidean(eye_points[0], eye_points[3])
        return (A + B) / (2.0 * C)
    except:
        return 1.0  # fallback EAR if points missing

def check_eye_status(landmarks):
    global frame_counter, closed_start_time
    try:
        left_eye = [landmarks[i] for i in LEFT_EYE]
        right_eye = [landmarks[i] for i in RIGHT_EYE]
        ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0
    except:
        return "unknown", 0.0

    status = "open"
    if ear < EAR_THRESH:
        frame_counter += 1
        if closed_start_time is None:
            closed_start_time = time()
        duration = time() - closed_start_time
        if frame_counter >= CONSEC_FRAMES and duration >= DROWSY_DURATION:
            status = "closed_long"
    else:
        frame_counter = 0
        closed_start_time = None
        status = "open"

    return status, ear
