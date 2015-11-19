import zmq
from enum import Enum
import numpy as np
import time


class MessageTypes(Enum):
    track = 1
    paint = 2


def _start():
    port = "5556"
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:%s" % port)
    time.sleep(1)
    return socket


def send_str(m):
    socket = _start()
    socket.send_string(m)

def send_paint(frame):
    socket = _start()
    print("paint")


def send_track(frame, mat):
    socket = _start()
    socket.send_string("hello")
    print("track")

