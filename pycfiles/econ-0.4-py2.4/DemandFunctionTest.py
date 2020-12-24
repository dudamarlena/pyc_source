# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/DemandFunctionTest.py
# Compiled at: 2007-04-18 06:57:54
import unittest, random
from DemandFunction import *

class DemandFunctionTest(unittest.TestCase):
    __module__ = __name__

    def testGetLinearDemandFunction(self):
        constant = 2.0
        slope = -1.0
        df1 = getLinearDemandFunction(constant, slope)
        price1 = random.random() * 3.0
        expDemand = max(0, 2.0 + price1 * slope)
        self.assertEqual(expDemand, df1(price1))