# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/layout/segment_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 398 bytes
import unittest
from bibliopixel.layout.geometry import segment

class SegmentTest(unittest.TestCase):

    def test_all(self):
        segments = segment.make_segments(list(range(21)), 3)
        self.assertEqual(len(segments), 7)
        for i, s in enumerate(segments):
            self.assertEqual(len(s), 3)
            for j, v in enumerate(s):
                self.assertEqual(v, 3 * i + j)