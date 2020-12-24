# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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