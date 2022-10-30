from cvlib.object_detection import YOLO
import cv2

weights="../python/YoloV4/yolov3.weights"
config="../python/YoloV4/yolov3.cfg"
labels="../python/YoloV4/coco.names"

yolo = YOLO(weights, config,labels)

def yolo_object_detection(img):
    detection = []
    img=cv2.resize(img,(680,460))
    bbox, label, conf = yolo.detect_objects(img)
    for i in range(len(label)):
        detection.append({label[i]:bbox[i]})
    return detection
