import zmq
import biotracker
import time


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
    w = str(mat.shape[0])
    h = str(mat.shape[1])
    try:
        channels = mat.shape[2]
    except:
        channels = 1
    mtype = str(
        biotracker.dtype_to_mtype(mat.dtype, channels)
    )
    shape = w + "," + h + "," + mtype
    socket.send_string(shape)
    print("track")

