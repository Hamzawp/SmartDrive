import cv2
import os
import datetime as dt
import numpy as np
import tensorflow as tf
import torch
from keras.models import load_model
from ultralytics import YOLO
import cvzone
import math
import time

print("Script loaded. Import complete")

TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_phone_number"
RECIPIENT_PHONE_NUMBER = "recipient_phone_number"

OBJECT_DETECTION_MODEL_PATH = "./Finding-seatbelt/best.pt"
PREDICTOR_MODEL_PATH = "./Finding-seatbelt/keras_model.h5"
CLASS_NAMES = {0: "No Seatbelt worn", 1: "Seatbelt Worn"}
SEATBELT_THRESHOLD_SCORE = 0.99
SMOKING_DRINKING_THRESHOLD_SCORE = 0.8
SKIP_FRAMES = 1
MAX_FRAME_RECORD = 500
INPUT_VIDEO = "./drinking.mp4"
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
output_width = 1000
output_height = 600

# Load the pre-trained face cascade and eye cascade for drowsiness detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")


def log_activity(activity):
    timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("activity_log.txt", "a") as file:
        file.write(f"{timestamp}: {activity}\n")


def prediction_func(img):
    img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
    img = (img / 127.5) - 1
    img = tf.expand_dims(img, axis=0)
    pred = predictor.predict(img)
    index = np.argmax(pred)
    class_name = CLASS_NAMES[index]
    confidence_score = pred[0][index]
    return class_name, confidence_score


def resize_frame(img, width=640, height=360):
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)


def limit_roi(img, x_min=0, y_min=0, x_max=output_width, y_max=output_height):
    return img[y_min:y_max, x_min:x_max]


def filter_detections(
    boxes, min_size=20, max_size=200, min_conf=SMOKING_DRINKING_THRESHOLD_SCORE
):
    filtered_boxes = []
    for box in boxes:
        x1, y1, x2, y2, conf = box.xyxy[0]
        if conf >= min_conf:
            box_width = x2 - x1
            box_height = y2 - y1
            box_size = box_width * box_height
            if min_size**2 <= box_size <= max_size**2:
                filtered_boxes.append(box)
    return filtered_boxes


last_alert_time = time.time()
predictor = load_model(PREDICTOR_MODEL_PATH, compile=False)
print("Predictor loaded")
model = torch.hub.load(
    "ultralytics/yolov5", "custom", path=OBJECT_DETECTION_MODEL_PATH, force_reload=False
)
smoking_model = YOLO("./Smoking-detection/cigar.pt")
drinking_model = YOLO("./Drinking-detection/general.pt")
classnames_cigar = ['cigarette']
classnames_drink = ['cell phone', 'drinking', 'eyeglass', 'hands off', 'hands on', 'mask', 'seatbelt', 'smoking']
cap = cv2.VideoCapture(INPUT_VIDEO)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))


# def draw_dashboard(img, smoking_detected, drinking_detected, seatbelt_detected, drowsy):
#     dashboard_color = (0, 0, 0)
#     dashboard_height = 100
#     cv2.rectangle(img, (0, 0), (output_width, dashboard_height), dashboard_color, -1)
#     cv2.putText(
#         img, "Dashboard", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2
#     )
#     indicator_size = 20
#     indicator_start_x = 150
#     cv2.putText(
#         img,
#         "Smoking:",
#         (indicator_start_x, 50),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         0.5,
#         (255, 255, 255),
#         2,
#     )
#     cv2.putText(
#         img,
#         "Drinking:",
#         (indicator_start_x, 75),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         0.5,
#         (255, 255, 255),
#         2,
#     )
#     cv2.putText(
#         img,
#         "Seatbelt:",
#         (indicator_start_x, 100),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         0.5,
#         (255, 255, 255),
#         2,
#     )
#     cv2.putText(
#         img,
#         "Drowsy:",
#         (indicator_start_x + 270, 75),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         0.5,
#         (255, 255, 255),
#         2,
#     )
#     cv2.rectangle(
#         img,
#         (indicator_start_x + 70, 35),
#         (indicator_start_x + 70 + indicator_size, 35 + indicator_size),
#         (0, 255, 0) if smoking_detected else (0, 0, 255),
#         -1,
#     )
#     cv2.rectangle(
#         img,
#         (indicator_start_x + 70, 60),
#         (indicator_start_x + 70 + indicator_size, 60 + indicator_size),
#         (0, 255, 0) if drinking_detected else (0, 0, 255),
#         -1,
#     )
#     cv2.rectangle(
#         img,
#         (indicator_start_x + 70, 85),
#         (indicator_start_x + 70 + indicator_size, 85 + indicator_size),
#         (0, 255, 0) if seatbelt_detected else (0, 0, 255),
#         -1,
#     )
#     cv2.rectangle(
#         img,
#         (indicator_start_x + 340, 60),
#         (indicator_start_x + 340 + indicator_size, 60 + indicator_size),
#         (0, 255, 0) if not drowsy else (0, 0, 255),
#         -1,
#     )

frame_rate = cap.get(cv2.CAP_PROP_FPS)
seconds_between_frames = 1 / frame_rate
frame_count = 0
try:
    # start_time = time.time()
    while True:
        ret, img = cap.read()
        if ret:
            frame_count += 1
            if frame_count % SKIP_FRAMES == 0:
                start_time = time.time()
                img = resize_frame(img)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = limit_roi(
                    img, x_min=0, y_min=0, x_max=output_width, y_max=output_height
                )

                # Detect driver seatbelt
                results = model(img)
                boxes = results.xyxy[0]
                boxes = boxes.cpu()
                seatbelt_detected = False
                for j in boxes:
                    x1, y1, x2, y2, score, class_index = j.numpy()
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    img_crop = img[y1:y2, x1:x2]
                    y_pred, score = prediction_func(img_crop)
                    if y_pred == CLASS_NAMES[0] or class_index > 0:
                        log_activity(f"Seatbelt not worn at frame {frame_count}")
                        seatbelt_detected = False
                        current_time = time.time()
                        if current_time - last_alert_time >= 7200:
                            last_alert_time = current_time
                    elif y_pred == CLASS_NAMES[1]:
                        seatbelt_detected = True
                        log_activity(f"Seatbelt worn detected at frame {frame_count}")
                    if score >= SEATBELT_THRESHOLD_SCORE:
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
                        cv2.putText(
                            img,
                            f"{y_pred} {str(score)[:4]}",
                            (x1 - 10, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            COLOR_GREEN,
                            1,
                        )

                # Detect smoking and drinking
                result_cigar = smoking_model(img, stream=True)
                result_drink = drinking_model(img, stream=True)
                # result = smoking_drinking_model(img, stream=True)
                smoking_detected = False
                drinking_detected = False
                for info in result_cigar:
                    boxes = info.boxes
                    for box in boxes:
                        confidence = box.conf[0]
                        confidence = math.ceil(confidence * 100)
                        Class = int(box.cls[0])
                        if confidence > 50:
                            smoking_detected = True
                            x1, y1, x2, y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                            cvzone.putTextRect(img, f'{classnames_cigar[Class]} {confidence}%', [x1 + 8, y1 + 100], scale=1, thickness=1)
                            log_activity(f"Smoking detected at frame {frame_count} with confidence {confidence}%")

                for info in result_drink:
                    boxes = info.boxes
                    for box in boxes:
                        connfidence = box.conf[0]
                        connfidence = math.ceil(connfidence * 100)
                        Class = int(box.cls[0])
                        if connfidence > 50 and classnames_drink[Class] == 'drinking':
                            x1,y1,x2,y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1),int(y1),int(x2),int(y2)
                            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),5)
                            cvzone.putTextRect(img, f'{classnames_drink[Class]} {connfidence}%', [x1+8, y1+100], scale=1.5, thickness=2)
                            log_activity(f"Drinking detected at frame {frame_count} with confidence {connfidence}%")



                # Drowsiness detection
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                drowsy = False
                for x, y, w, h in faces:
                    roi_gray = gray[y : y + h, x : x + w]
                    roi_color = img[y : y + h, x : x + w]
                    eyes = eye_cascade.detectMultiScale(roi_gray)
                    if len(eyes) == 0:
                        drowsy = True
                        log_activity(f"Drowsiness detected at frame {frame_count}")
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        cv2.putText(
                            img,
                            "Drowsy",
                            (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 0, 255),
                            1,
                        )
                    else:
                        drowsy = False
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(
                            img,
                            "Awake",
                            (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 255, 0),
                            1,
                        )

                # draw_dashboard(
                #     img, smoking_detected, drinking_detected, seatbelt_detected, drowsy
                # )

                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                cv2.namedWindow("Video feed", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("Video feed", output_width, output_height)
                cv2.imshow("Video feed", img)

                # log_activity(f"Seatbelt worn at time {elapsed_time}s") if seatbelt_detected else None
                # log_activity(f"Seatbelt not worn detected at time {elapsed_time}s") if not seatbelt_detected else None
                # log_activity(f"Smoking detected at time {elapsed_time}s with confidence {confidence}%") if smoking_detected else None
                # log_activity(f"Drinking detected at time {elapsed_time}s with confidence {confidence}%") if drinking_detected else None
                # log_activity(f"Drowsiness detected at time {elapsed_time}s") if drowsy else None

        else:
            break
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
except KeyboardInterrupt:
    pass
finally:
    seatbelt_count = 0
    seatbelt_notcount = 0
    smoking_detected = False
    drinking_detected = False
    drowsiness_detected = False

    with open('activity_log.txt', 'r') as file:
        lines = file.readlines()

    # Process the log file
    for line in lines:
        if 'Seatbelt worn detected' in line:
            seatbelt_count += 1
        elif 'Seatbelt not worn' in line:
            seatbelt_notcount += 1
        elif 'Smoking detected' in line:
            smoking_detected = True
        elif 'Drinking detected' in line:
            drinking_detected = True
        elif 'Drowsiness detected' in line:
            drowsiness_detected = True

    # Calculate seatbelt rating
    seatbelt_rating = seatbelt_count / (seatbelt_count + seatbelt_notcount) * 100  # Assuming 30 frames per second
    print(f"Seatbelt Rating: {seatbelt_rating:.2f}/100")
    print(f"Smoking Detected: {smoking_detected}")
    print(f"Drinking Detected: {drinking_detected}")
    print(f"Drowsiness Detected: {drowsiness_detected}")
    
    cap.release()
    cv2.destroyAllWindows()
    print("Script run complete.")
