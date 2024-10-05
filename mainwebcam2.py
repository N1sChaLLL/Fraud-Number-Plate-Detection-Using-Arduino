import cv2
import cvzone
import math
from ultralytics import YOLO
import pytesseract
from datetime import datetime
import time

# Set the path for pytesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Use webcam instead of video file
cap = cv2.VideoCapture(2)  # Use '0' for default webcam, change to '1', '2', etc., if needed

# Load the YOLO model
model = YOLO('license_plate_detector.pt')
classnames = ['number-plate']

# Open file for writing recognized number plates
with open("license_plates.txt", "a") as file:
    file.write("NumberPlate\tDate\tTime\n")  # Writing column headers
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

                # If text is detected, save it to the file
                if text:
                    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("license_plates.txt", "a") as file:
                        file.write(f"{text}\t{current_datetime}\n")
                    print(f"Detected text: {text}")

    # Display the frame with detections
    cv2.imshow('frame', frame)

    # Exit when 't' is pressed
    if (cv2.waitKey(1) & 0xFF == ord('t')) or (time.time() - start_time  > 30):
        break

cap.release()
cv2.destroyAllWindows()
