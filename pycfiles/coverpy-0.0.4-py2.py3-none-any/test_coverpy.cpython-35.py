# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sergio/Projects/cpy/coverpy/build/lib/test/test_coverpy.py
# Compiled at: 2016-05-21 19:17:09
# Size of source mod 2**32: 452 bytes
import unittest, coverpy

class TestCoverPy(unittest.TestCase):

    def setUp(self):
        self.coverpy = coverpy.CoverPy()

    def test_get_cover(self):
        """ Test retrieving a sample cover, OK Computer by Radiohead. """
        result = self.coverpy.get_cover('OK Computer')
        self.assertEqual(result.album, 'OK Computer')
        self.assertEqual(result.artist, 'Radiohead')


if __name__ == '__main__':
    unittest.main()