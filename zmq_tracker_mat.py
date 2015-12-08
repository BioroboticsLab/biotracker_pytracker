import biotracker
import numpy as np

Mat = None


def track(frame, M):
    global Mat
    Mat = np.absolute(M - 50) 
    print("track " + str(frame) + str(Mat.shape))


def paint(frame):
    global Mat
    print("paint " + str(frame))
    if Mat is not None:
        return Mat


def paint_overlay(qpainter):
    print("paint overlay")
    qpainter.setPen(255, 255, 0, 255)
    qpainter.drawRect((20, 20, 60, 60))


def shutdown():
    print("shutdown")


def btn_click():
    print("button click")


def request_widgets():
    print("request widgets")
    return [biotracker.Button("ClickMe", btn_click)]


biotracker.run_client(
    track,
    paint,
    paint_overlay,
    shutdown,
    request_widgets=request_widgets )
