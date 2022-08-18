BASE_PATH    = 'static'
UPLOAD_PATH  = f'{BASE_PATH}\\upload'
PREDICT_PATH = f'{BASE_PATH}\\predict'
ROI_PATH     = f'{BASE_PATH}\\roi'

YOLO_WEIGHT = 'yolov3\\yolov3.weights'
YOLO_CONFIG = 'yolov3\\yolov3.cfg'

CONF_THRESHOLD = 0.5
NMS_THRESHOLD  = 0.4

COLOR = (0, 0, 255)
SCALE = 0.00392

HOST = '0.0.0.0'
PORT = '5000'