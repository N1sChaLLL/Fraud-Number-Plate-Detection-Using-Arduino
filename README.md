
# Fraud Number Plate Detection using Embedded Systems

People find new ways of scamming and taking advantages of the poor system present in our country when it comes to roadways. One such thing is faulty number plate, different number plates are attached to the front and rear part of the vehicle. Our system helps the NHAI staff members to identify these faulty number plate cars and put them behind bars for what so ever reason. 


## Authors

- [@Sampath844](https://github.com/Sampath844)
- [@N1sChaLLL](https://github.com/N1sChaLLL)
- [@kanapathi123](https://github.com/kanapathi123)


## Screenshots

![1](https://github.com/user-attachments/assets/cca0f71f-fa20-4602-a58c-c6005c70c629)
![2](https://github.com/user-attachments/assets/dfa5ccf0-b0a8-4396-bda7-45fff9d5bf69)
![3](https://github.com/user-attachments/assets/f544239a-cf55-49af-bb48-26600e269a06)
![4](https://github.com/user-attachments/assets/6c71e62c-3269-40cc-af13-a9c402fc6e15)



## Installation

Install my-project with these modules

```bash
import cv2
import cvzone
import math
from ultralytics import YOLO
import pytesseract
from datetime import datetime
import time
```
These are the modules needed to run our YOLOv8 code.
    
## Tech Stack

**Dataset** :- We have created our own dataset of number plates, it has been added in our repository.

**Model** :- We have used YOLOv8 (You only look once) image recognition model which using CNN (Convolutional Neural Networks) to learn from the images.

**Hardware** :- We have used a LCD with I2C module soldered to it. Arduiuno UNO Board. Jumper Wires.

**Software** :- To run the machine learning model code, we have used VScode. To run the Arduiuno code we have used to Arduiuno IDE.



## Connections

The LCD has 4 pins. 
- VCC for Voltage this must be connected to the 5V pin of Arduino.
- GND is ground and must be connected to the ground of Arduino.
- SCL is Serial clock pin it must be connected to the A5 (Analog 5) of Arduino.
- SDA is Serial data pin it must be connected to the A4 (Analog 4 ) of Arduino.


## Lessons Learned

We learnt how to combine both machine learning and embedded systems to build a efficient systems which can help the government catch these scammers. We also learnt how we efficiently use the Arduino UNO and the pins of it. 
