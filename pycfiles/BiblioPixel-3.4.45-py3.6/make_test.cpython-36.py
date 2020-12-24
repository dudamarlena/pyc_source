# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/colors/make_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1525 bytes
import unittest
from fractions import Fraction
from bibliopixel.colors import make, COLORS

class MakeTest(unittest.TestCase):

    def test_color(self):
        self.assertEqual(make.color('red'), COLORS.red)

    def test_split_colors1(self):
        test = 'red, green, [25, 81, 100], yellow'
        actual = list(make._split_colors(test))
        expected = ['red', 'green', '[25, 81, 100]', 'yellow']
        self.assertEqual(actual, expected)

    def test_split_colors2(self):
        test = '[12, 12, 12], red, green, [25, 81, 100], yellow, (3, 4, 5)'
        actual = list(make._split_colors(test))
        expected = ['[12, 12, 12]', 'red', 'green', '[25, 81, 100]',
         'yellow', '(3, 4, 5)']
        self.assertEqual(actual, expected)

    def test_colors0(self):
        test = 'red, green, yellow'
        actual = list(make.colors(test))
        expected = [COLORS.red, COLORS.green, COLORS.yellow]
        self.assertEqual(actual, expected)

    def test_colors1(self):
        test = 'red, green, [25, 81, 100], yellow'
        actual = list(make.colors(test))
        expected = [COLORS.red, COLORS.green, (25, 81, 100), COLORS.yellow]
        self.assertEqual(actual, expected)

    def test_colors2(self):
        test = '[12, 12, 12], red, green, [25, 81, 100], yellow, (3, 4, 5)'
        actual = list(make.colors(test))
        expected = [(12, 12, 12), COLORS.red, COLORS.green, (25, 81, 100),
         COLORS.yellow, (3, 4, 5)]
        self.assertEqual(actual, expected)