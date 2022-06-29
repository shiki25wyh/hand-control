
import cv2
import mediapipe as mp
import time
import module as m
import math
import numpy as np
import autopy
import pyautogui
import platform
if platform.system() == 'Windows':
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    minVol,maxVol = -65.25,0
elif platform.system() == 'Darwin':
    import osascript
    
    minVol,maxVol = 0,100
else:
    pass



vol = 0
volBar = 400
volPer = 0


wScr,hScr = autopy.screen.size()
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
detector = m.handDetector(maxHands=1,detectionCon=0.5)

margin = 100
smooth = 5
locx, locy = 0,0
clocx, clocy = 0,0
is_release_left = 0
is_release_right = 0
is_release = 0
action = ''
try:
    while True:
        last_time = time.time()
        ret,frame = cap.read()
        frame = cv2.flip(frame,1)
        frame,handness = detector.findHands(frame)
        lmList,bbox = detector.position(frame)

        ############################################################# mouse ########################################################################
        cv2.rectangle(frame,(margin,margin),(640-margin,490-margin),(255,255,0),2)
        if len(lmList)!=0 and lmList[15][2]<lmList[16][2] and lmList[19][2]<lmList[20][2]:
            

            if (handness[0].classification[0].index == 0 and lmList[4][1]<lmList[2][1]) or (handness[0].classification[0].index == 1 and lmList[4][1]>lmList[2][1]):
                x1,y1 = lmList[4][1:]
                
                x3 = np.interp(x1,(margin,640-margin),(0,wScr))
                y3 = np.interp(y1,(margin,480-margin),(0,hScr))
                clocx = locx + (x3-locx)/smooth
                clocy = locy + (y3-locy)/smooth


                autopy.mouse.move(clocx,clocy)  
                locx,locy = clocx, clocy
                # print(x3,y3)
                length,frame,lineinfo = detector.distance(8,12,frame)
                # if(length>50 and is_release == 0 and (lmList[8][1]-lmList[7][1])<-1 ):
                    
                #     is_release = 1
                #     action = 'double left click'
                #     pyautogui.click(clicks=2,button='left')

                # elif(length<=50 and is_release == 1):
                #     is_release = 0
                #     action = ''
                    

                if (lmList[8][2]>lmList[7][2] and lmList[12][2]>lmList[11][2] and is_release_left == 0) :
                    is_release_left = 1
                    # autopy.mouse.click()
                    pyautogui.click(clicks=1,button='left')
                    action = 'left click'
                    
                elif (length>50  and is_release_right == 0) :
                    # autopy.mouse.click(button=RIGHT_BUTTON)
                    is_release_right = 1
                    action = 'right click'
                    
                    pyautogui.click(button='right')
                elif (lmList[8][2]<lmList[7][2] and lmList[12][2]<lmList[11][2] and is_release_left == 1) :
                    is_release_left = 0
                    action = ''
                    
                elif (length<=50 and is_release_right == 1) :
                    # autopy.mouse.click(button=RIGHT_BUTTON)
                    is_release_right = 0
                    action = ''
                    
                else:
                    pass

        


        ################################################################# vloume ########################################################################
        elif len(lmList)!=0 and lmList[9][2]<lmList[12][2] and lmList[13][2]<lmList[16][2] and lmList[17][2]<lmList[20][2]:
            if (handness[0].classification[0].index == 0 and lmList[4][1]>lmList[3][1]) or (handness[0].classification[0].index == 1 and lmList[4][1]<lmList[3][1]):
                # print(lmList[8][2],lmList[12][2])
                # print(handness[0].classification[0].index)
            # if lmList[12]<lmList[8]
            # print(area)
            # print(lm_list[4],lm_list[8])
        
                length,frame,lineinfo = detector.distance(4,8,frame)
                cx,cy=lineinfo[4],lineinfo[5]
                # print(length)
                # volRange = 0-100
                # lenRange = 50,350
                vol = np.interp(length,[50,150],[minVol,maxVol]).astype(int)
                volBar = np.interp(length,[50,150],[400,150]).astype(int)
                volPer = np.interp(length,[50,150],(0,100)).astype(int)
                # print (volBar)
                if platform.system() == 'Darwin':
                    
                    osascript.osascript("set volume output volume {}".format(vol))
                elif platform.system() == 'Windows':
                    volume.SetMasterVolumeLevel(vol, None)

                if length<50:
                    cv2.circle(frame,(cx,cy),15,(0,255,0),cv2.FILLED)
    
        cv2.rectangle(frame,(50,150),(85,400),(0,255,0),3)
        cv2.rectangle(frame,(50,volBar),(85,400),(0,255,0),cv2.FILLED)
        cv2.putText(frame,f'{volPer}%',(40,450),cv2.FONT_ITALIC,1,(0,255,0),3)
        cv2.putText(frame,action,(20,50),cv2.FONT_ITALIC,1,(0,255,0),3)

    



        fps = 1/(time.time()-last_time)
        cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)




        cv2.imshow('window',frame)



        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
except:
    pass


cap.release()
cv2.destroyAllWindows()