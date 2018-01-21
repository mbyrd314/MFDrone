import cv2
import numpy as np
import matplotlib.pyplot as plt

#Begin video feed
cap = cv2.VideoCapture(0)


ret, frame = cap.read()
hsv_template = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
plt.imshow(hsv_template)
plt.show()

#if cv2.waitKey(0) & 0xFF == ord('c'):
#    x = raw_input()
#    y = raw_input()

#hue, saturation, value = hsv_template[y,x,:]
#print("HUE: %d /t Saturation: %d /t Value: %d" %(hue, saturation,value))

while True:
    #Filter frame
    ret, frame = cap.read()
    frame = cv2.medianBlur(frame,5)
    gframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Convert BGR to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    #define color range to be detectted
    lower_val = np.array([100,100,50])
    upper_val= np.array([120,170,255])

    #Threshold HSV to get color of interest
    mask = cv2.inRange(hsv, lower_val, upper_val)

    #Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask = mask)

    gres = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    #Identify circles
    circles = cv2.HoughCircles(gres,cv2.HOUGH_GRADIENT,1,minDist=20,param1=50,param2=30,minRadius=20,maxRadius=0)
    if circles is not None:
        circles = np.uint16(np.around(circles))

        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)

        #cv2.imshow('image 3', frame)

    cv2.imshow('mask', mask)
    cv2.imshow('video feed', frame)
    #quit using q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
