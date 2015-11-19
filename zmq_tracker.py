import biotracker
import numpy as np

print("start")

print("start zmq client")

x = 0
y = 1
w = 1
h = 1


def track(frame, M):
    print("track")


def paint(frame):
    print("paint")

#while True:
#    print("wait for next mat")
#    M = biotracker.recv_mat()
#
#    N = np.zeros_like(M)
#    N[(M >= 200).nonzero()] = 255
#
#    print("matrix:" + str(M[400][402]))
#
#    p = biotracker.QPainter()
#    p.setPen((0, 0, 255, 255))
#    p.drawRect((x, y, w, h))
#
#    biotracker.send_painter(p)
