import cv2
from scipy.misc import face
from constants import *
import numpy as np
from PIL import Image
import tensorflow as tf
from Tensorflow.detection import detect_fn,category_index

fonts = cv2.FONT_HERSHEY_COMPLEX
fonts2 = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
fonts3 = cv2.FONT_HERSHEY_COMPLEX_SMALL
fonts4 = cv2.FONT_HERSHEY_TRIPLEX
# Camera Object
cap = cv2.VideoCapture(0)  # Number According to your Camera
Distance_level = 0

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"XVID")
# out = cv2.VideoWriter("output21.mp4", fourcc, 30.0, (640, 480))

# face detector object
face_detector = cv2.CascadeClassifier(
    "../python/models/haarcascade_frontalface_default.xml")
# focal length finder function


def FocalLength(measured_distance, real_width, width_in_rf_image):
    # Function Discrption (Doc String)
    """
    This Function Calculate the Focal Length(distance between lens to CMOS sensor), it is simple constant we can find by using
    MEASURED_DISTACE, REAL_WIDTH(Actual width of object) and WIDTH_OF_OBJECT_IN_IMAGE
    :param1 Measure_Distance(int): It is distance measured from object to the Camera while Capturing Reference image

    :param2 Real_Width(int): It is Actual width of object, in real world (like My face width is = 5.7 Inches)
    :param3 Width_In_Image(int): It is object width in the frame /image in our case in the reference image(found by Face detector)
    :retrun Focal_Length(Float):
    """
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length


# distance estimation function


def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
    """
    This Function simply Estimates the distance between object and camera using arguments(Focal_Length, Actual_object_width, Object_width_in_the_image)
    :param1 Focal_length(float): return by the Focal_Length_Finder function

    :param2 Real_Width(int): It is Actual width of object, in real world (like My face width is = 5.7 Inches)
    :param3 object_Width_Frame(int): width of object in the image(frame in our case, using Video feed)
    :return Distance(float) : distance Estimated

    """
    distance = (real_face_width * Focal_Length) / face_width_in_frame
    return distance


# face detection Fauction


def face_data(image, CallOut, Distance_level):
    """

    This function Detect face and Draw Rectangle and display the distance over Screen

    :param1 Image(Mat): simply the frame
    :param2 Call_Out(bool): If want show Distance and Rectangle on the Screen or not
    :param3 Distance_Level(int): which change the line according the Distance changes(Intractivate)
    :return1  face_width(int): it is width of face in the frame which allow us to calculate the distance and find focal length
    :return2 face(list): length of face and (face paramters)
    :return3 face_center_x: face centroid_x coordinate(x)
    :return4 face_center_y: face centroid_y coordinate(y)

    """

    face_width = 0
    face_x, face_y = 0, 0
    face_center_x = 0
    face_center_y = 0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(
        gray_image, 1.3, 5)  # list of faces coordinates
    #print(faces)
    for (x, y, w, h) in faces:
        line_thickness = 2
        # print(len(faces))
        LLV = int(h * 0.12)
        # print(LLV)

        # cv2.rectangle(image, (x, y), (x+w, y+h), BLACK, 1)
        cv2.line(image, (x, y + LLV), (x + w, y + LLV),
                 (GREEN), line_thickness)
        cv2.line(image, (x, y + h), (x + w, y + h), (GREEN), line_thickness)
        cv2.line(image, (x, y + LLV), (x, y + LLV + LLV),
                 (GREEN), line_thickness)
        cv2.line(
            image, (x + w, y + LLV), (x + w, y +
                                      LLV + LLV), (GREEN), line_thickness
        )
        cv2.line(image, (x, y + h), (x, y + h - LLV), (GREEN), line_thickness)
        cv2.line(image, (x + w, y + h), (x + w, y + h - LLV),
                 (GREEN), line_thickness)

        face_width = w
        face_center = []
        # Drwaing circle at the center of the face
        face_center_x = int(w / 2) + x
        face_center_y = int(h / 2) + y
        if Distance_level < 10:
            Distance_level = 10

        # cv2.circle(image, (face_center_x, face_center_y),5, (255,0,255), 3 )
        if CallOut == True:
            # cv2.line(image, (x,y), (face_center_x,face_center_y ), (155,155,155),1)
            cv2.line(image, (x, y - 11), (x + 180, y - 11), (ORANGE), 28)
            cv2.line(image, (x, y - 11), (x + 180, y - 11), (YELLOW), 20)
            cv2.line(image, (x, y - 11),
                     (x + Distance_level, y - 11), (GREEN), 18)

            # cv2.circle(image, (face_center_x, face_center_y),2, (255,0,255), 1 )
            # cv2.circle(image, (x, y),2, (255,0,255), 1 )

        # face_x = x
        # face_y = y

    return face_width, faces, face_center_x, face_center_y


# reading reference image from directory
ref_image = cv2.imread("../Screenshot 2022-10-25 at 10.00.49 AM.png")

ref_image_face_width, _, _, _ = face_data(ref_image, False, Distance_level)
#ref_image_face_width = 30
Focal_length_found = FocalLength(
    Known_distance, Known_width, ref_image_face_width)
print("Face width of the refrence image", ref_image_face_width)
print("Focal length of the camera", Focal_length_found)

# cv2.imshow("ref_image", ref_image)

while True:
    _, frame = cap.read()
    
    #tf
    image_np_expanded = np.expand_dims(frame, axis=0)
    
    input_tensor = tf.convert_to_tensor(
        np.expand_dims(frame, 0), dtype=tf.float32)
    detections, predictions_dict, shapes = detect_fn(input_tensor)

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                for key, value in detections.items()}
    detections['num_detections'] = num_detections

    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
    
    boxes = detections['detection_boxes']
    scores = detections['detection_scores']
    min_score_thresh=.3
    coordinates = []
    max_boxes_to_draw = 5
    imgout = Image.fromarray(frame, 'RGB')
    
    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        if scores[i] > min_score_thresh:
            class_id = int(detections['detection_classes'][i] + 1)
            box = boxes[i]
            im_height = imgout.height
            im_width = imgout.width
            (ymin, xmin, ymax, xmax) = (box[0] * im_height, box[1] * im_width,
                            box[2] * im_height, box[3] * im_width)
            coordinates.append({
                "box": [int(xmin) , int(ymin) , int(xmax) ,int(ymax)],
                "class_name": category_index[class_id]["name"],
                "score": scores[i]
            })
    
    print(coordinates)
    
    face_width_in_frame, Faces, FC_X, FC_Y = face_data(
        frame, True, Distance_level)
    # finding the distance by calling function Distance finder
    #print(Faces,type(Faces))
    #print(coordinates,type(coordinates))
    for obj in coordinates:
        try:
            face_x, face_y, face_w, face_h = (obj['box'][0],obj['box'][1],obj['box'][2],obj['box'][3])
            #for (face_x, face_y, face_w, face_h) in objTuple:
            if face_width_in_frame != 0:

                Distance = Distance_finder(
                    Focal_length_found, Known_width, face_width_in_frame
                )
                Distance = round(Distance, 2)
                # Drwaing Text on the screen
                Distance_level = int(Distance)

                cv2.putText(
                    frame,
                    f"Distance {Distance} Inches & object is {obj['class_name']}",
                    (face_x - 6, face_y - 6),
                    fonts,
                    0.5,
                    (WHITE),
                    2,
                )
        except IndexError:
            pass
    cv2.imshow("frame", frame)
    # out.write(frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
# out.release()
cv2.destroyAllWindows()
