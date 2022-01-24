import cv2

#cap = cv2.VideoCapture(0)

def getImg(display = False, size= (480,240)):
    cap = cv2.VideoCapture(0)
    _,img = cap.read()
    #img = cv2.resize(img,(224,224),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
    img = cv2.resize(img,size)
    if display:
        cv2.imshow('IMAGE', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return img

if __name__ == "__main__":
    while True:
        img = getImg(True)
       # cv2.resize(img,(img.size[0],img.size[1]))