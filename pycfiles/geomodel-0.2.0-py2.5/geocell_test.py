# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/geo/tests/geocell_test.py
# Compiled at: 2009-08-31 03:59:42
"""Unit tests for geocell.py."""
__author__ = 'api.roman.public@gmail.com (Roman Nurik)'
import unittest
from geo import geocell
from geo import geotypes

class GeocellTests(unittest.TestCase):

    def test_compute(self):
        cell = geocell.compute(geotypes.Point(37, -122), 14)
        self.assertEqual(14, len(cell))
        self.assertTrue(geocell.is_valid(cell))
        self.assertTrue(geocell.contains_point(cell, geotypes.Point(37, -122)))
        lowres_cell = geocell.compute(geotypes.Point(37, -122), 8)
        self.assertTrue(cell.startswith(lowres_cell))
        self.assertTrue(geocell.contains_point(lowres_cell, geotypes.Point(37, -122)))
        cell = geocell.compute(geotypes.Point(0, 0), 0)
        self.assertEqual(0, len(cell))
        self.assertFalse(geocell.is_valid(cell))

    def test_compute_box(self):
        cell = geocell.compute(geotypes.Point(37, -122), 14)
        box = geocell.compute_box(cell)
        self.assertTrue(box.south <= 37 and 37 <= box.north and box.west <= -122 and -122 <= box.east)

    def test_adjacent(self):
        cell = geocell.compute(geotypes.Point(37, -122), 14)
        box = geocell.compute_box(cell)
        self.assertEquals(box.north, geocell.compute_box(geocell.adjacent(cell, (0,
                                                                                 1))).south)
        self.assertEquals(box.south, geocell.compute_box(geocell.adjacent(cell, (0,
                                                                                 -1))).north)
        self.assertEquals(box.east, geocell.compute_box(geocell.adjacent(cell, (1,
                                                                                0))).west)
        self.assertEquals(box.west, geocell.compute_box(geocell.adjacent(cell, (-1,
                                                                                0))).east)
        self.assertEquals(8, len(geocell.all_adjacents(cell)))
        self.assertTrue(geocell.collinear(cell, geocell.adjacent(cell, (0, 1)), True))
        self.assertFalse(geocell.collinear(cell, geocell.adjacent(cell, (0, 1)), False))
        self.assertTrue(geocell.collinear(cell, geocell.adjacent(cell, (1, 0)), False))
        self.assertFalse(geocell.collinear(cell, geocell.adjacent(cell, (1, 0)), True))

    def test_interpolation(self):
        cell = geocell.compute(geotypes.Point(37, -122), 14)
        sw_adjacent = geocell.adjacent(cell, (-1, -1))
        sw_adjacent2 = geocell.adjacent(sw_adjacent, (-1, -1))
        self.assertEquals(4, len(geocell.interpolate(cell, sw_adjacent)))
        self.assertEquals(4, geocell.interpolation_count(cell, sw_adjacent))
        self.assertEquals(9, len(geocell.interpolate(cell, sw_adjacent2)))
        self.assertEquals(9, geocell.interpolation_count(cell, sw_adjacent2))


if __name__ == '__main__':
    unittest.main()