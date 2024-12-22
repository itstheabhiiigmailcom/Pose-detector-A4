from flask import Flask, render_template, Response, request
import cv2
import threading
from flask_cors import CORS
from squat import generate_squat_frames 
from push_up import generate_Push_up_frames
from situp import generate_situp_frames


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

is_running = False
cap = cv2.VideoCapture(0)
cap_lock = threading.Lock()


@app.route('/')
def index():
    return render_template('index.html')  # Render HTML template for the frontend


def stop_camera():
    """Release the camera."""
    global is_running, cap
    is_running = False
    if cap.isOpened():
        cap.release()
    print("Camera released")



@app.route('/video_feed')
def video_feed():
    """Render video feed."""
    global is_running, cap
    exercise = request.args.get('exercise')  # Get exercise type
    if is_running:
        stop_camera()

    with cap_lock:
        cap = cv2.VideoCapture(0)  # Reinitialize camera
    is_running = True

    if exercise == 'push_up':
        return Response(generate_Push_up_frames(cap, is_running),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        
    elif exercise == 'squat':
        return Response(generate_squat_frames(cap, is_running), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    elif exercise == 'situp':
        return Response(generate_situp_frames(cap, is_running), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Invalid exercise selected!", 400



@app.route('/stop_detection')
def stop_detection():
    """Stop detection."""
    stop_camera()
    return "Detection stopped!"


if __name__ == "__main__":
    app.run(debug=True)
