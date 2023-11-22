import cv2
import mediapipe as mp
import time

cap=cv2.VideoCapture(0)


mphands=mp.solutions.hands  # for accesing hands detection in mediapipe
hands=mphands.Hands()   #extracting hands

mpDraw=mp.solutions.drawing_utils  #it contain utitilities to Draw the hand landmarks


ptime=0 #previous time
ctime=0 # current time
while True:
    success, img=cap.read()
    img=cv2.flip(img,1)
    imgrgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #Mediapipe uses rgb format
    results=hands.process(imgrgb)   #here process to take hands on rgb format

    print(results.multi_hand_landmarks)


    if results.multi_hand_landmarks:
        for handlandmarks in results.multi_hand_landmarks:
            for id,lm in enumerate(handlandmarks.landmark):
                print(id,lm) #landmarks lm is an ratio in format of x,y,z
                h,w,c=img.shape #getting height ,width
                cx,cy=int(lm.x*w),int(lm.y*h) #taking pixels no. by multiplyiing with height and width
                cv2.putText(img, str(int(id)), (cx,cy), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2) #taking circle on detected landmarks

            mpDraw.draw_landmarks(img,handlandmarks,mphands.HAND_CONNECTIONS)  #given handlandmarks and use connection to draw

    #for Getting FPS
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3)
    #fps end


    cv2.imshow("Win", img)
    cv2.waitKey(1)