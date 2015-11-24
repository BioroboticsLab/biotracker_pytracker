import biotracker
import numpy as np

Mat = None


def track(frame, M):
    global Mat
    Mat = np.absolute(M - 50) 
    print("track " + str(frame) + str(Mat.shape))


def paint(qpainter, frame):
    global Mat
    print("paint " + str(frame))
    qpainter.setPen((255, 255, 0, 255))
    qpainter.drawRect((20, 20, 60, 60))
    if Mat is not None:
        return Mat



def shutdown():
    print("shutdown")

biotracker.run_client(track, paint, shutdown)
