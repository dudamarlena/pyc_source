# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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