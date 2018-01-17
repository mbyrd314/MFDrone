import cv2
import numpy as np
import matplotlib.pyplot as plt

template = cv2.imread('pillow.jpg', 1)
img = cv2.imread('pillowdetect.jpg', 1)

orb = cv2.ORB_create()

#save keypoints
kp1, des1 = orb.detectAndCompute(template,None)
kp2, des2 = orb.detectAndCompute(img,None)

#create bfmatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

matches = bf.match(des1,des2)
matched = sorted(matches, key = lambda x:x.distance)

img3 = cv2.drawMatches(template, kp1, img, kp2, matches[:2], None, flags=2)
cv2.imshow('image 3', img3)
#plt.show()
cv2.waitKey(0)
