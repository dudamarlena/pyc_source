# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/colors/closest_colors_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1015 bytes
import collections, unittest
from bibliopixel.colors import closest_colors
closest = closest_colors.closest_colors

class ClosestColorsTest(unittest.TestCase):

    def exhaustive(self, metric, start=32, skip=64, report=4):
        for color in closest_colors.all_colors(start, skip=skip):
            cl = closest(color, metric)
            if len(cl) >= report:
                yield (
                 color, cl)

    def test_simple(self):
        self.assertEqual(closest((255, 0, 0)), ['red', 'red 1'])

    def test_far(self):
        c = closest((0, 0, 64), metric=(closest_colors.taxicab))
        self.assertEqual(c, ['black', 'navy', 'none', 'off'])
        c = closest((64, 0, 0), metric=(closest_colors.taxicab))
        self.assertEqual(c, ['black', 'maroon', 'none', 'off'])

    def test_euclidean(self):
        ex = list(self.exhaustive(closest_colors.euclidean))
        self.assertEqual(ex, [])

    def test_taxicab(self):
        ex = list(self.exhaustive(closest_colors.taxicab))
        self.assertEqual(ex, [])