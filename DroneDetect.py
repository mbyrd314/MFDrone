import cv2
import numpy as np
#import matplotlib.pyplot as plt
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import io
#import gtk


def circle_detect():
	#cv2.dilate(img,kernel)
	#cv2.erode(img,kernel)

	#print('Before instantiating camera')
	camera = PiCamera()
	camera.resolution = (640,480)
	center_x = 320
	center_y = 240
	camera.framerate = 32
	rawCapture = PiRGBArray(camera, size=(640,480))

	#print('After instantiating camera')

	#frame = camera.capture(rawCapture, format='bgr')

	#plt.imshow(frame)
	#plt.show()


	time.sleep(2)
	#Begin video feed
	for cap in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	    frame= cap.array
	    #print('After capturing image')
	#hue, saturation, value = hsv_template[y,x,:]
	#print("HUE: %d /t Saturation: %d /t Value: %d" %(hue, saturation,value))
	#frame = cv2.imread("circle2.jpg",1)
	#frame = cv2.resize(frame,dsize=(0,0), fx = .5, fy = .5)  
	#for x in range(1):
	    #Filter frame
	    #frame = cv2.imread("circle2.jpg",1)
	    #frame = cv2.resize(frame,dsize=(0,0),fx = .5, fy = .5)  
	    frame = cv2.medianBlur(frame,5)
	    #print('After blur')
	    gframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	    #Convert BGR to HSV
	    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	   # plt.imshow(hsv, cmap = "hsv")
	    #plt.show()   
	    #define color range to be detectted
	    #lower_val = np.array([100,70,0])
	    #upper_val= np.array([120,255,255])
	    lower_val = np.array([170, 140, 0])
	    upper_val = np.array([180, 255, 255])
	    #Threshold HSV to get color of interest
	    mask = cv2.inRange(hsv, lower_val, upper_val)

	    #Bitwise-AND mask and original image
	    res = cv2.bitwise_and(frame, frame, mask = mask)

	    gres = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

	    #Identify circles
	    circles = cv2.HoughCircles(gres,cv2.cv.CV_HOUGH_GRADIENT,1,minDist=200,param1=50,param2=20,minRadius=10,maxRadius=0)
	    if circles is not None:
		circles = np.uint16(np.around(circles))

		for i in circles[0,:]:
		    # draw the outer circle
		    cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
		    # draw the center of the circle
		    cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)

		zmotion = 0
		tolerance = 1/(i[2]) * 200
	
		if i[0] < (center_x - tolerance):
			print('Move Left')
			zmotion = 0
		elif i[0] > (center_x + tolerance):
			print('Move Right')
			zmotion = 0
		else:
			print('Hover')
			zmotion = 1
	        
		if i[1] < (center_y - tolerance):
			print('Move backward')
		elif i[1] >( center_y + tolerance):
			print('Move forward')
		else:
			print("Hover")
	        if zmotion == 1:
			print("Move up in the z direction")
	         



		#cv2.imshow('image 3', frame)

	    #print('Before imshow')
	    #cv2.imshow('mask', mask)
	    cv2.imshow('video feed', frame)
	    #cv2.imshow('masked image', gres)
	    #print('After imshow')
	    #quit using q
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	       break
	    rawCapture.truncate(0)
	    #print('End of while loop')
	    
	cv2.destroyAllWindows()

if __name__ == '__main__':
	try:
		circle_detect()
	finally:
		print("User ended function")
