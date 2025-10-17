import cv2
import numpy as np

def detect(frame):
    status_text = "No Phone Detected"
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_color = np.array([0, 0, 200])
    upper_color = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower_color, upper_color)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    phone_detected = False

    for contour in contours:
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(contour)

            if w > 100 and h > 100:
                phone_detected = True
                # **KEEP** visual indicator (contour drawing)
                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)
                status_text = "Phone Detected"
                # REMOVED: cv2.putText(frame, status_text, (x, y - 10), ...)

    # REMOVED: cv2.putText(frame, status_text, (30, 50), ...)

    return frame, status_text