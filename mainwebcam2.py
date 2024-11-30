import cv2
import cvzone
import math
from ultralytics import YOLO
import pytesseract
from datetime import datetime
import time
import serial

# Initialize Arduino connection
arduino = serial.Serial(port='COM8', baudrate=9600, timeout=1)

def send_to_lcd(data):
    """Sends data to the Arduino."""
    if arduino.isOpen():
        arduino.write((data + '\n').encode())  # Send data to Arduino
        print(f"Sent to LCD: {data}")
        time.sleep(1)  # Short delay to ensure Arduino processes it

# Set the path for pytesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Use webcam
cap = cv2.VideoCapture(2)  # Use '0' for default webcam, change as needed

if not cap.isOpened():
    print("Error: Camera could not be initialized!")
    exit()

# Load the YOLO model
model = YOLO('goodone.pt')
classnames = ['number-plate']

# Function to detect number plates
def detect_plate():
    detected_plate = None
    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame = cv2.resize(frame, (1080, 720))
        results = model(frame)

        for result in results:
            parameters = result.boxes
            for box in parameters:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                confidence = box.conf[0]
                class_detect = box.cls[0]
                class_detect = int(class_detect)
                class_detect = classnames[class_detect]
                conf = math.ceil(confidence * 100)
                if conf > 50 and class_detect == 'number-plate':
                    # Draw rectangle around detected license plate
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # Display the class and confidence
                    cvzone.putTextRect(frame, f'{class_detect} {conf}%', [x1 + 8, y1 - 12], thickness=2, scale=1)

                    # Crop the detected license plate from the frame
                    crop_img = frame[y1:y2, x1:x2]

                    # Convert the cropped image to grayscale for better OCR performance
                    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

                    # Recognize text from the license plate using pytesseract
                    text = pytesseract.image_to_string(gray, config='--psm 8').strip()

                    if text:
                        print(f"Detected text: {text}")

            # Display the frame
        cv2.imshow('frame', frame)

        # Exit when 't' is pressed
        if (cv2.waitKey(1) & 0xFF == ord('t')) or (time.time() - start_time > 10):
            break

    return text

# Detect the front plate
print("Reposition the camera for the front plate. Press Enter to continue...")
input()
print("Starting front plate detection.")
front_plate = detect_plate()
print(f"Front Plate: {front_plate}")
if front_plate:
    send_to_lcd(f"F: {front_plate}")

# Wait for the user to reposition the camera for the rear plate
print("Reposition the camera for the rear plate. Press Enter to continue...")
input()

# Detect the rear plate
print("Starting rear plate detection.")
rear_plate = detect_plate()
print(f"R: {rear_plate}")
if rear_plate:
    send_to_lcd(f"Rear: {rear_plate}")

# Compare the plates
if front_plate and rear_plate:
    if front_plate.lower().strip() == rear_plate.lower().strip():
        print("Front and Rear Plates Match!")
        send_to_lcd("Match: True")
        time.sleep(6)  # Delay for displaying match status
        send_to_lcd(f"R: {rear_plate}")
        time.sleep(6)  # Delay for displaying rear plate
        send_to_lcd(f"F: {front_plate}")
        time.sleep(6)  # Delay for displaying front plate
    else:
        print("Front and Rear Plates Do Not Match!")
        send_to_lcd("Match: False")
        time.sleep()  # Delay for displaying match status
        send_to_lcd(f"R: {rear_plate}")
        time.sleep()  # Delay for displaying rear plate
        send_to_lcd(f"F: {front_plate}")
        time.sleep()  # Delay for displaying front plate
else:
    print("Detection failed for one or both plates!")
    send_to_lcd("Error")

cap.release()
cv2.destroyAllWindows()