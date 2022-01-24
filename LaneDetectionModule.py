import cv2
import numpy as np
import utils
from timeit import default_timer

curveList = []
AvgVal = 10  #user defined

def getLaneCurve(img,display = 2):
    imgCopy = img.copy()
    #step 1
    img_thres = utils.thresholding(img)
    
    #step 2
    hT,wT,c  = img.shape
    points = utils.valTrackbars()
    imgWarp = utils.warpImg(img_thres,points,wT,hT)
    imgWarpPoints = utils.drawPoints(imgCopy,points)
    
    #step 3
    mid_point, imgHist = utils.getHistogram(imgWarp,display = True, minPer = 0.5)#region = 4)
    curveAvgPoint, imgHist = utils.getHistogram(imgWarp,display = True, minPer = 0.9)
    curveRaw = curveAvgPoint - mid_point
    
    #step 4
    curveList.append(curveRaw)
    if len(curveList) > AvgVal:
        curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))
    imgResult = 0
    #step 5
    if display != 0:
       imgInvWarp = utils.warpImg(imgWarp, points, wT, hT)#inv = True)
       imgInvWarp = cv2.cvtColor(imgInvWarp,cv2.COLOR_GRAY2BGR)
       imgInvWarp[0:hT//3,0:wT] = 0,0,0
       imgLaneColor = np.zeros_like(img)
       imgLaneColor[:] = 0, 255, 0
       imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
       imgResult = cv2.addWeighted(imgResult,1,imgLaneColor,1,0)
       midY = 450
       cv2.putText(imgResult,str(curve),(wT//2-80,85),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)
       cv2.line(imgResult,(wT//2,midY),(wT//2+(curve*3),midY),(255,0,255),5)
       cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY-25), (wT // 2 + (curve * 3), midY+25), (0, 255, 0), 5)
       for x in range(-30, 30):
           w = wT // 20
           cv2.line(imgResult, (w * x + int(curve//50 ), midY-10),
                    (w * x + int(curve//50 ), midY+10), (0, 0, 255), 2)
       fps = cv2.getTickFrequency() / (cv2.getTickCount() - default_timer());
       cv2.putText(imgResult, 'FPS '+str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230,50,50), 3);
    if display == 2:
        imgStacked = utils.stackImages(0.7,([img,imgWarpPoints,imgWarp],
                                         [imgHist,imgLaneColor,imgResult]))
        cv2.imshow('ImageStack',imgStacked)
    elif display == 1:
        cv2.imshow('Resutlt',imgResult)
    
    #Normalization 
    curve = curve/100
    if curve > 1:
        curve == 1
    if curve < -1:
        curve == -1
    '''
    cv2.imshow('Threshold_image',img_thres)
    cv2.imshow('Warped Image',imgWarp)
    cv2.imshow('Warp points',imgWarpPoints)
    ''' 
    return curve
    
'''
def getImg(display = False, size=[480,240]):
    cap = cv2.VideoCapture(0)
    _, img = cap.read() 
    img = cv2.resize(img,(size[0],size[1]))
    if display:
        cv2.imshow('IMAGE',img)
    return img
'''

        

if __name__ == '__main__':
    
    cap = cv2.VideoCapture(0)
    initialTracbarVals  = [100,100,100,100]
    utils.initializeTrackbars(initialTracbarVals)
    frameCounter = 0
    while True:
        frameCounter +=1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) ==frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            frameCounter=0
 
        success, img = cap.read()
        img = cv2.resize(img,(640,480))
        curve = getLaneCurve(img,display = 1)
        print(curve)
        cv2.imshow('Results',img)
        cv2.waitKey(1)