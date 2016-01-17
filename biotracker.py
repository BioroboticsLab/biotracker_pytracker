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

    def setPen(self, r=0, g=0, b=0, a=255):
        #(r, g, b, a) = col
        if len(self.content) > 0:
            self.content += ";"
        self.content += "p(" + str(r) + "," + str(g) + "," + str(b) + ',' + str(a) + ")"

    def drawRect(self, rec):
        (x, y, w, h) = rec
        if len(self.content) > 0:
            self.content += ";"
        self.content += "r(" + str(x) + "," + str(y) + "," + str(w) + "," + str(h) + ")"


def id_generator():
    """
    generates a unique id for the widgets
    :return: {id}
    """
    i = 0
    while True:
        i += 1
        yield i

id_gen = id_generator()


class Widget:
    """

    """
    id = -1

    def __init__(self):
        self.id = next(id_gen)

    def to_msg(self):
        raise Exception("Not implemented")


class Divider(Widget):
    def to_msg(self):
        return "d()"


class Text(Widget):
    text = ""
    type = "t"

    def __init__(self, text):
        super().__init__()
        self.text = text

    def to_msg(self):
        return self.type + "(" + str(self.id) + "," + str(self.text) + ")"


class Button(Text):
    callback = None,

    def __init__(self, text, callback):
        super().__init__(text)
        self.callback = callback
        self.type = "b"


class Slider(Widget):
    text = ""
    callback = None
    min = 0
    max = 255
    default = 100

    def __init__(self, text, minv, maxv, default, callback):
        super().__init__()
        self.text = text
        self.callback = callback
        self.min = minv
        self.max = maxv
        self.default = default
    
    def to_msg(self):
        return "s(" + str(self.id) + "," +\
            str(self.text) + "," +\
            str(self.min) + "," +\
            str(self.max) + "," +\
            str(self.default) + ")"

MSG_TYPE_NOTIFICATION = "0"
MSG_TYPE_WARNING = "1"
MSG_TYPE_FAIL = "2"
MSG_TYPE_FILE_OPEN = "3"


class Helper:

    @staticmethod
    def rgb2gray(rgb):
        return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

class Signals:
    """
    represents the signals that a Tracker can send to the BioTracker GUI
    """

    @staticmethod
    def notify_gui(message, type=MSG_TYPE_NOTIFICATION):
        global socket
        message = message.replace(",", "%2C").replace(";", "%3B")
        socket.send_string("0," + message + "," + type)

    @staticmethod
    def update():
        global socket
        socket.send_string("1")

    @staticmethod
    def force_tracking():
        global socket
        socket.send_string("2")

    @staticmethod
    def jump_to_frame(frame_number):
        global socket
        socket.send_string("3," + str(int(frame_number)))

    @staticmethod
    def pause_playback(paused):
        global socket
        data = "4,"
        if paused:
            data += "1"
        else:
            data += "0"
        socket.send_string(data)

    @staticmethod
    def stop_listening():
        global socket
        socket.send_string("99")

    @staticmethod
    def register_views(views):
        raise Exception("not implemented")


def run_client(on_track, on_paint, on_paintOverlay, on_shutdown, keep_running=None, request_widgets=None):
    """

    :param on_track:
    :param on_paint:
    :param on_paintOverlay:
    :param on_shutdown:
    :param keep_running:
    :param request_widgets:
    """
    if not hasattr(on_track, '__call__'):
        raise Exception("on_track must be a function")
    if not hasattr(on_paintOverlay, '__call__'):
        raise Exception("on_paintOverlay must be a function")
    if not hasattr(on_paint, '__call__'):
        raise Exception("on_paint must be a function")
    if not hasattr(on_shutdown, '__call__'):
        raise Exception("on_shutdown must be a function")
    if keep_running is not None and not hasattr(keep_running, '__call__'):
        raise Exception("keep_running must be a function")
    if request_widgets is not None and not hasattr(request_widgets, '__call__'):
        raise Exception("request_widgets must be a function")

    event_cache = dict()
    widget_str = ''
    if request_widgets is not None:
        widget_list = request_widgets()
        for widget in widget_list:
            key = str(widget.id)
            if key in event_cache:
                raise Exception("duplicate key:" + key)
            if hasattr(widget, 'callback'):
                event_cache[key] = widget.callback
            if len(widget_str) > 0:
                widget_str += ";"
            widget_str += widget.to_msg()

    global socket
    if socket is None:
        start()
    is_running = True
    qpainter = QPainter()
    while is_running:
        msg_type = socket.recv_string()
        if msg_type == "0":  # track
            frame, M = recv_mat()
            on_track(frame, M)
            Signals.stop_listening()  # stop busy wait at server
        elif msg_type == "1":  # paint
            frame = recv_paint()
            M = on_paint(frame)
            Signals.stop_listening()  # stop busy wait at server
            if M is None:
                socket.send_string("N")
            else:  # send matrix back
                socket.send_string("Y", flags=zmq.SNDMORE)
                send_mat(M)
        elif msg_type == "2":  # shutdown
            on_shutdown()
            Signals.stop_listening()
            is_running = False
        elif msg_type == "3":  # paintOverlay
            on_paintOverlay(qpainter)
            Signals.stop_listening()
            socket.send_string(qpainter.to_msg())
            qpainter.content = ""
        elif msg_type == "4":  # request widgets
            Signals.stop_listening()
            socket.send_string(widget_str)
        elif msg_type == "5":  # update widget
            events = socket.recv_string().split(',')
            event_type = events[0]
            widget_id = events[1]
            if widget_id in event_cache:
                if event_type == "0":  # click event
                    event_cache[widget_id]()
                elif event_type == "1":  # value changed
                    event_cache[widget_id](int(events[2]))
                else:
                    raise Exception("Unknown event type " + event_type)
            else:
                raise Exception("cannot find callback for widget id " + widget_id)
            Signals.stop_listening()
        else:
            raise Exception("could not determine type:" + msg_type)

        if keep_running is not None:
            is_running = keep_running(msg_type)


def send_mat(M):
    """

    :param M: numpy
    """
    h = str(M.shape[0])
    w = str(M.shape[1])
    if len(M.shape) == 3:
        c = M.shape[2]
    else:
        c = 1
    mtype = str(dtype_to_mtype(M.dtype, c))
    shape = w + "," + h + "," + mtype
    socket.send_string(shape, flags=zmq.SNDMORE)
    socket.send(M)


def recv_paint():
    """
    :return: the paint event
    """
    frame = socket.recv_string()
    return int(frame)


def rec_str():
    m = socket.recv_string()
    return m


def recv_mat():
    mat_dim = socket.recv_string()
    shape = mat_dim.split(",")
    h = int(shape[0])
    w = int(shape[1])
    mtype = int(shape[2])
    frame = int(shape[3])
    mat_data = socket.recv(copy=True, track=False)
    return frame, _reshape(mat_data, w, h, mtype)


def cpp_type(dtype):
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
    return mtype


def dtype_to_mtype(dtype, channels):
    """
    http://ninghang.blogspot.de/2012/11/list-of-mat-type-in-opencv.html
    :param dtype:
    :return:
    """

    if channels < 1 or channels > 4:
        raise Exception("number of channels must be between 1 .. 4")

    mtype = cpp_type(dtype)

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
    if len(buf) == 1:
        return None
    M = np.frombuffer(buf, dtype=dtype)
    return np.reshape(M, (w, h, channels))
