import cv2
from constants import *
from YoloV4.detection import *

fonts = cv2.FONT_HERSHEY_COMPLEX
fonts2 = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
fonts3 = cv2.FONT_HERSHEY_COMPLEX_SMALL
fonts4 = cv2.FONT_HERSHEY_TRIPLEX
# Camera Object
cap_left = cv2.VideoCapture(0)  # Number According to your Camera
cap_right = cv2.VideoCapture(1)  
cap_back = cv2.VideoCapture(2)  
Distance_level = 0

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"XVID")
# out = cv2.VideoWriter("output21.mp4", fourcc, 30.0, (640, 480))

# face detector object
face_detector = cv2.CascadeClassifier("../python/models/haarcascade_frontalface_default.xml")
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


# reading reference image from directory
ref_image = cv2.imread("../om.png")

ref_image_face_width, _, _, _ = face_data(ref_image, False, Distance_level)
#ref_image_face_width = 30
Focal_length_found = FocalLength(Known_distance, Known_width, ref_image_face_width)
print("Face width of the refrence image",ref_image_face_width)
print("Focal length of the camera",Focal_length_found)

# cv2.imshow("ref_image", ref_image)

"""CAMERA FUNCTIONS"""

while True:
    _, frame = cap_left.read()
    # calling face_data function
    # Distance_leve =0
    
    coordinates = yolo_object_detection(frame)
    face_width_in_frame, Faces, FC_X, FC_Y = face_data(frame, True, Distance_level)
    for obj in coordinates:
        face_x, face_y, face_w, face_h = tuple(list(obj.values())[0])
        
        # finding the distance by calling function Distance finder
        if face_width_in_frame != 0:

            Distance = Distance_finder(
                Focal_length_found, Known_width, face_width_in_frame
            )
            Distance = round(Distance, 2)
            # Drwaing Text on the screen
            Distance_level = int(Distance)

            cv2.putText(
                frame,
                f"Distance {Distance} Inches & object is {list(obj.keys())[0]}",
                (face_x - 6, face_y - 6),
                fonts,
                0.5,
                (BLACK),
                2,
            )
    cv2.imshow("frame", frame)
    #out.write(frame)

    if cv2.waitKey(1) == ord("q"):
        break

while True:
    _, frame = cap_right.read()
    # calling face_data function
    # Distance_leve =0
    
    coordinates = yolo_object_detection(frame)
    face_width_in_frame, Faces, FC_X, FC_Y = face_data(frame, True, Distance_level)
    for obj in coordinates:
        face_x, face_y, face_w, face_h = tuple(list(obj.values())[0])
        
        # finding the distance by calling function Distance finder
        if face_width_in_frame != 0:

            Distance = Distance_finder(
                Focal_length_found, Known_width, face_width_in_frame
            )
            Distance = round(Distance, 2)
            # Drwaing Text on the screen
            Distance_level = int(Distance)

            cv2.putText(
                frame,
                f"Distance {Distance} Inches & object is {list(obj.keys())[0]}",
                (face_x - 6, face_y - 6),
                fonts,
                0.5,
                (BLACK),
                2,
            )
    cv2.imshow("frame", frame)
    #out.write(frame)

    if cv2.waitKey(1) == ord("q"):
        break
    
while True:
    _, frame = cap_back.read()
    # calling face_data function
    # Distance_leve =0
    
    coordinates = yolo_object_detection(frame)
    face_width_in_frame, Faces, FC_X, FC_Y = face_data(frame, True, Distance_level)
    for obj in coordinates:
        face_x, face_y, face_w, face_h = tuple(list(obj.values())[0])
        
        # finding the distance by calling function Distance finder
        if face_width_in_frame != 0:

            Distance = Distance_finder(
                Focal_length_found, Known_width, face_width_in_frame
            )
            Distance = round(Distance, 2)
            # Drwaing Text on the screen
            Distance_level = int(Distance)

            cv2.putText(
                frame,
                f"Distance {Distance} Inches & object is {list(obj.keys())[0]}",
                (face_x - 6, face_y - 6),
                fonts,
                0.5,
                (BLACK),
                2,
            )
    cv2.imshow("frame", frame)
    #out.write(frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap_left.release()
cap_right.release()
cap_back.release()
# out.release()
cv2.destroyAllWindows()