# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/util/limit_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 3208 bytes
import numpy, unittest
from fractions import Fraction
from bibliopixel.util.limit import Limit
from bibliopixel.util.color_list import ListMath, NumpyMath
from . import color_list_test

class LimitTest(unittest.TestCase):

    def test_default(self):
        limit = Limit()
        self.assertFalse(limit)
        actual = [limit.limit(Fraction(i, 8)) for i in range(9)]
        expected = [Fraction(i, 8) for i in range(9)]
        self.assertEqual(actual, expected)

    def test_ratio(self):
        limit = Limit(ratio=(Fraction(3, 4)))
        self.assertTrue(limit)
        actual = [limit.limit(Fraction(i, 8)) for i in range(11)]
        expected = [Fraction(i, 8) * 3 / 4 for i in range(9)] + [
         Fraction(3, 4), Fraction(3, 4)]
        self.assertEqual(actual, expected)

    def test_knee(self):
        limit = Limit(ratio=(Fraction(3, 4)), knee=(Fraction(1, 4)))
        self.assertTrue(limit)
        actual = [limit.limit(Fraction(i, 8)) for i in range(11)]
        expected = [Fraction(0), Fraction(1, 8), Fraction(1, 4),
         Fraction(1, 3), Fraction(5, 12), Fraction(1, 2),
         Fraction(7, 12), Fraction(2, 3), Fraction(3, 4),
         Fraction(3, 4), Fraction(3, 4)]
        self.assertEqual(actual, expected)

    def test_knee_gain(self):
        limit = Limit(ratio=(Fraction(3, 4)),
          knee=(Fraction(1, 4)),
          gain=(Fraction(1, 2)))
        self.assertTrue(limit)
        actual = [limit.limit(Fraction(i, 8)) for i in range(11)]
        expected = [Fraction(0) / 2, Fraction(1, 8) / 2, Fraction(1, 4) / 2,
         Fraction(1, 3) / 2, Fraction(5, 12) / 2, Fraction(1, 2) / 2,
         Fraction(7, 12) / 2, Fraction(2, 3) / 2, Fraction(3, 4) / 2,
         Fraction(3, 4) / 2, Fraction(3, 4) / 2]
        self.assertEqual(actual, expected)

    def test_knee_gain_disabled(self):
        limit = Limit(ratio=(Fraction(3, 4)),
          knee=(Fraction(1, 4)),
          gain=(Fraction(1, 2)))
        self.assertTrue(limit)
        limit.enable = False
        self.assertFalse(limit)
        actual = [limit.limit(Fraction(i, 8)) for i in range(11)]
        expected = [Fraction(i, 8) for i in range(11)]
        self.assertEqual(actual, expected)

    def test_colors(self):
        limit = Limit(ratio=(Fraction(3, 4)),
          knee=(Fraction(1, 4)),
          gain=(Fraction(1, 2)))
        self.assertTrue(limit)
        cl = color_list_test.COLORS1[:]
        limit.limit_colors(cl, ListMath)
        c = 106.25
        expected = [(c, 0, 0), (0, c, 0), (0, 0, c), (c, c, c)]
        self.assertEqual(len(expected), len(cl))
        asserts = 0
        for exp, act in zip(expected, cl):
            for e, a in zip(exp, act):
                self.assertAlmostEqual(e, a)
                asserts += 1

        self.assertEqual(asserts, 12)

    def test_empty_colors(self):
        limit = Limit()
        self.assertFalse(limit)
        colors = [(1, 1, 1), (2, 2, 2)]
        limit.limit_colors(colors, ListMath)
        self.assertEqual(colors, [(1, 1, 1), (2, 2, 2)])