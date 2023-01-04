from cvzone.HandTrackingModule import HandDetector
import cv2
from djitellopy import Tello

global imgContour
global rotate
global Positionx
global Positiony
global Positionz

rotate=0
Positionx=0
Positiony=0
Positionz=0

startCounter =1

# CONNECT TO TELLO
me = Tello()
#me.connect()
me.for_back_velocity = 0
me.left_right_velocity = 0
me.up_down_velocity = 0
me.yaw_velocity = 0
me.speed = 0

#me.streamoff()
#me.streamon()

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
success, img = cap.read()
h, w, _ = img.shape
detector = HandDetector(detectionCon=0.8, maxHands=2)
state=[0,0,0,0,0]

######################################################################
deadZone =150
frameWidth = w
frameHeight = h
######################################################################

def display(img):
    cv2.line(img,(int(frameWidth/2)-deadZone,0),(int(frameWidth/2)-deadZone,frameHeight),(255,255,0),3)
    cv2.line(img,(int(frameWidth/2)+deadZone,0),(int(frameWidth/2)+deadZone,frameHeight),(255,255,0),3)
    cv2.circle(img,(int(frameWidth/2),int(frameHeight/2)),5,(0,0,255),5)
    cv2.line(img, (0,int(frameHeight / 2) - deadZone), (frameWidth,int(frameHeight / 2) - deadZone), (255, 255, 0), 3)
    cv2.line(img, (0, int(frameHeight / 2) + deadZone), (frameWidth, int(frameHeight / 2) + deadZone), (255, 255, 0), 3)

def getContours1(x,y):
            global rotate
            global Positionx
            global Positiony
            global Positionz
            if (int(x) <int(frameWidth/2)-deadZone):
                cv2.putText(imgContour, " GO LEFT " , (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(0,int(frameHeight/2-deadZone)),(int(frameWidth/2)-deadZone,int(frameHeight/2)+deadZone),(0,0,255),cv2.FILLED)
                Positionx=-20
                Positionz=0
                rotate=0
                Positiony=0

            elif (int(x) > int(frameWidth / 2) + deadZone):
                cv2.putText(imgContour, " GO RIGHT ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(int(frameWidth/2+deadZone),int(frameHeight/2-deadZone)),(frameWidth,int(frameHeight/2)+deadZone),(0,0,255),cv2.FILLED)
                Positionx=20
                Positionz=0
                rotate=0
                Positiony=0

            elif (int(y) < int(frameHeight / 2) - deadZone):
                cv2.putText(imgContour, " GO FORWARD ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(int(frameWidth/2-deadZone),0),(int(frameWidth/2+deadZone),int(frameHeight/2)-deadZone),(0,0,255),cv2.FILLED)
                Positiony=20
                Positionz=0
                rotate=0
                Positionx=0

            elif (int(y) > int(frameHeight / 2) + deadZone):
                cv2.putText(imgContour, " GO BACK ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(int(frameWidth/2-deadZone),int(frameHeight/2)+deadZone),(int(frameWidth/2+deadZone),frameHeight),(0,0,255),cv2.FILLED)
                Positiony=-20
                Positionz=0
                rotate=0
                Positionx=0

            else:
                Positionx=0
                Positiony=0
                Positionz=0
                rotate=0

def getContours2(x,y):
            global rotate
            global Positionx
            global Positiony
            global Positionz
            if (int(x) <int(frameWidth/2)-deadZone):
                cv2.putText(imgContour, " TURN LEFT " , (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(0,int(frameHeight/2-deadZone)),(int(frameWidth/2)-deadZone,int(frameHeight/2)+deadZone),(0,0,255),cv2.FILLED)
                rotate=-20
                Positionz=0
                Positionx=0
                Positiony=0
                 
            elif (int(x) > int(frameWidth / 2) + deadZone):
                cv2.putText(imgContour, " TURN RIGHT ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(int(frameWidth/2+deadZone),int(frameHeight/2-deadZone)),(frameWidth,int(frameHeight/2)+deadZone),(0,0,255),cv2.FILLED)
                rotate=20
                Positionz=0
                Positionx=0
                Positiony=0

            elif (int(y) < int(frameHeight / 2) - deadZone):
                cv2.putText(imgContour, " GO UP ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(int(frameWidth/2-deadZone),0),(int(frameWidth/2+deadZone),int(frameHeight/2)-deadZone),(0,0,255),cv2.FILLED)
                Positionz=20
                rotate=0
                Positionx=0
                Positiony=0

            elif (int(y) > int(frameHeight / 2) + deadZone):
                cv2.putText(imgContour, " GO DOWN ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 0, 255), 3)
                cv2.rectangle(imgContour,(int(frameWidth/2-deadZone),int(frameHeight/2)+deadZone),(int(frameWidth/2+deadZone),frameHeight),(0,0,255),cv2.FILLED)
                Positionz=-20
                rotate=0
                Positionx=0
                Positiony=0
            else:
                Positionz=0
                rotate=0
                Positionx=0
                Positiony=0


while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw

    if startCounter == 0:
       me.takeoff()
       startCounter = 1
    
    imgContour = img.copy()
    data = []
    
    display(imgContour)
    
    if hands:
        # Hand 1
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 Landmark points
        state=detector.fingersUp(hand)
        if state == [0,1,0,0,0]:
            getContours1(lmList[0][0],lmList[0][1])
        
        elif state == [1,0,0,0,0]:
            getContours2(lmList[0][0],lmList[0][1])
        else:
            me.for_back_velocity = 0
            me.left_right_velocity = 0
            me.up_down_velocity = 0
            me.yaw_velocity = 0
            me.speed = 0

    me.yaw_velocity = rotate
    me.up_down_velocity= Positionz
    me.left_right_velocity = Positionx 
    me.for_back_velocity = Positiony
   # SEND VELOCITY VALUES TO TELLO
    if me.send_rc_control:
       me.send_rc_control(me.left_right_velocity, me.for_back_velocity, me.up_down_velocity, me.yaw_velocity)
    # Display
    cv2.imshow("Image", imgContour)
    cv2.waitKey(1)
    if cv2.waitKey(5) & 0xFF == 27:
      break




