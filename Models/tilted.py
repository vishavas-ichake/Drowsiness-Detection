import cv2
import mediapipe as mp
import math

mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def calculate_head_tilt_angle(landmarks, image_width, image_height):
    left_eye = landmarks.landmark[33]
    right_eye = landmarks.landmark[263]

    left_eye_coords = (left_eye.x * image_width, left_eye.y * image_height)
    right_eye_coords = (right_eye.x * image_width, right_eye.y * image_height)

    delta_y = right_eye_coords[1] - left_eye_coords[1]
    delta_x = right_eye_coords[0] - left_eye_coords[0]
    angle = math.degrees(math.atan2(delta_y, delta_x))

    return angle

def detect(frame):
    status_text = "Head Straight"
    h, w = frame.shape[:2]
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = mp_face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            angle = calculate_head_tilt_angle(face_landmarks, w, h)

            if abs(angle) > 10:
                status_text = f"Head Tilted ({angle:.1f}°)" # Include angle in status
            else:
                status_text = f"Head Straight ({angle:.1f}°)"

            # REMOVED: All cv2.putText calls
            
    return frame, status_text