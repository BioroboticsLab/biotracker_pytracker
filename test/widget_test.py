import unittest
import biotracker


class WidgetTest(unittest.TestCase):
    """
    Unit tests for the widgets
    """

    def test_id(self):
        """
        make sure the id counts up correctly
        """
        a = biotracker.Widget()
        b = biotracker.Widget()
        self.assertFalse(a.id == b.id)

    def test_text(self):
        """
        """
        a = biotracker.Text("test")
        self.assertEqual(a.to_msg(), "t(" + str(a.id) + ",test)")

    def test_button(self):
        b = biotracker.Button("Click", lambda x: x)
        self.assertEqual(b.to_msg(), "b(" + str(b.id) + ",Click)")
