import unittest
import numpy as np
import _thread
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
        try:
            biotracker.run_client(track, paint, shutdown)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_full_paint_cycle(self):
        """

        """
        send_frame = 10

        def track():
            pass

        def paint(f):
            self.assertEqual(f, send_frame)
            raise Exception("success")

        def shutdown():
            pass

        def keep_running():
            return False

        _thread.start_new(test_server.send_complete_paint, (send_frame,))

        try:
            biotracker.run_client(track, paint, shutdown, keep_running=keep_running)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

