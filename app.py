# app.py
from Models import yawn, eye, phone, tilted # Corrected imports
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)

        # 1. Run detections and get STATUS text
        # The frame is updated with visual indicators (like boxes, polylines) inside the model files
        frame, yawn_status = yawn.detect(frame)
        frame, drowsy_status = eye.detect(frame)
        frame, head_tilt_status = tilted.detect(frame)
        frame, phone_status = phone.detect(frame)
        
        # 2. Collect all statuses into a list
        status_lines = [
            f"1. Yawn: {yawn_status}",
            f"2. Drowsy: {drowsy_status}",
            f"3. Head Tilt: {head_tilt_status}",
            f"4. Phone: {phone_status}"
        ]

        # 3. Centralized Drawing (Stacked List)
        y_offset = 30 # Starting Y coordinate for the first line
        line_height = 30 # Vertical spacing between lines

        for i, line in enumerate(status_lines):
            # Use red color for alerts
            color = (0, 0, 255) if "ALERT" in line or "Tilted" in line or "Yawning" in line or "Detected" in line else (0, 255, 0)
            
            current_y = y_offset + (i * line_height)
            
            cv2.putText(frame, line, (10, current_y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)