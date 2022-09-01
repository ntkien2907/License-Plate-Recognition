HOST = '0.0.0.0'
PORT = '5000'

# YOLO_VERSION = 3
# YOLO_WEIGHT  = 'yolov3\\yolov3.weights'
# YOLO_CONFIG  = 'yolov3\\yolov3.cfg'

YOLO_VERSION = 7
YOLO_WEIGHT  = 'yolov7/best.pt'
YOLO_CONFIG  = 'WongKinYiu/yolov7'

BASE_PATH    = 'static'
UPLOAD_PATH  = f'{BASE_PATH}\\upload'
PREDICT_PATH = f'{BASE_PATH}\\predict'
ROI_PATH     = f'{BASE_PATH}\\roi'

CONF_THRESHOLD = 0.5
NMS_THRESHOLD  = 0.4

COLOR = (0, 255, 0)
SCALE = 0.00392