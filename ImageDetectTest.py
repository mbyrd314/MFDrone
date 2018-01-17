import cv2                                      #BGR
import numpy as np
import matplotlib.pyplot as plt                 #RGB
#This program opens an iage and displays it. Image is closed when key is pressed
#define image
img= cv2.imread('watch.jpg', cv2.IMREAD_GRAYSCALE)                  #IMREAD_COLOR = 1
                                                                    #IMREAD_UNCHANGED = -1
cv2.imshow('image 1', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.plot([50,100], [80,100],'c', linewidth=5)
plt.show()

cv2.imwrite('graywatch.png', img)
