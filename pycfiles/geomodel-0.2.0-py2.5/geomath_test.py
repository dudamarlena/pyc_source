# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/geo/tests/geomath_test.py
# Compiled at: 2009-08-31 04:00:03
"""Unit tests for geomath.py."""
__author__ = 'api.roman.public@gmail.com (Roman Nurik)'
import unittest
from geo import geomath
from geo import geotypes

class GeomathTests(unittest.TestCase):

    def test_distance(self):
        calc_dist = geomath.distance(geotypes.Point(37, -122), geotypes.Point(42, -75))
        known_dist = 4024365
        self.assertTrue(abs((calc_dist - known_dist) / known_dist) <= 0.01)


if __name__ == '__main__':
    unittest.main()