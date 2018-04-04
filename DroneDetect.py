import cv2
import numpy as np
#import matplotlib.pyplot as plt
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import io

def circle_detect():

#Initializing Camera with resolution of 640 * 480
	camera = PiCamera()
	camera.resolution = (640,480)
	center_x = 320
	center_y = 240
	camera.framerate = 32
	rawCapture = PiRGBArray(camera, size=(640,480))

#To set new HSV range uncomment and determine color
	#frame = camera.capture(rawCapture, format='bgr')
	#plt.imshow(frame)
	#plt.show()


	time.sleep(2)

#Begin video feed capture	
	for cap in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		frame= cap.array

	    #Filter image by blurring using average of 5 pixels
		frame = cv2.medianBlur(frame,5)

		#Convert to Grayscale
		gframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	    #Convert BGR to HSV
		hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

	    #Define threshold HSV color range to be detected
		lower_val = np.array([170, 140, 0])
		upper_val = np.array([180, 255, 255])
		mask = cv2.inRange(hsv, lower_val, upper_val)

	    #Bitwise-AND mask and original image
		res = cv2.bitwise_and(frame, frame, mask = mask)

		#Recombine with gray sclae image
		gres = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

	    #Identify circles
		circles = cv2.HoughCircles(gres,cv2.cv.CV_HOUGH_GRADIENT,1,minDist=200,param1=50,param2=20,minRadius=10,maxRadius=0)

		if circles is not None:
			circles = np.uint16(np.around(circles))
			zmotion = 0
			
		#Only check first circle detected
			i= circles[0,0]
	    	# draw the outer circle
			cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
	    	# draw the center of the circle
			cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
			
			#Create tolerance value function to determine center of circle
			tolerance = 1/(i[2]) * 300
			
			#Determine which direction drone should move based on location of center of circle to center of image
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
				 
		#Optional image display
		#cv2.imshow('mask', mask)
		#cv2.imshow('video feed', frame)
		#cv2.imshow('masked image', gres)
		
		#Optional image saving
		#cv2.imwrite('mask.png', mask)
		#cv2.imwrite('graymask.png', gres)
		#cv2.imwrite('original.png', frame)

	    #quit using q if using image display
		#if cv2.waitKey(1) & 0xFF == ord('q'):
			#break

		rawCapture.truncate(0)
   
	cv2.destroyAllWindows()

if __name__ == '__main__':
	try:
		circle_detect()
	finally:
		print("User ended function")
