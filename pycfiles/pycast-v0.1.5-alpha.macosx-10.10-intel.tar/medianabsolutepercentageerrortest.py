# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/medianabsolutepercentageerrortest.py
# Compiled at: 2015-05-28 05:24:05
import unittest
from pycast.errors import MedianAbsolutePercentageError
from pycast.common.timeseries import TimeSeries

class MedianAbsolutePercentageErrorTest(unittest.TestCase):

    def setUp(self):
        self.dataOrg = [
         1.0, 2.3, 0.1, -2.0, -1.0, 0.0, -0.2, -0.3, 0.15, -0.2, 0]
        self.dataCalc = [1.2, 2.0, -0.3, -1.5, -1.5, 0.3, 0.0, 0.3, -0.15, 0.3, 0]

    def error_calculation_test(self):
        """ Test error calculation for MedianAbsolutePercentageError"""
        mdape = MedianAbsolutePercentageError()
        tsOrg = TimeSeries()
        tsCalc = TimeSeries()
        for idx in xrange(len(self.dataOrg)):
            tsOrg.add_entry(float(idx), self.dataOrg[idx])
            tsCalc.add_entry(float(idx), self.dataCalc[idx])

        mdape.initialize(tsOrg, tsCalc)
        self.assertEqual(mdape.get_error(), 100)
        self.assertEqual(mdape.get_error(20.0, 50.0), 50)