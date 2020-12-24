# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/repos/python-ternary/tests/test_heatmapping.py
# Compiled at: 2015-08-03 11:44:35
import unittest
from numpy.testing import assert_array_almost_equal
from ternary.heatmapping import triangle_coordinates, alt_triangle_coordinates, hexagon_coordinates
from ternary.helpers import SQRT3OVER2

class FunctionCases(unittest.TestCase):

    def test_coordinates(self):
        coords = triangle_coordinates(1, 1, 1)
        expected = [(1, 1, 1), (2, 1, 0), (1, 2, 0)]
        self.assertEqual(coords, expected)
        coords = alt_triangle_coordinates(2, 2, 2)
        expected = [(2, 3, 1), (3, 2, 1), (3, 3, 0)]
        self.assertEqual(coords, expected)
        coords = hexagon_coordinates(1, 1, 1)
        expected = [(2.0 / 3, 5.0 / 3, 1.0), (4.0 / 3, 4.0 / 3, 1.0), (5.0 / 3, 2.0 / 3, 1.0),
         (
          4.0 / 3, 1.0 / 3, 1.0), (2.0 / 3, 2.0 / 3, 1.0), (1.0 / 3, 4.0 / 3, 1.0)]
        print coords
        print expected
        assert_array_almost_equal(coords, expected)


if __name__ == '__main__':
    unittest.main()