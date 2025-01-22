from flask import Flask, render_template, Response, request, jsonify
import cv2
import threading
from flask_cors import CORS
from squat import generate_squat_frames 
from push_up import generate_Push_up_frames
from situp import generate_situp_frames
from cardio import generate_Cardio_frames
from state import get_exercise_counts, get_total_energy, reset_all


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

is_running = False
cap = cv2.VideoCapture(0)
cap_lock = threading.Lock()


@app.route('/')
def index():
    return render_template('index.html')  # Render HTML template for the frontend

# Endpoint to stop the camera
def stop_camera():
    """Release the camera."""
    global is_running, cap
    is_running = False
    if cap.isOpened():
        cap.release()
    print("Camera released")


# Endpoint to get live stream
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
    if exercise == 'pushup':
        return Response(generate_Push_up_frames(cap, is_running),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    elif exercise == 'squat':
        return Response(generate_squat_frames(cap, is_running), mimetype='multipart/x-mixed-replace; boundary=frame')
    elif exercise == 'situp':
        return Response(generate_situp_frames(cap, is_running), mimetype='multipart/x-mixed-replace; boundary=frame')
    elif exercise == 'cardio':
        return Response(generate_Cardio_frames(cap, is_running), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Invalid exercise selected!", 400


# Endpoint to get count for exercise
@app.route('/exercise_count', methods=['GET'])
def exercise_count():
    exercise = request.args.get('exercise') 
    counts = get_exercise_counts()
    if exercise == "all" or not exercise:
        return jsonify(counts)
    elif exercise in counts:
        return jsonify({'exercise': exercise, 'count': counts[exercise]})
    else:
        return jsonify({'error': 'Invalid exercise'}), 400
    

# Endpoint to get te ebergy spent by the user
@app.route('/total_energy', methods=['GET'])
def total_energy():
    total = get_total_energy()
    return jsonify({'total_energy_spent': total})


# Endpoint to reset all variables
@app.route('/reset')
def reset():
    stop_camera()
    reset_all()
    return "reset successfully!"

@app.route('/stop_detection')
def stop_detection():
    """Stop detection."""
    stop_camera()
    return "Detection stopped!"


if __name__ == "__main__":
    app.run(debug=True)
