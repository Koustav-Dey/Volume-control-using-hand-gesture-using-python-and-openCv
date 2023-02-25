import cv2
import time
import numpy as np
import module as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam , hCam = 640,480
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
a = 0

detector = htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volbar = 400
volper = 0



while True:
    _,img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw = False)
    if len(lmList)!= 0:
        # print(lmList[4],lmList[8])/

        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        cx,cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,255,0),2)
        cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        # print(length)

        vol = np.interp(length,[50,300],[minVol,maxVol])
        volbar = np.interp(length,[50,300],[400,150])
        volper = np.interp(length,[50,300],[0,100])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<50:
            cv2.circle(img,(cx,cy),5,(0,240,0),cv2.FILLED)
    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volbar)),(85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img,f'{(int(volper))}%',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(237,130,0),3)

    cTime =time.time()
    a = (cTime - pTime)
    if a == 0:
        a = 0.1
    fps = 1 / a
    pTime = cTime
    cv2.putText(img,f'FPS : {(int(fps))}',(40,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,126),3)

    cv2.imshow("Image",img)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()