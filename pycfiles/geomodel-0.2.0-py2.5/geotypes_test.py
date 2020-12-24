# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/geo/tests/geotypes_test.py
# Compiled at: 2009-08-31 03:57:11
"""Unit tests for geotypes.py."""
__author__ = 'api.roman.public@gmail.com (Roman Nurik)'
import unittest
from geo import geotypes

class PointTests(unittest.TestCase):

    def test_Point(self):
        self.assertRaises(ValueError, geotypes.Point, 95, 0)
        self.assertRaises(ValueError, geotypes.Point, 0, 185)
        point = geotypes.Point(37, -122)
        self.assertEquals(37, point.lat)
        self.assertEquals(-122, point.lon)
        self.assertTrue(isinstance(point.__str__(), str))
        self.assertEquals(geotypes.Point(37, -122), geotypes.Point(37, -122))
        self.assertNotEquals(geotypes.Point(37, -122), geotypes.Point(0, 0))


class BoxTests(unittest.TestCase):

    def test_Box(self):
        self.assertRaises(ValueError, geotypes.Box, 95, 0, 0, 0)
        box = geotypes.Box(37, -122, 34, -125)
        self.assertEquals(37, box.north)
        self.assertEquals(34, box.south)
        self.assertEquals(-122, box.east)
        self.assertEquals(-125, box.west)
        self.assertRaises(ValueError, box._set_north, 32)
        self.assertRaises(ValueError, box._set_south, 39)
        self.assertTrue(isinstance(box.__str__(), str))
        self.assertEquals(geotypes.Box(37, -122, 34, -125), geotypes.Box(34, -122, 37, -125))


if __name__ == '__main__':
    unittest.main()