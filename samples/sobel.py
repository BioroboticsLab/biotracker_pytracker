from biotracker import (
    Signals,
    Button,
    run_client
)
import numpy as np
from scipy import signal

Mat = None
Kx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
Ky = Kx.T
show_x = True


def track(frame, M):
    global Mat, Kx, Ky, show_x
    if show_x:
        Mat = signal.convolve2d(M, Kx, boundary='symm', mode='same')
    else:
        Mat = signal.convolve2d(M, Ky, boundary='symm', mode='same')


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
