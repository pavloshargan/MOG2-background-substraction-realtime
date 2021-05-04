import cv2
from ring_buffer import RingBuffer
import threading
import time


FROM_CAMERA = False

if not FROM_CAMERA:
    source = "./record.avi"
else:
    source = 0
cap = cv2.VideoCapture(source)

FRAME_BUFFER_SIZE = 15
frame_buffer = RingBuffer(FRAME_BUFFER_SIZE)

fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold = 70, detectShadows = False)

def read_frames():
    count=0
    start = time.time()
    while(cap.isOpened()):
        #append frame to circular buffer
        ret, frame = cap.read()
        frame_buffer.append(frame)
        if not FROM_CAMERA:
            time.sleep(0.03) #limit speed of reading to like 33 FPS as we read from recorded file
        count+=1
        #check fps
        if count==FRAME_BUFFER_SIZE:
            result = time.time()-start
            print("FPS: ", FRAME_BUFFER_SIZE/result)
            # print("fps {}", 10/result)
            start = time.time()
            count=0

def process_buffer():
    while(True):
        if not frame_buffer.is_full():
            continue
        mask = fgbg.apply(frame_buffer.get_first())
        for frame in frame_buffer.get_sorted()[1::]:
            mask =  mask + fgbg.apply(frame)

        cv2.imshow("mask", mask)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            cv2.destroyAllWindows()
            sys.exit()

frames_collecting = threading.Thread(target=read_frames, daemon=True)
frames_processing = threading.Thread(target=process_buffer, daemon=True)


frames_collecting.start()
frames_processing.start()

frames_collecting.join()
frames_processing.join()
