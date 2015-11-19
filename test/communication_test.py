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
        _thread.start_new(test_server.send_track, (1, M,))
        result = biotracker.rec_str()
        self.assertEqual("q", result)
