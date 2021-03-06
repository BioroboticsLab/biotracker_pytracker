from biotracker import (
    Signals,
    Button,
    Text,
    Slider,
    run_client)
import numpy as np

Mat = None


def track(frame, M):
    global Mat
    Mat = np.absolute(M - 50) 
    Signals.notify_gui("track" + str(frame) + str(Mat.shape))


def paint(frame):
    global Mat
    Signals.notify_gui("paint")
    if Mat is not None:
        return Mat


def paint_overlay(qpainter):
    Signals.notify_gui("paint overlay")
    qpainter.setPen(255, 255, 0, 255)
    qpainter.drawRect((20, 20, 60, 60))


def shutdown():
    Signals.notify_gui("shutdown")


def btn_click():
    Signals.notify_gui("button click")


def btn2_click():
    Signals.notify_gui("button2 click")

def slider_changed(value):
    Signals.notify_gui("slider changed " + str(value))

def request_widgets():
    return [
        Button("ClickMe", btn_click),
        Button("ClickMeToo", btn2_click),
        Slider("Slide me", 0, 100, 25, slider_changed),
        Text("Funny text:")]

run_client(
    track,
    paint,
    paint_overlay,
    shutdown,
    request_widgets=request_widgets)
