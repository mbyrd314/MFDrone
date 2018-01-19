import cv2
import numpy as np

#Begin video feed
cap = cv2.VideoCapture(0)

#Resize template
template = cv2.imread('DroneDesign.jpeg', 0)
template= cv2.resize(template, (0,0), fx =.05, fy =.05)


#creating feature detection object
orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(template,None)

while True:
    #Filter frame and change to grayscale
    ret, frame = cap.read()
    frame = cv2.medianBlur(frame,5)
    gframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Identify circles
    circles = cv2.HoughCircles(gframe,cv2.HOUGH_GRADIENT,1,minDist=2000,param1=60,param2=35,minRadius=0,maxRadius=0)
    if circles is not None:
        circles = np.uint16(np.around(circles))

        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)

            #cv2.imshow('detected circles',frame)

            #define region of interest as square of side length 2r
            x,y,radius = i[0],i[1],i[2]
            roi_frame = frame[y-radius: y+radius, x-radius:x+radius]
            roi_gframe = gframe[y-radius: y+radius, x-radius:x+radius]

            #Create bf matcher
            kp2, des2 = orb.detectAndCompute(gframe,None)
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = False)

            #determine matches and sort
            matches = bf.match(des1,des2)
            matched = sorted(matches, key = lambda x:x.distance)
            frame = cv2.drawMatches(template, kp1, frame, kp2, matches[:2], None, flags=2)
        #display image with circle detection and feature match
        cv2.imshow('image 3', frame)

    #quit using q    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
