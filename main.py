import time
import mss
import numpy as np
import cv2
from PIL import ImageGrab
from flask import Flask, Response
import pyautogui

app = Flask(__name__)

def capture_screen():
    # Capture the entire screen
    img = ImageGrab.grab()
    
    # Get cursor position
    cursor_pos = pyautogui.position()
    return np.array(img), cursor_pos

def generate_frames():
    while True:
        frame, cursor_pos = capture_screen()
        # Convert frame to JPEG for streaming
        _, jpeg = cv2.imencode('.jpg', frame)
        
        # Create frame with cursor position overlay
        frame_with_cursor = cv2.circle(frame, cursor_pos, radius=10, color=(0, 0, 255), thickness=-1)
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame_with_cursor)[1].tobytes() + b'\r\n')
        # time.sleep(0.1)  # Adjust the sleep time if needed

@app.route('/')
def stream_screen():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
