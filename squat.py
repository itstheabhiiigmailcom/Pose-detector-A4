# from shared import is_running_squart
import cv2
import numpy as np
from PoseModule import poseDetector
from state import update_exercise_count, get_exercise_counts

def generate_squat_frames(cap, is_running) :
    detector = poseDetector()
    direction = 0
    form = 0
    threshold=100
    feedback = "Fix Form"
    arr = []
    while is_running:
        ret, img = cap.read()  # 640 x 480
        if not ret:
            break
        img = cv2.flip(img, 1)
        # Determine dimensions of video - Help with creation of box in Line 43
        width = cap.get(3)  # float `width`
        height = cap.get(4)  # float `height`
        # print(width, height)

        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        # print(lmList)
        if len(lmList) != 0:

            hip = detector.findAngle(img, 11, 23, 25)
            knee = detector.findAngle(img, 23, 25, 27)
            # Percentage of success of pushup
            per = np.interp(knee, (90, 160), (0, 100))

            # Bar to show Pushup progress
            bar = np.interp(knee, (90, 160), (380, 50))

            # Check to ensure right form before starting the program
            if knee>160 and hip>160:
                shoulder_level = lmList[11][2]
                form = 1
                if not len(arr):
                    arr.append(shoulder_level)
                else:
                    current_level = lmList[11][2]
                    difference = abs(arr[0]-current_level)
                    # print(f"shoulder_level: {arr[0]},current_level: {current_level},difference: {difference}")
            # Check for full range of motion for the pushup
            if form == 1:

                if per > 85:

                    if knee > 140 and hip > 140:
                        feedback = "Down"
                        # print("down wala if", hip, knee)
                        if direction == 0:
                            update_exercise_count("squat", 0.5)
                            direction = 1
                    else:
                        feedback = "Fix Form"
                        # form = 0


                if per < 15:
                    if not len(arr):
                        arr.append(shoulder_level)
                    else:
                        current_level = lmList[11][2]
                        difference = abs(arr[0] - current_level)
                        # print(f"SHLD: {arr[0]},CURR: {current_level}, DIFF: {difference}")

                    if knee < 90 and hip < 120 and (difference>threshold):
                        feedback = "Up"
                        if direction == 1:
                            update_exercise_count("squat", 0.5)
                            # print("count hai 1")
                            direction = 0
                    else:
                        feedback = "Fix Form"
                        # form = 0
            # print(count)
            # Draw Bar
            if form == 1:
                cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 0, 0), 2)

            # Pushup counter
            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(get_exercise_counts()['squat'])), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                        (255, 0, 0), 5)

            # Feedback
            cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 255, 0), 2)
        else:
            if len(arr):
                arr.pop()
                
        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', img)

        # Yield the frame as part of an mjpeg stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        # cv2.imshow('Pushup counter', img)
        # if cv2.waitKey(10) & 0xFF == ord('q'):
        #     break