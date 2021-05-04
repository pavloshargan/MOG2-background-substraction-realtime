import cv2
from ring_buffer import RingBuffer
import threading

fgbg = cv2.cuda.createBackgroundSubtractorMOG2(varThreshold = 70, detectShadows = False)


source = "./record.avi"
cap = cv2.VideoCapture(source)

FRAME_BUFFER_SIZE = 15
frame_buffer = RingBuffer(FRAME_BUFFER_SIZE)


def read_frames():
    count=0
    start = time.time()
    while(cap.isOpened()):
        #append frame to circular buffer
        ret, frame = cap.read()
        frame_buffer.append(frame)
        count+=1
        #check fps
        if count==BUFFER_SIZE:
            result = time.time()-start
            print("FPS: ", BUFFER_SIZE/result)
            # print("fps {}", 10/result)
            start = time.time()
            count=0

def process_buffer():
    stream = cv2.cuda_Stream()
    frame_cuda = cv2.cuda_GpuMat()
    frame_cuda.upload(custom_buffer.get_first(), stream)
    foreground_mask_cuda = fgbg.apply(frame_cuda,-1,cv2.cuda.Stream_Null())
    for frame in frame_buffer.get_sorted()[1::]:
        frame_cuda.upload(frame, stream)
        added =  cv2.cuda.bitwise_or(foreground_mask_cuda, fgbg.apply(frame_cuda,-1,stream))
        foreground_mask_cuda = added

    foreground_mask = foreground_mask_cuda.download(stream)
    stream.waitForCompletion()
    cv2.imshow("mask", foreground_mask)
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
