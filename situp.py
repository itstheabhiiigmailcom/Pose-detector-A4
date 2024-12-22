import cv2
import PoseModule as pm
import numpy as np


def generate_situp_frames(cap, is_running):
    detector = pm.poseDetector()
    count = 0
    form = 0
    direction = 0
    feedback = "Fix Form"
    min_hip_angle = 45 
    max_hip_angle = 90
    min_shoulder_angle = 60
    min_knee_angle  = 50

    while is_running:
        ret, img = cap.read()
        if not ret:
            break
        img = cv2.flip(img, 1)

        width = cap.get(3)
        height = cap.get(4)
        # now process the image
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        
        if len(lmList) != 0:
            hip_angle = detector.findAngle(img, 11, 23, 25)     # angle formed at hip
            shoulder_angle = detector.findAngle(img, 13, 11, 23)    # angle formed at shoulder
            knee_angle = detector.findAngle(img, 23, 25, 27)        # angle formed at knee
            waist_y = lmList[23][2]                 # waist height
            heel_y = lmList[27][2]                  # hill hieght
            
            per = np.interp(hip_angle, (min_hip_angle, max_hip_angle), (0, 100))
            bar = np.interp(hip_angle, (min_hip_angle,max_hip_angle), (380, 50))
            
            if hip_angle>max_hip_angle and shoulder_angle>min_shoulder_angle and knee_angle>min_knee_angle and abs(waist_y - heel_y) < 40:
                form = 1
        
            if form == 1:
                if hip_angle <= min_hip_angle and direction == 0 and abs(waist_y - heel_y) < 40:
                    feedback = "Down"       # now user should go down
                    count += 0.5
                    direction = 1       # now user is in the up position
                elif hip_angle >= max_hip_angle and direction == 1 and abs(waist_y - heel_y) < 40:
                    feedback = "Up"         # now user should go up
                    count += 0.5
                    direction = 0       # now user is in the down position
                else:
                    feedback = "Correct Your Form"
            
            # Draw Progress Bar
            if form == 1:
                cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 0, 0), 2)
            
            # Draw sit-up Counter
            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                        (255, 0, 0), 5)

            # Show Feedback (Fix Form / Up / Down)
            cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 255, 0), 2)
        
        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', img)
        # Yield the frame as part of an mjpeg stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')