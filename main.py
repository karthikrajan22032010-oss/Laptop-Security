import cv2
from deepface import DeepFace
import winsound
import os

print("========================================")
print("🚨 AI Face Match Alarm RUNNING!")
print("Press 'q' on your keyboard to stop.")
print("========================================")

# Start Laptop Camera
cap = cv2.VideoCapture(0)

# Fast Face Detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        # PUDHU NAME: "live_face.jpg"
        cv2.imwrite("live_face.jpg", frame)
        
        try:
            # AI Magic: Compare live face with family.jpg
            result = DeepFace.verify(img1_path="family.jpg", img2_path="live_face.jpg", enforce_detection=False)
            
            if result["verified"] == True:
                # MATCH! (Green Box, No Alarm)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "MATCHED! WELCOME", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                # NO MATCH! (Red Box + LOUD ALARM!)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(frame, "UNKNOWN! ALARM!", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Show the red box on screen and play alarm
                cv2.imshow("Laptop Security Camera", frame)
                cv2.waitKey(1)
                winsound.Beep(2500, 1000) # Beeps for 1 second
                
        except Exception as e:
            pass

    # Show the video
    cv2.imshow("Laptop Security Camera", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Clean up temp file
if os.path.exists("live_face.jpg"):
    os.remove("live_face.jpg")