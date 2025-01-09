import cv2
import numpy as np
import sys
import time

def try_camera_index(index):
    cap = cv2.VideoCapture(index)
    if cap is None or not cap.isOpened():
        return None
    return cap

def init_camera():
    # Try different camera indices
    for idx in range(3):  # Try indices 0, 1, 2
        print(f"Trying camera index {idx}...")
        cap = try_camera_index(idx)
        if cap is not None:
            print(f"Successfully opened camera {idx}")
            return cap
    return None

# Initialize video capture
cap = init_camera()
if cap is None:
    print("Error: Could not open any camera")
    sys.exit(1)

# Load the face cascade classifier
try:
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        raise Exception("Failed to load cascade classifier")
except Exception as e:
    print(f"Error loading cascade classifier: {e}")
    cap.release()
    sys.exit(1)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Draw rectangle around each detected face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Add FPS counter
        cv2.putText(frame, f'Press Q to quit', (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow('Face Tracking', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    cap.release()
    cv2.destroyAllWindows()
