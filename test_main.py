import unittest
import os


class TestCli(unittest.TestCase):
    def test_procedures(self):
        self.assertEqual(os.system('./main_example procedures 2>&1 > /dev/null'), 0)
        self.assertEqual(os.system('./main_example procedures --help 2>&1 > /dev/null'), 0)
        self.assertEqual(os.system('./main_example procedures -t foofoo | wc -l | grep 0 2>&1 > /dev/null'), 0)
        self.assertEqual(os.system('./main_example procedures -s foofoo | wc -l | grep 0 2>&1 > /dev/null'), 0)


if __name__ == '__main__':
    unittest.main()
