# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/test_series.py
# Compiled at: 2017-06-19 11:05:10
from uncertainties import ufloat
from unittest import TestCase
from unseries import Series

class TestSeries(TestCase):

    def test_zero_input(self):
        z0 = Series(1)
        self.assertEqual(str(z0), '0')
        self.assertEqual(z0.pprint(), '0')
        self.assertEqual(('{}').format(z0), '0')

    def test__add(self):
        z1 = Series(2, {0: ufloat(1, 0.3), 1: ufloat(2, 0.003)})
        z2 = Series(3, {0: ufloat(-1, 0.4), 1: ufloat(-2, 0.004), 2: ufloat(999, 0.1)})
        z3 = Series(2, {0: ufloat(0, 0.5), 1: ufloat(0, 0.005)})