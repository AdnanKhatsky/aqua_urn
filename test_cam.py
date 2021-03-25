import numpy as np
import cv2
camera = cv2.VideoCapture(0)while(True):
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('frame', frame)
    cv2.imshow('gray', gray)
    if cv2.waitKey(27) & 0xFF:
        breakcap.release()
cv2.destroyAllWindows()