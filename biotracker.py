import zmq
import numpy as np

socket = None


def start():
    global socket
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect("tcp://localhost:5556")



class QPainter:
    content = ""

    def to_msg(self):
        return self.content

    def setPen(self, col):
        (r, g, b, a) = col
        if len(self.content) > 0:
            self.content += ";"
        self.content += "p(" + str(r) + "," + str(g) + "," + str(b) + ',' + str(a) + ")"

    def drawRect(self, rec):
        (x, y, w, h) = rec
        if len(self.content) > 0:
            self.content += ";"
        self.content += "r(" + str(x) + "," + str(y) + "," + str(w) + "," + str(h) + ")"


def send_painter(p):
    socket.send_string(p.to_msg())


def rec_str():
    m = socket.recv_string()
    return m


def recv_mat():
    print("rec mat")
    mat_dim = socket.recv_string()
    shape = mat_dim.split(",")
    w = int(shape[0])
    h = int(shape[1])
    mtype = int(shape[2])
    mat_data = socket.recv()
    return _reshape(mat_data, w, h, mtype)


def run_client(track_fun, paint_fun):
    if not hasattr(track_fun, '__call__'):
        return ""


def dtype_to_mtype(dtype, channels):
    """
    http://ninghang.blogspot.de/2012/11/list-of-mat-type-in-opencv.html
    :param dtype:
    :return:
    """
    mtype = -1
    if dtype == np.uint8:
        mtype = 0
    elif dtype == np.int8:
        mtype = 1
    elif dtype == np.uint16:
        mtype = 2
    elif dtype == np.int16:
        mtype = 3
    elif dtype == np.int32:
        mtype = 4
    elif dtype == np.float32:
        mtype = 5
    elif dtype == np.float64:
        mtype = 6
    else:
        raise Exception("dtype " + str(dtype) + " not supported")

    if channels < 1 or channels > 4:
        raise Exception("number of channels must be between 1 .. 4")

    return mtype + ((channels - 1) * 8)


def _reshape(mat_data, w, h, mtype):
    """
    M {MATRIX}
    w {width}
        h {height}
    mtype {matrix type}
    """
    mod = mtype % 8
    dtype = np.int8
    if mod == 0:
        dtype = np.uint8
    elif mod == 1:
        dtype = np.int8
    elif mod == 2:
        dtype = np.uint16
    elif mod == 3:
        dtype = np.int16
    elif mod == 4:
        dtype = int
    elif mod == 5:
        dtype = np.float32
    elif mod == 6:
        dtype = np.float64
    else:
        raise Exception("Invalid integer type" + str(type))

    div = mtype // 8
    channels = 1
    if div == 0:
        channels = 1
    elif div == 1:
        channels = 2
    elif div == 2:
        channels = 3
    elif div == 3:
        channels = 4
    else:
        raise Exception("Wrong number of channels:" + str(channels))

    buf = memoryview(mat_data)
    M = np.frombuffer(buf, dtype=dtype)
    return np.reshape(M, (w, h, channels))
