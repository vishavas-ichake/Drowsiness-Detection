from scipy.spatial import distance

MOUTH = [13, 14, 78, 308]
YAWN_THRESH = 0.6

def mouth_open_ratio(landmarks):
    try:
        top = landmarks[MOUTH[0]]
        bottom = landmarks[MOUTH[1]]
        left = landmarks[MOUTH[2]]
        right = landmarks[MOUTH[3]]
        vertical = distance.euclidean(top, bottom)
        horizontal = distance.euclidean(left, right)
        return vertical / horizontal
    except:
        return 0.0

def check_yawn(landmarks):
    ratio = mouth_open_ratio(landmarks)
    return ratio > YAWN_THRESH, ratio
