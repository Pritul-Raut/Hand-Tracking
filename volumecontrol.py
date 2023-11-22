import cv2
import mediapipe as mp
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap=cv2.VideoCapture(0)


#Audio controls
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volPer = 0
area = 0
colorVol = (255, 0, 0)


mphands=mp.solutions.hands  # for accesing hands detection in mediapipe
hands=mphands.Hands()   #extracting hands

mpDraw=mp.solutions.drawing_utils  #it contain utitilities to Draw the hand landmarks



while True:
    success, img=cap.read()
    img=cv2.flip(img,1)
    imgrgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #Mediapipe uses rgb format
    results=hands.process(imgrgb)   #here process to take hands on rgb format

    print(results.multi_hand_landmarks)


    if results.multi_hand_landmarks:
        lm_list = []

        for handlandmarks in results.multi_hand_landmarks:



            for id,lm in enumerate(handlandmarks.landmark):
                #print(id,lm) #landmarks lm is an ratio in format of x,y,z
                h,w,c=img.shape #getting height ,width


                cx,cy=int(lm.x*w),int(lm.y*h) #taking pixels no. by multiplyiing with height and width
                cv2.putText(img, str(int(id)), (cx,cy), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2) #taking circle on detected landmarks
                lm_list.append([id,cx,cy])











            x1, y1 = lm_list[4][1], lm_list[4][2]
            x2, y2 = lm_list[8][1], lm_list[8][2]
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.circle(img, (x1,y1), 10, (0, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2,y2), 10, (255, 255, 255), cv2.FILLED)


            mcx,mcy=(x2+x1)//2,(y2+y1)//2
            cv2.circle(img, (mcx, mcy), 8, (150, 150, 155), cv2.FILLED)

            length=math.hypot(x2-x1,y2-y1)

            vol=np.interp(length,[50,200],[minVol,maxVol])

            volPer=np.interp(length,[50,200],[0,100])

            print(length,vol)
            volume.SetMasterVolumeLevel(vol,None)


            cv2.putText(img,f'Volume : {int(volPer)}%',(100,400),cv2.FONT_HERSHEY_PLAIN,4,(0,255,0),4)

            mpDraw.draw_landmarks(img,handlandmarks,mphands.HAND_CONNECTIONS)  #given handlandmarks and use connection to draw

            if int(volPer)==0:
                cv2.putText(img, f'MUTE', (200, 250), cv2.FONT_HERSHEY_PLAIN, 5, (0,0 ,255), 5)
                cv2.circle(img, (mcx, mcy), 15, (0, 0, 255), cv2.FILLED)

            if int(volPer)==100:
                cv2.putText(img, f'FULL', (200, 250), cv2.FONT_HERSHEY_PLAIN, 5, (0,0 ,255), 5)
                cv2.circle(img, (mcx, mcy), 15, (0, 255, 0), cv2.FILLED)



    cv2.imshow("Win", img)
    cv2.waitKey(1)