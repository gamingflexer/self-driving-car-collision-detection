import cv2
from constants import *
from detection import *

from utils import face_data,Distance_finder

"""MOTOR CODE"""

import RPi.GPIO as GPIO          
from time import sleep

in1 = 23
in2 = 24
en1 = 25

in3 = 27
in4 = 22
en2 = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p1 = GPIO.PWM(en1,1000)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p2 = GPIO.PWM(en2,1000)

p1.start(0)
p2.start(0)



"""MOTOR CODE"""


DEBUG = False

fonts = cv2.FONT_HERSHEY_COMPLEX
fonts2 = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
fonts3 = cv2.FONT_HERSHEY_COMPLEX_SMALL
fonts4 = cv2.FONT_HERSHEY_TRIPLEX
# Camera Object
cap_left = cv2.VideoCapture(0)  # Number According to your Camera

Distance_level = 0

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"XVID")

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
    return (width_in_rf_image * measured_distance) / real_width


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
        motor_started_left = False
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
            
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            p1.ChangeDutyCycle(75)
            x = 'z'
            motor_started_left = True
            
        if motor_started_left:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW)
            p1.ChangeDutyCycle(0)
            p2.ChangeDutyCycle(0)
            x = 'z'
            
    cv2.imshow("frame", frame)
    #out.write(frame)

    if cv2.waitKey(1) == ord("q"):
        break

if DEBUG:
    cap_right = cv2.VideoCapture(1)  
    cap_back = cv2.VideoCapture(2)  

    while True:
        _, frame = cap_right.read()
        # calling face_data function
        # Distance_leve =0
        
        coordinates = yolo_object_detection(frame)
        face_width_in_frame, Faces, FC_X, FC_Y = face_data(frame, True, Distance_level)
        for obj in coordinates:
            
            motor_started_right = False
            
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
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                p2.ChangeDutyCycle(75)
                x = 'z'
                motor_started_right = True
                
            if motor_started_right:
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW)
                p1.ChangeDutyCycle(0)
                p2.ChangeDutyCycle(0)
                x = 'z'
                
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
            
            motor_started_back = False
            
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
                
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                p1.ChangeDutyCycle(75)
                p2.ChangeDutyCycle(75)
                x = 'z'
                motor_started_back = True
                
            if motor_started_back:
                #stop the motor
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW)
                p1.ChangeDutyCycle(0)
                p2.ChangeDutyCycle(0)
                x = 'z'
                
        cv2.imshow("frame", frame)
        #out.write(frame)

        if cv2.waitKey(1) == ord("q"):
            break
    cap_right.release()
    cap_back.release()

cap_left.release()
# out.release()
cv2.destroyAllWindows()