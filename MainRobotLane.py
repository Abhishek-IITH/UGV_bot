from MotorModule import Motor
import utils
from LaneDetectionModule import getLaneCurve
import webCamModule
import cv2

motor = Motor(2,17,3,4,22,27) 

def main():
    img = webCamModule.getImg()
    print("I am here")
    curveVal = getLaneCurve(img,2)
    sen = 1.3  #sensitivity
    maxVal = 0.3 #maxspeed
    if curveVal > maxVal:
        curveVal = maxVal
    if curveVal < -maxVal:
        curveVal = -maxVal
    
    if curveVal > 0:
        sen = 1.7
        if curveVal < 0.05:
            curveVal = 0
    else:
        if curveVal > -0.08:
            curveVal = 0
    motor.move(0.20,-curveVal*sen,0.05)
    cv2.waitKey(1)
    
    
if __name__=="__main__":
    initialTracbarVals  = [100,100,100,100]
    utils.initializeTrackbars(initialTracbarVals)
    while True:
        main()
        