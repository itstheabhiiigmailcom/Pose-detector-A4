from flask import Flask, render_template, Response
import cv2
import numpy as np
import PoseModule as pm
import threading
# import push_up_counter  # Import your existing detection module

app = Flask(__name__)
is_running = False

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()




def generate_frames():
    global is_running
    # Adjust these values for a more flexible range of motion
    min_elbow_angle = 90  # Min angle for 'Up' position
    max_elbow_angle = 160  # Max angle for 'Down' position
    count = 0
    direction = 0
    form = 0
    feedback = "Fix Form"

    while cap.isOpened() and is_running:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:
             # Get angles of the body parts
            elbow = detector.findAngle(img, 11, 13, 15)  # Elbow angle
            shoulder = detector.findAngle(img, 13, 11, 23)  # Shoulder angle
            hip = detector.findAngle(img, 11, 23, 25)  # Hip angle

            # Interpolate elbow angle to percentage (progress bar)
            per = np.interp(elbow, (min_elbow_angle, max_elbow_angle), (0, 100))
            bar = np.interp(elbow, (min_elbow_angle, max_elbow_angle), (380, 50))

            shoulder_y = lmList[11][2]
            hip_y = lmList[23][2]

            # Check if body is at an appropriate height (use shoulder and hip Y positions)
            if abs(shoulder_y - hip_y) < 100:  # If the shoulder and hip are close in height, it's a horizontal position (push-up)
                is_pushup = True
            else:
                is_pushup = False

            # Form validation: Ensure body parts are aligned correctly before counting
            if elbow > max_elbow_angle and shoulder > 40 and hip > 160 and is_pushup:
                form = 1  # Indicate that the form is correct

            if form == 1:
                if elbow <= min_elbow_angle and direction == 0:  # Going up
                    feedback = "Up"
                    count += 0.5  # Increment count (since we detect two phases)
                    direction = 1  # Now we're in the 'Up' position
                elif elbow >= max_elbow_angle and direction == 1:  # Going down
                    feedback = "Down"
                    count += 0.5  # Increment count
                    direction = 0  # Now we're in the 'Down' position
                else:
                    feedback = "Fix Form"  # Feedback if form is incorrect

            # Draw Progress Bar
            if form == 1:
                cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 0, 0), 2)

            # Draw Push-up Counter
            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                        (255, 0, 0), 5)

            # Show Feedback (Fix Form / Up / Down)
            cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 255, 0), 2)

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        # Yield the frame in an HTTP response format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()





@app.route('/')
def index():
    return render_template('index.html')  # Render HTML template for the frontend

@app.route('/start_detection')
def start_detection():
    global is_running, cap
    if not is_running:
        cap.open(0)  # Reinitialize the camera if necessary
        is_running = True
        threading.Thread(target=generate_frames).start()  # Start frame generation in a new thread
    return "Detection started!"


@app.route('/stop_detection')
def stop_detection():
    global is_running, cap
    is_running = False  # Stop the detection loop
    if cap.isOpened():
        cap.release()  # Release the camera
    return "Detection stopped!"


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
