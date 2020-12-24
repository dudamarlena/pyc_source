# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: S:\Documents\Code\colourettu\build\lib\colourettu\test\test_setup.py
# Compiled at: 2016-11-27 16:46:25
# Size of source mod 2**32: 350 bytes
import unittest, colourettu

class Test_Setup(unittest.TestCase):

    def test_we_live(self):
        """Test we should *always* pass"""
        pass

    def test_version(self):
        """Version is available"""
        self.assertIsNotNone(colourettu.__version__)


def main():
    unittest.main()


if __name__ == '__main__':
    main()