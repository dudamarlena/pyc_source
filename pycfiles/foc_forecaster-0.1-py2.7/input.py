# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/forecaster/tests/input.py
# Compiled at: 2011-12-28 04:58:47
"""
Created on 16. 12. 2011.

@author: kermit
"""
import unittest
from forecaster.ai.input import Input
from forecaster.common import conf

class Test(unittest.TestCase):

    def test_parse_sample_selection(self):
        input = Input()
        crises_dates, normal_dates = input.parse_sample_selection('test_sample_selection.xls')
        expected_crises = {'usa': [2009, 2001], 'deu': []}
        expected_normal = {'usa': [1994, 1995, 1996], 'deu': [1994, 1995]}
        self.assertEqual(crises_dates, expected_crises)
        self.assertEqual(normal_dates, expected_normal)


if __name__ == '__main__':
    unittest.main()