from ultralytics import YOLO
import cvzone
import cv2
import math

# Running real time from webcam
cap = cv2.VideoCapture('../drinking.mp4')
model = YOLO('./general.pt')

# Reading the classes
classnames=['cell phone', 'drinking', 'eyeglass', 'hands off', 'hands on', 'mask', 'seatbelt', 'smoking']

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame,(640,480))
    result = model(frame, stream=True)

    for info in result:
        boxes = info.boxes
        for box in boxes:
            connfidence = box.conf[0]
            connfidence = math.ceil(connfidence * 100)
            Class = int(box.cls[0])
            if connfidence > 50 and classnames[Class] == 'drinking':
                x1,y1,x2,y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1),int(y1),int(x2),int(y2)
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),5)
                cvzone.putTextRect(frame, f'{classnames[Class]} {connfidence}%', [x1+8, y1+100], scale=1.5, thickness=2)
                

    cv2.imshow('frame', frame)
    cv2.waitKey(1)
