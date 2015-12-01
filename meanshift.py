import numpy as np
import cv2
import biotracker

Mat = None

term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
roi_hist = None
r, h, c, w = 260, 90, 470, 165
track_window = (c, r, w, h)


def track(frame, M):
    global Mat, roi_hist, track_window
    Mat = M

    if frame == 0:
        # calculate the Histo
        roi = M[r:r+h, c:c+w]
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
    else:
        if Mat is not None:
            hsv = cv2.cvtColor(Mat, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
            ret, track_window = cv2.meanShift(dst, track_window, term_crit)
        pass


def paint(frame):
    pass


def paint_overlay(qpainter):
    global track_window
    qpainter.setPen(255, 0, 0)
    x = track_window[1]
    y = track_window[0]
    w = track_window[2]
    h = track_window[3]
    qpainter.drawRect((x, y, w, h))


def shutdown():
    pass

biotracker.run_client(track, paint, paint_overlay, shutdown)