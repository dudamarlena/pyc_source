# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/DiscountRateTest.py
# Compiled at: 2007-04-18 06:57:54
import unittest
from DiscountRate import *
import data

class DiscountRateTest(unittest.TestCase):
    __module__ = __name__

    def testDiscountRateConstant(self):
        drc1 = DiscountRateConstant()
        self.assertEquals(drc1.getDiscount(5), 1, 'PV should be 1')
        drc1.setUnitDiscountRate(1 / 1.02)
        self.assertEquals(drc1.getUnitDiscountRate(), 1 / 1.02)
        self.assertEquals(drc1.getDiscount(0), 1, 'PV when time elapsed is 0 should be 1')
        self.assertEquals(drc1.getDiscount(1), 1 / 1.02)
        self.assertEquals(drc1.getReturn(1), 1.02)

    def testGetSet(self):
        rate1 = 1.0 / 1.02
        rate2 = 1.0 / 1.05
        drc1 = DiscountRateConstant(1.0 / 1.02)
        out1 = drc1.getUnitDiscountRate()
        self.assertEquals(rate1, out1)
        drc1.setUnitDiscountRate(rate2)
        out2 = drc1.getUnitDiscountRate()
        self.assertEquals(rate2, out2)


class DiscountRateHistoricalTest(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        dataPoints = [
         (1850, 10.9), (1990, 497.6), (2002, 695.1)]
        ts1 = data.TimeSeries(dataPoints)
        self.discounter = DiscountRateHistorical(ts1)

    def test1(self):
        out1 = self.discounter.getReturn(1850, 2002)
        exp1 = 695.1 / 10.9
        self.assertAlmostEquals(out1, exp1)