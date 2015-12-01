import unittest
import biotracker

class QPainterTest(unittest.TestCase):
    """
    Unit tests for QPainter (py)
    """

    def test_set_pen(self):
        """
        Check if setPen works correctly
        """
        painter = biotracker.QPainter()
        painter.setPen(100, 50, 30, 33)
        self.assertEqual("p(100,50,30,33)", painter.to_msg())

    def test_set_pen_noalpha(self):
        """
        Check if setPen works correctly
        """
        painter = biotracker.QPainter()
        painter.setPen(100, 50, 30)
        self.assertEqual("p(100,50,30,255)", painter.to_msg())