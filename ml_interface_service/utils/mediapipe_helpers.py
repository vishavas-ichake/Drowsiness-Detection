import mediapipe as mp
import cv2

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
MOUTH = [13, 14, 78, 308]
NOSE = 1
CHIN = 152
LEFT_HAND = [19, 20, 21, 22]
RIGHT_HAND = [245, 246, 247, 248]

def extract_landmarks(frame):
    """Return face landmarks or None if not detected."""
    try:
        h, w = frame.shape[:2]
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            coords = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
            return coords
    except Exception as e:
        print("Landmark extraction error:", e)
    return None
