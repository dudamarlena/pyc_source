# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/forecaster/tests/indicator.py
# Compiled at: 2011-12-28 04:58:47
"""
Created on 15. 12. 2011.

@author: kermit
"""
import unittest
from forecaster.model.indicator import Indicator

class Test(unittest.TestCase):

    def test_apply_derivative(self):
        indicator = Indicator([1, 2, 3], [17, 16, 13])
        indicator.apply_derivative()
        self.assertEqual(indicator.values, [-1, -3])
        self.assertEqual(indicator.dates, [2, 3])


if __name__ == '__main__':
    unittest.main()