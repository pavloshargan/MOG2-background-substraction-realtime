import cv2
from ring_buffer import RingBuffer
import threading
import time
import numpy as np

#you can play with threshold
fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold = 70, detectShadows = False)

source = "./record.avi"
cap = cv2.VideoCapture(source)

while(cap.isOpened()):
    ret, frame = cap.read()
    mask = fgbg.apply(frame)
    #you can play with postprocessing (erosion and dilation)
    kernel_e = np.ones((2,2),np.uint8)  
    kernel_d = np.ones((8,8),np.uint8)  
    erosion = cv2.erode(mask,kernel_e,iterations = 1)
    dilation = cv2.dilate(erosion,kernel_d,iterations = 1)
    ret, thresh = cv2.threshold(dilation, 127, 255, 0)
    cv2.imshow("mask", thresh)
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        cv2.destroyAllWindows()
        sys.exit()

       