from math import atan2, degrees

NOSE = 1
CHIN = 152
TILT_THRESH = 15

def check_head_tilt(landmarks):
    try:
        nose = landmarks[NOSE]
        chin = landmarks[CHIN]
        dy = chin[1] - nose[1]
        dx = chin[0] - nose[0]
        angle = degrees(atan2(dy, dx)) - 90
        tilted = abs(angle) > TILT_THRESH
        return tilted, angle
    except:
        return False, 0.0
