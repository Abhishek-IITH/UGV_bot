from picamera.array import PiRGBArray
import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import cv2
import numpy as np
import math
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(7, GPIO.OUT)
#GPIO.setup(8, GPIO.OUT)

IN1 = 16
IN2 = 20
IN3 = 21
IN4 = 26
servoPIN = 17
speed_control1 = 13
speed_control2 = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.setup(servoPIN, GPIO.OUT)

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(speed_control1, GPIO.OUT)
GPIO.setup(speed_control2, GPIO.OUT)
s1 = GPIO.PWM(speed_control1, 490)
s2 = GPIO.PWM(speed_control2, 490)
s1.start(30)
s2.start(30)


def fwd():
    GPIO.output(IN1,0)
    GPIO.output(IN2,1)
    GPIO.output(IN3,0)
    GPIO.output(IN4,1)

def stp():
    GPIO.output(IN1,0)
    GPIO.output(IN2,0)
    GPIO.output(IN3,0)
    GPIO.output(IN4,0)


def rt():
    GPIO.output(IN1,0)
    GPIO.output(IN2,1)
    GPIO.output(IN3,1)
    GPIO.output(IN4,0)

def lt():
    GPIO.output(IN1,1)
    GPIO.output(IN2,0)
    GPIO.output(IN3,0)
    GPIO.output(IN4,1)

def bck():
    GPIO.output(IN1,1)
    GPIO.output(IN2,0)
    GPIO.output(IN3,1)
    GPIO.output(IN4,0)
    
theta=0
minLineLength = 5
maxLineGap = 10
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)   
    
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
   image = frame.array
   gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   #ret,gray = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
   gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
   blurred = cv2.GaussianBlur(gray, (5, 5), 0)
   edged = cv2.Canny(blurred, 85, 85)
   lines = cv2.HoughLinesP(edged,1,np.pi/180,10,minLineLength,maxLineGap)
   #print(type(lines))
   try:
       line_len = len(lines)
       if(line_len !=None):
           for x in range(0, line_len):
               for x1,y1,x2,y2 in lines[x]:
                   cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
                   theta=theta+math.atan2((y2-y1),(x2-x1))
       #print(theta)GPIO pins were connected to arduino for servo steering control
       threshold=6
       if(theta>threshold):
           #GPIO.output(7,True)
           #GPIO.output(8,False)
           print("left")
           lt()
       if(theta<-threshold):
           #GPIO.output(8,True)
           #GPIO.output(7,False)
           print("right")
           rt()
       if(abs(theta)<threshold):
          #GPIO.output(8,False)
         # GPIO.output(7,False)
          print("straight")
          fwd()
       time.sleep(0.05) 
   except:
       stp()
       print("stop")
   theta=0
   cv2.imshow("Frame",image)
   key = cv2.waitKey(1) & 0xFF
   rawCapture.truncate(0)
   if key == ord("q"):
       break