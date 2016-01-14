from biotracker import (
    Signals,
    Button,
    run_client
)
import numpy as np
from scipy import signal, ndimage

Mat = None
Kx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
Ky = Kx.T
show_x = True


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])


def track(frame, M):
    global Mat, Kx, Ky, show_x
    M = rgb2gray(M)
    if show_x:
        Mat = ndimage.sobel(M, 0)
    else:
        Mat = ndimage.sobel(M, 1)


def paint(frame):
    global Mat
    return Mat


def paint_overlay(qpainter):
    pass


def toggle_xy():
    global show_x
    show_x = not show_x


def request_widgets():
    return [
        Button("Toggle X/Y", toggle_xy())
    ]


def shutdown():
    pass


run_client(
    track,
    paint,
    paint_overlay,
    shutdown,
    request_widgets=request_widgets)
