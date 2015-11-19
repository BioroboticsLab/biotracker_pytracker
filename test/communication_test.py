import unittest
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

    def test_start(self):
        """
        test the server-client test architecture
        """
        send = "test123"
        _thread.start_new(test_server.send_str, (send,))
        biotracker.start()
        result = biotracker.rec_str()
        self.assertEqual(result, send)
