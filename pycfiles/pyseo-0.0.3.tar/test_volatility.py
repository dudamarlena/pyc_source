# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_volatility.py
# Compiled at: 2016-02-21 15:55:31
__doc__ = 'Test case for pysentosa.volatility\n- run run_test.sh in the top folder\n'
from pysentosa.volatility import *
from unittest import TestCase, main

class TestVolatility(TestCase):

    def test_next_business_day(self):
        self.assertTrue(next_business_day('2015-12-18') == '2015-12-21')
        self.assertTrue(next_business_day('2015-12-18', 2) == '2015-12-22')
        self.assertTrue(next_business_day('2015-12-18', 5) == '2015-12-28')
        self.assertTrue(next_business_day('2015-12-26', 1) == '2015-12-28')

    def test_prev_business_day(self):
        self.assertTrue(prev_business_day('2015-12-21') == '2015-12-18')
        self.assertTrue(prev_business_day('2015-12-21', 2) == '2015-12-17')
        self.assertTrue(prev_business_day('2015-12-28', 1) == '2015-12-24')


if __name__ == '__main__':
    main()