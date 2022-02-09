from cvzone.HandTrackingModule import HandDetector
from pickle import PicklingError
import cv2
import mediapipe
import serial

drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector = HandDetector(detectionCon=0.8, maxHands=2)
frameWidth = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

try:
        ser = serial.Serial("COM9", 9600)
        print("Robot Connected ")
except:
        print("Not Connected To Robot ")
        pass
 
def sendData(fingers):

    string = "$"+str(int(fingers[0]))+str(int(fingers[1]))+str(int(fingers[2]))+str(int(fingers[3]))+str(int(fingers[4]))
    try:
       ser.write(string.encode())
       print(string)
       print 
    except:
        pass

with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:
    numt=0   
    numr=0   
    numm=0   
    numi=0   
    nump=0   
    while (True):
 
        ret, frame = capture.read()
 
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
       
        success, img = capture.read()
        hand,img= detector.findHands(img)
        if hand:
            handType1 = hand[0]["type"]
            print(handType1)
 
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                for point in handsModule.HandLandmark:
 
                    normalizedLandmark = handLandmarks.landmark[point]
                    pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, frameWidth, frameHeight)
                    #print(point)
                    #print(pixelCoordinatesLandmark)
                    #print(normalizedLandmark)
                    cv2.circle(frame, pixelCoordinatesLandmark, 5, (0, 255, 0), -1)
 
            pinkytip = handLandmarks.landmark[20]
            pinkytipcoors = drawingModule._normalized_to_pixel_coordinates(pinkytip.x, pinkytip.y, frameWidth, frameHeight)
            #print("pinky_tip")
            #print(pinkytip)
            #print(pinkytipcoors)
            
            ringtip = handLandmarks.landmark[16]
            ringtipcoors = drawingModule._normalized_to_pixel_coordinates(ringtip.x, ringtip.y, frameWidth, frameHeight)
            #print("ring_tip")
            #print(ringtip)
            #print(ringtipcoors)
            
            middletip = handLandmarks.landmark[12]
            middletipcoors = drawingModule._normalized_to_pixel_coordinates(middletip.x, middletip.y, frameWidth, frameHeight)
            #print("middle_tip")
            #print(middletip)
            #print(middletipcoors)
            
            thumbtip = handLandmarks.landmark[4]
            thumbtipcoors = drawingModule._normalized_to_pixel_coordinates(thumbtip.x, thumbtip.y, frameWidth, frameHeight)
            #print("thumb_tip")
            #print(thumbtip)
            #print(thumbtipcoors)

            indextip = handLandmarks.landmark[8]
            indextipcoors = drawingModule._normalized_to_pixel_coordinates(indextip.x, indextip.y, frameWidth, frameHeight)
            #print("index_tip")
            #print(indextip)
            #print(indextipcoors)

#-----------#------------------------------------------------
            pinkyjoint = handLandmarks.landmark[17]
            pinkyjointcoors = drawingModule._normalized_to_pixel_coordinates(pinkyjoint.x, pinkyjoint.y, frameWidth, frameHeight)
            #print("pinky_joint")
            #print(pinkyjoint)
            #print(pinkyjointcoors)
            #
            ringjoint = handLandmarks.landmark[13]
            ringjointcoors = drawingModule._normalized_to_pixel_coordinates(ringjoint.x, ringjoint.y, frameWidth, frameHeight)
            #print("ring_joint")
            #print(ringjoint)
            #print(ringjointcoors)
            #
            middlejoint = handLandmarks.landmark[9]
            middlejointcoors = drawingModule._normalized_to_pixel_coordinates(middlejoint.x, middlejoint.y, frameWidth, frameHeight)
            #print("middle_joint")
            #print(middlejoint)
            #print(middlejointcoors)
            #
            thumbjoint = handLandmarks.landmark[5]
            thumbjoint1 = handLandmarks.landmark[0]
            thumbjointcoors = drawingModule._normalized_to_pixel_coordinates(thumbjoint.x, thumbjoint.y, frameWidth, frameHeight)
            #print("thumb_joint")
            #print(thumbjoint)
            #print(thumbjointcoors)
#
            indexjoint = handLandmarks.landmark[5]
            indexjointcoors = drawingModule._normalized_to_pixel_coordinates(indexjoint.x, indexjoint.y, frameWidth, frameHeight)
            #print("index_joint")
            #print(indexjoint)
            #print(indexjointcoors)

            #print(f"joint {indexjoint.y}" )
            #print(f"tip {indextip.y} ")
            
            ij = indexjoint.y
            it = indextip.y
            
            mj = middlejoint.y
            mt = middletip.y
            
            rj = ringjoint.y
            rt = ringtip.y
            
            pj = pinkyjoint.y
            pt = pinkytip.y

            tj = thumbjoint.x
            tj1 = thumbjoint1.x
            tt = thumbtip.x
            
            if ij >= it:
                #print(f"i{numi}")
                numi+=1
                iif = True
            else: 
                iif = False
            
            if mj <= mt:
                #print(f"m{numm}")
                numm+=1
                mif = True
            else: 
                mif = False
            
            if rj <= rt:
                #print(f"r{numr}")
                numr+=1
                rif = True
            else: 
                rif = False
            
            if pj <= pt:
                #print(f"p{nump}")
                nump+=1
                pif = True
            else: 
                pif = False

            if handType1 == "Right":
                if ((tj1+tj)/2) <= tt:
                    #print(f"t{numt}")
                    numt+=1 
                    tif = True
                else: 
                    tif = False
            elif handType1 == "Left":
                if ((tj1+tj)/2) >= tt:
                    #print(f"t{numt}")
                    numt+=1 
                    tif = True
                else: 
                    tif = False
                
                #p, r, m, i, t
            if   (    pif and         rif and         mif and     iif and     tif):sendData([1, 1, 1, 1, 1]);FingerCount="Five"
            elif (    pif and         rif and         mif and     iif and not tif):sendData([1, 1, 1, 1, 0]);FingerCount="Four"
            elif (    pif and         rif and         mif and not iif and     tif):sendData([1, 1, 1, 0, 1]);FingerCount="Three"
            elif (    pif and         rif and         mif and not iif and not tif):sendData([1, 1, 1, 0, 0]);FingerCount="Three"
            elif (    pif and         rif and     not mif and     iif and     tif):sendData([1, 1, 0, 1, 1]);FingerCount="four"
            elif (    pif and         rif and     not mif and     iif and not tif):sendData([1, 1, 0, 1, 0]);FingerCount="Three"
            elif (    pif and         rif and     not mif and not iif and     tif):sendData([1, 1, 0, 0, 1]);FingerCount="Three"
            elif (    pif and         rif and     not mif and not iif and not tif):sendData([1, 1, 0, 0, 0]);FingerCount="Two"
            elif (    pif and     not rif and         mif and     iif and     tif):sendData([1, 0, 1, 1, 1]);FingerCount="four"
            elif (    pif and     not rif and         mif and     iif and not tif):sendData([1, 0, 1, 1, 0]);FingerCount="Three"
            elif (    pif and     not rif and         mif and not iif and     tif):sendData([1, 0, 1, 0, 1]);FingerCount="Three"
            elif (    pif and     not rif and         mif and not iif and not tif):sendData([1, 0, 1, 0, 0]);FingerCount="Two"
            elif (    pif and     not rif and     not mif and     iif and     tif):sendData([1, 0, 0, 1, 1]);FingerCount="Three"
            elif (    pif and     not rif and     not mif and     iif and not tif):sendData([1, 0, 0, 1, 0]);FingerCount="Two"
            elif (    pif and     not rif and     not mif and not iif and     tif):sendData([1, 0, 0, 0, 1]);FingerCount="Two"
            elif (    pif and     not rif and     not mif and not iif and not tif):sendData([1, 0, 0, 0, 0]);FingerCount="one"
            elif (not pif and         rif and         mif and     iif and     tif):sendData([0, 1, 1, 1, 1]);FingerCount="four"
            elif (not pif and         rif and         mif and     iif and not tif):sendData([0, 1, 1, 1, 0]);FingerCount="Three"
            elif (not pif and         rif and         mif and not iif and     tif):sendData([0, 1, 1, 0, 1]);FingerCount="Three"
            elif (not pif and         rif and         mif and not iif and not tif):sendData([0, 1, 1, 0, 0]);FingerCount="Two"
            elif (not pif and         rif and     not mif and     iif and     tif):sendData([0, 1, 0, 1, 1]);FingerCount="Three"
            elif (not pif and         rif and     not mif and     iif and not tif):sendData([0, 1, 0, 1, 0]);FingerCount="Two" 
            elif (not pif and         rif and     not mif and not iif and     tif):sendData([0, 1, 0, 0, 1]);FingerCount="Two"
            elif (not pif and         rif and     not mif and not iif and not tif):sendData([0, 1, 0, 0, 0]);FingerCount="one"
            elif (not pif and     not rif and         mif and     iif and     tif):sendData([0, 0, 1, 1, 1]);FingerCount="three"
            elif (not pif and     not rif and         mif and     iif and not tif):sendData([0, 0, 1, 1, 0]);FingerCount="Two"
            elif (not pif and     not rif and         mif and not iif and     tif):sendData([0, 0, 1, 0, 1]);FingerCount="Two"
            elif (not pif and     not rif and         mif and not iif and not tif):sendData([0, 0, 1, 0, 0]);FingerCount="one"
            elif (not pif and     not rif and     not mif and     iif and     tif):sendData([0, 0, 0, 1, 1]);FingerCount="Two"
            elif (not pif and     not rif and     not mif and     iif and not tif):sendData([0, 0, 0, 1, 0]);FingerCount="one"
            elif (not pif and     not rif and     not mif and not iif and     tif):sendData([0, 0, 0, 0, 1]);FingerCount="one"
            elif (not pif and     not rif and     not mif and not iif and not tif):sendData([0, 0, 0, 0, 0]);FingerCount="zero"
            else:sendData([0, 0, 0, 0, 0]);FingerCount="zero"

        cv2.imshow('hanD', frame)
 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
cv2.destroyAllWindows()
capture.release()