# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/meanabsolutepercentageerrortest.py
# Compiled at: 2015-05-28 03:51:33
import unittest
from pycast.common.timeseries import TimeSeries
from pycast.errors import MeanAbsolutePercentageError
import math

class MeanAbsolutePercentageErrorTest(unittest.TestCase):
    """Test class containing all tests for MeanAbsolutePercentageError."""

    def setUp(self):
        self.dataOrg = [
         1.0, 2.3, 0.1, -2.0, -1.0, 0.0, -0.2, -0.3, 0.15, -0.2, 0]
        self.dataCalc = [1.2, 2.0, -0.3, -1.5, -1.5, 0.3, 0.0, 0.3, -0.15, 0.3, 0]

    def tearDown(self):
        pass

    def local_error_test(self):
        """Test MeanAbsolutePercentageError.local_error."""
        localErrors = [
         20, 13.043, 400, 25, 50, None, 100, 200, 200, 250, None]
        mape = MeanAbsolutePercentageError()
        for i in xrange(len(self.dataOrg)):
            calc_local_error = mape.local_error([self.dataOrg[i]], [self.dataCalc[i]])
            if calc_local_error:
                self.assertEquals('%.3f' % calc_local_error, '%.3f' % localErrors[i])
            else:
                self.assertEquals(localErrors[i], None)

        return

    def error_calculation_test(self):
        """Test the calculation of the MeanAbsolutePercentageError."""
        tsOrg = TimeSeries()
        tsCalc = TimeSeries()
        for idx in xrange(len(self.dataOrg)):
            tsOrg.add_entry(float(idx), self.dataOrg[idx])
            tsCalc.add_entry(float(idx), self.dataCalc[idx])

        mape = MeanAbsolutePercentageError()
        mape.initialize(tsOrg, tsCalc)
        self.assertEquals('139.78', str(mape.get_error())[:6])