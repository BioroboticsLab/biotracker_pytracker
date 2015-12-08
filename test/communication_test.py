import unittest
import numpy as np
import _thread
import time
import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../server')

import test_server
import biotracker


class Communication(unittest.TestCase):
    """
    Unit tests
    """

    def setUp(self):
        biotracker.start()

    def test_start(self):
        """
        test the server-client test architecture
        """
        send = "test123"
        _thread.start_new(test_server.send_str, (send,))
        result = biotracker.rec_str()
        self.assertEqual(result, send)

    def test_track(self):
        """
        test the track loop
        """
        M = np.random.rand(800, 600)
        _thread.start_new(test_server.send_track, (8, M,))
        frame, result = biotracker.recv_mat()
        self.assertEqual(M.shape[0], result.shape[0])
        self.assertEqual(M.shape[1], result.shape[1])
        self.assertEqual(frame, 8)

    def test_wrong_function_registration(self):
        """
        test that we can only register functions
        """
        def track():
            pass

        def paint():
            pass
        shutdown = "hello"

        def paintOverlay():
            pass

        try:
            biotracker.run_client(track, paint, paintOverlay, shutdown)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_request_widgets(self):
        """
        make sure that the widgets reach the server
        """
        track = lambda _: None
        paint = lambda _: None
        paintOverlay = lambda _: None
        shutdown = lambda _: None
        keep_running = lambda t: t != "4"

        def request_widgets():
            widgets = []
            widgets.append(biotracker.Button('Click', lambda _: None))
            widgets.append(biotracker.Divider())
            return widgets

        result = dict()
        _thread.start_new(test_server.send_widget_request, (result,))
        biotracker.run_client(
            track,
            paint,
            paintOverlay,
            shutdown,
            keep_running=keep_running,
            request_widgets=request_widgets)
        time.sleep(5)
        print(result)
        #self.assertEqual(result['widgets'], "")

    def test_button_callback(self):
        """
        Mimics the button callback
        """
        pass

    def test_full_paint_cycle(self):
        """

        """
        send_frame = 10

        def track():
            pass

        def paint(f):
            self.assertEqual(f, send_frame)

        def paintOverlay(qpainter):
            qpainter.drawRect((0, 1, 10, 5))

        def shutdown():
            pass

        def keep_running(msg_type):
                return msg_type != "3"

        result = dict()
        _thread.start_new(test_server.send_complete_paint, (send_frame, result))

        biotracker.run_client(
            track,
            paint,
            paintOverlay,
            shutdown,
            keep_running=keep_running)
        time.sleep(5)
        self.assertEqual(result['qpainter'], "r(0,1,10,5)")

