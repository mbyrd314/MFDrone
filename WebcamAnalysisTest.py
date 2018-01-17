import cv2
import numpy as np

cap = cv2.VideoCapture(0)

#Save video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

while True:
    #get frames from camera
    ret, frame = cap.read()             #returns T/F for ret and frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #save frame
    out.write(frame)

    #show video on screen
    cv2.imshow('frame',frame)
    cv2.imshow('gray', gray)

    #quit when q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
