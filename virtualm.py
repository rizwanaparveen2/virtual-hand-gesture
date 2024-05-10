import cv2
import numpy as nm
import autopy
import handtrack as ht
import time
import pyautogui
wcam, hcam =640,480
frameR = 95
plocx,plocy = 0,0
clocx,clocy = 0,0
smoothning = 7
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
pTime = 0            
detector = ht.handDetector(maxHands=1)
wscr,hscr = autopy.screen.size()
print(wscr,hscr)
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    if len(lmList)!=0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        fingers = detector.fingerUp()
        #print(fingers)
        cv2.rectangle(img, (frameR, frameR), ((wcam - frameR), (hcam - frameR)), (255, 23, 14), 2)
        if fingers[1]==1 and fingers[2]==0:
            #print("click")
            x3 = nm.interp(x1,(frameR,wcam-frameR),(0,1536))
            y3 = nm.interp(y1,(frameR,hcam-frameR),(0,864))
            clocx = plocx + (x3-plocx)/ smoothning
            clocy = plocy + (y3-plocy)/ smoothning
            autopy.mouse.move(wscr-x3,y3)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocx, plocy = clocx, clocy
        if fingers[1] == 1 and fingers[2] == 1:
            length,img, lineInfo = detector.findDistance(8,12,img)
            print(length)
            if length<39:
                cv2.circle(img,(lineInfo[4],lineInfo[5]),15,(0,255,0),cv2.FILLED)
                autopy.mouse.click()
        if fingers[1] == 1 and fingers[2]==0 and fingers[4] == 1 :
            autopy.mouse.click(autopy.mouse.Button.RIGHT)
            cv2.waitKey(800)
        if fingers[3]==1 and fingers[1]==0 and fingers[2]==0 and fingers[0]==0 and fingers[4]==0:
            pyautogui.scroll(100)
        if fingers[0]==1 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
            pyautogui.scroll(-100)


            


    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow("Image",img)
    cv2.waitKey(1)

