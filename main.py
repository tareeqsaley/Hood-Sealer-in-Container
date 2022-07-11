### The purpose of this code is to detect the presence/absence of sealer placed on the hood of a vehicle. This is based on the known regions of interest
### of where that sealer needs to be positioned

### Lead Engineer: Tareeq Saley -  tsaley@toyota.co.za
### Support Engineer 1: Shihal Sapry - ssapry@toyota.co.za
### Support Engineer 2: Jeremy Hammond -  jhammond@toyota.co.za

import cv2
import numpy as np
import time
from datetime import datetime
import globals as g
import keyboard

evt=-1
flip=2
coord = []
white = 250

def click(event,x,y,flags,params): 
    global pnt
    global evt
    if event ==cv2.EVENT_LBUTTONDOWN:
        print('Mouse Event Was: ',event)
        print(x,',',y)
        pnt = (g.x-x,g.y-y)
        coord.append(pnt)
        print(coord) 
        evt = event

cv2.namedWindow('Detection Frame') 
cv2.setMouseCallback('Detection Frame',click) #set a callback for when the mouse is clicked


#cam = cv2.VideoCapture(f'rtsp://admin:Toyota9753@192.168.1.11/2',cv2.CAP_FFMPEG)
cam = cv2.VideoCapture("/home/tareeq/Documents/Hood_Sealer_Container/hood1.mp4")
#greyback = np.zeros((1920,2000,3),np.uint8)
#greyback.fill(125)
#cv2.moveWindow('greyback',0,0)
#cv2.imshow(' ',greyback)

def inPosition():
    return True
    if keyboard.is_pressed('enter'):  # if key 'enter' is pressed 
        return True  
    else:    
        return False

def binarizeFrame(frame):
    
    grayFrame =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh,binarizedFrame = cv2.threshold(grayFrame, 128, 255, cv2.THRESH_OTSU)
    #print(thresh)
    return binarizedFrame

def showFrame(frame, name, resizedW, resizedH, movedX, movedY):
    #croppedFrame = frame[y:y+h,x:x+w].copy()
    resizedFrame= cv2.resize(frame, (resizedW,resizedH))
    cv2.imshow(name,resizedFrame)
    cv2.moveWindow(name,movedX,movedY)

def detectSealer(frame, binFrame):

    sealerCounter = 0
    faultCounter = 0
    i = 0
    for i in range (i,len(g.ROI_POSITIONS),1):
        x,y,w,h =  g.ROI_POSITIONS[i]
        currentROIBinFrame = binFrame[y:y+h,x:x+w]
        #currentROIBinFrame = binarizeFrame(currentROI)
        #cv2.imshow('Current Bin ROI', currentROIBinFrame)
        #print (np.mean(currentROIBinFrame))

        if np.mean(currentROIBinFrame) <= white:
            sealerCounter = sealerCounter + 1
            cv2.rectangle(frame,(x-2,y-2),(x+2+w, y+2+h),(0,255,0),2)
        else:
            faultCounter = faultCounter + 1
            cv2.rectangle(frame,(x-2,y-2),(x+2+w, y+2+h),(0,0,255),2)

    return sealerCounter, faultCounter


def evaluateSealer(sCounter,fCounter,frame):
    
    if (sCounter in g.SEALER_DERIVATIVE_COUNT) and (fCounter==0):
        #print(scounter)

        frame = cv2.copyMakeBorder(frame, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value =  [0,255,0])
    else:
        frame = cv2.copyMakeBorder(frame, 20, 20, 20, 20, cv2.BORDER_CONSTANT,  value =  [0,0,255]) 

    return frame


while True:

    ret,frame = cam.read()
    showFrame(frame,'Continuous Frame',900,1000,0,0)

    for pnts in coord:
        cv2.circle(frame,pnts,5,(0,0,255),-1)
        myStr = str(pnts)
        font = cv2.FONT_HERSHEY_PLAIN
        #print(pnts)
        cv2.putText(frame,myStr,pnts,font,1,(255,0,100),2)

    if inPosition():
        binFrame = binarizeFrame(frame)
       # showFrame(binFrame,'Binarized Frame',970,1000,0,0)
        sealerCounter, faultCounter = detectSealer(frame,binFrame)
        finalFrame = evaluateSealer(sealerCounter, faultCounter ,frame)
        showFrame(finalFrame,'Detection Frame',950,1000,970,0)


    if cv2.waitKey(1)==ord('q'):
        break


cam.release()
cv2.destroyAllWindows()

    
