# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/forecaster/tests/wb.py
# Compiled at: 2011-12-21 07:09:19
"""
Created on 15. 12. 2011.

@author: kermit
"""
import unittest
from forecaster.sources import wb

class Test(unittest.TestCase):

    def test_all_indicators(self):
        inds = wb.all_indicators()
        self.assertTrue(len(inds) > 0, "didn't fetch all indicators")


if __name__ == '__main__':
    unittest.main()