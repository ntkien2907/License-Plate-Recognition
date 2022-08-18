import os
import cv2
import numpy as np
import pytesseract as pt
from config import *


if not os.path.exists(BASE_PATH): 
    os.mkdir(BASE_PATH)
if not os.path.exists(UPLOAD_PATH): 
    os.mkdir(UPLOAD_PATH)
if not os.path.exists(PREDICT_PATH): 
    os.mkdir(PREDICT_PATH)
if not os.path.exists(ROI_PATH): 
    os.mkdir(ROI_PATH)

TESSERACT_EXE = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'


def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers


def object_detection_yolo(img_path):
    image = cv2.imread(img_path)
    w = image.shape[1]
    h = image.shape[0]

    net  = cv2.dnn.readNet(YOLO_WEIGHT, YOLO_CONFIG)
    blob = cv2.dnn.blobFromImage(image, SCALE, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    class_ids   = []
    confidences = []
    boxes       = []
    n_coords    = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                w = int(detection[2] * w)
                h = int(detection[3] * h)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONF_THRESHOLD, NMS_THRESHOLD)

    for i in indices:
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        xmin, xmax, ymin, ymax = round(x), round(x + w), round(y), round(y + h)
        n_coords.append([xmin, xmax, ymin, ymax])
    
    return n_coords


def OCR(img_path, filename):
    n_coords = object_detection_yolo(img_path)
    if len(n_coords) == 0:
        return None
    
    img = cv2.imread(img_path)
    xmin, xmax, ymin, ymax = n_coords[0]
    roi = img[ymin:ymax, xmin:xmax]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, img_binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite(f'{ROI_PATH}\\{filename}', roi)
    
    pt.pytesseract.tesseract_cmd = TESSERACT_EXE
    text = pt.image_to_string(img_binary, lang='eng', config='--psm 6')
    if len(text) == 0:
        return None

    save_text(filename, text)
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), COLOR, 2)
    cv2.imwrite(f'{PREDICT_PATH}\\{filename}', img)

    return text


def save_text(filename, text):
    name, ext = os.path.splitext(filename)
    with open(f'{PREDICT_PATH}\\{name}.txt', mode='w') as f:
        f.write(text)
    f.close()