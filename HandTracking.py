import cv2
import mediapipe as mp
import time 

cap = cv2.VideoCapture(0)


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    last_time = time.time()

    ret, frame = cap.read()
    frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = hands.process(frameRGB)
    # print(results.multi_hand_landmarks)
    

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id, lm in enumerate(handlms.landmark):
                # print(id,lm)
                h,w,c = frame.shape
                cx, cy = int(lm.x*w),int(lm.y*h)
                print(id,cx,cy)

            mpDraw.draw_landmarks(frame,handlms,mpHands.HAND_CONNECTIONS)

    fps = 1/(time.time()-last_time)
    cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)


    cv2.imshow('window',frame)



    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

