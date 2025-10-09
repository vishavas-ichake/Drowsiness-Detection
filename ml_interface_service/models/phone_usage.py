from scipy.spatial import distance

LEFT_HAND = [19, 20, 21, 22]
RIGHT_HAND = [245, 246, 247, 248]
NOSE = 1
HAND_THRESH = 50

def check_phone_usage(landmarks):
    try:
        nose = landmarks[NOSE]
        for hand_points in [LEFT_HAND, RIGHT_HAND]:
            for idx in hand_points:
                hand = landmarks[idx]
                if distance.euclidean(nose, hand) < HAND_THRESH:
                    return True
    except:
        return False
    return False
