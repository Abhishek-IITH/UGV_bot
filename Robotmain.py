from MotorModule import Motor
import KeypressModule as kp
import cv2
import webCamModule
#import LaneDetection
#import pygame

def liveVideo():
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        img = cv2.resize(img,(640,480))
        cv2.imshow('Results',img)
        
        if kp.getKey('UP'):
            print('forward')
            motor.move(0.6,0,0.1)
        elif kp.getKey('DOWN'):
            print('down')
            motor.move(-0.6,0,0.1)
            
        elif kp.getKey('LEFT'):
            print('left')
            motor.move(0.5,0.3,0.1)
            
        elif kp.getKey('RIGHT'):
            print('right')
            motor.move(0.5,-0.3,0.1)
            
        else:
            motor.stop(0.1)
            #print('Stop')
            
    
        cv2.waitKey(1)

def init():
    pygame.init()
    window = pygame.display.set_mode((100,100))

#########
motor = Motor(2,17,3,4,22,27)  #RPi pin configuration
########
kp.init()

def main():
    img = webCamModule.getImg(True)

    
def main1():
    main()
    print('function call')
    
    if kp.getKey('UP'):
        print('forward')
        motor.move(0.6,0,0.1)
        main()
    elif kp.getKey('DOWN'):
        motor.move(-0.6,0,0.1)
        main()
    elif kp.getKey('LEFT'):
        motor.move(0.5,0.3,0.1)
        main()
    elif kp.getKey('RIGHT'):
        motor.move(0.5,-0.3,0.1)
        main()
    else:
        motor.stop(0.1)
        main()
      
#import PiLiveVideo
if __name__ == '__main__':
    #while True:
    liveVideo()
        
        #main1()
        #main()
        
    
    
