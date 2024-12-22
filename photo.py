import cv2
import time
import threading
import pyttsx3

from ultralytics import YOLO
from cvzone.HandTrackingModule import HandDetector
from read import label_faces  # Import the labeling function

model = YOLO("yolov8n.pt")


def main(citi_no):
        
    def speak(text):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower() or 'feminine' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.say(text)
        engine.runAndWait()

    instructions = (
        "Now get ready to take a picture of yourself. When ready please show a thumb gesture"
    )

    def start_process():
        threading.Thread(target=speak, args=(instructions,)).start()
        detect()

    def capture_image_on_keypress(cap):
        countdown_duration = 10
        captured_frame = None

        while True:
            countdown_start = time.time()
            while True:
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)
                if not ret:
                    print("Error: Could not read frame.")
                    break

                elapsed_time = int(time.time() - countdown_start)
                remaining_time = countdown_duration - elapsed_time

                if remaining_time > 0:
                    cv2.putText(frame, str(remaining_time), (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 7, (0, 255, 0), 10, cv2.LINE_AA)
                else:
                    captured_frame = frame.copy()
                    break

                cv2.imshow("Webcam Person Detection", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            if captured_frame is not None:
                frame1 = captured_frame.copy()
                cv2.putText(frame1, "Press 'y' to save & 'r' to retake", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow("Captured Image", frame1)

                while True:
                    key = cv2.waitKey(0) & 0xFF
                    if key == ord('y'):
                        cv2.putText(frame1, "Saving...", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                        cv2.imshow("Captured Image", frame1)
                        image_path = "captured_image.jpg"
                        cv2.imwrite(image_path, captured_frame)
                        print(f"Image captured and saved as '{image_path}'.")
                        cv2.destroyWindow("Captured Image")

                        # Call the label_faces function here
                        label_faces(image_path, 'pic',citi_no)
                        return True
                    elif key == ord('r'):
                        cv2.destroyWindow("Captured Image")
                        return False
                    elif key == ord('q'):
                        break
            else:
                return False

    def detect():
        cap = cv2.VideoCapture(0)
        detector = HandDetector(detectionCon=0.8, maxHands=1)
        while True:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            if not ret:
                print("Error: Could not read frame.")
                break

            results = model(frame)
            person_detected = False

            for result in results:
                for box in result.boxes:
                    if int(box.cls[0]) == 0:
                        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                        conf = box.conf[0].item()
                        if conf > 0.8:
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2, cv2.LINE_AA)
                            cv2.putText(frame, f'Person {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)
                            
                            hands, _ = detector.findHands(frame)
                            if hands:
                                hand = hands[0]
                                fingers = detector.fingersUp(hand)
                                print(fingers)
                                
                                if fingers == [1, 0, 0, 0, 0]:
                                    save_image = capture_image_on_keypress(cap)
                                    if save_image:
                                        person_detected = True
                                        break

            if person_detected:
                break

            cv2.imshow('Webcam Person Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    start_process()