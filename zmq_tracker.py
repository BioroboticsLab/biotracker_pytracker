import biotracker
import numpy as np

Mat = None


def track(frame, M):
    global Mat
    if M is not None:
        Mat = np.absolute(M - 50) 
        print("track " + str(frame) + str(Mat.shape))


def paint(frame):
    global Mat
    print("paint " + str(frame))


def paint_overlay(qpainter):
    qpainter.setPen(255, 255, 0, 255)
    qpainter.drawRect((20, 20, 60, 60))

def shutdown():
    print("shutdown")

def request_widgets():
    return []

biotracker.run_client(
    track,
    paint,
    paint_overlay,
    shutdown)
