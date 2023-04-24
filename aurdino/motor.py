# Python Script
# https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

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

print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("L-run first motor R-run second motor M-run both motors S-stop E-exit")
print("\n")

while(1):

    x = raw_input()
    
    if x == 'L':
        print("Running first motor")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        p1.ChangeDutyCycle(75)
        x = 'z'

    elif x == 'R':
        print("Running second motor")
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        p2.ChangeDutyCycle(75)
        x = 'z'

    elif x == 'M':
        print("Running both motors")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        p1.ChangeDutyCycle(75)
        p2.ChangeDutyCycle(75)
        x = 'z'

    elif x == 'S':
        print("Stopping both motors")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        p1.ChangeDutyCycle(0)
        p2.ChangeDutyCycle(0)
        x = 'z'

    elif x == 'E':
        GPIO.cleanup()
        print("GPIO Clean up")
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
