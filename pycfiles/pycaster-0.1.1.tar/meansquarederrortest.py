# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/meansquarederrortest.py
# Compiled at: 2015-05-28 05:24:11
import unittest
from pycast.errors import MeanSquaredError
from pycast.common.timeseries import TimeSeries

class MeanSquaredErrorTest(unittest.TestCase):
    """Testing MeanSquaredError."""

    def setUp(self):
        self.dataOrg = [
         1.0, 2.3, 0.1, -2.0, -1.0, 0.0, -0.2, -0.3, 0.15, -0.2, 0]
        self.dataCalc = [1.2, 2.0, -0.3, -1.5, -1.5, 0.3, 0.0, 0.3, -0.15, 0.3, 0]

    def tearDown(self):
        pass

    def local_error_test(self):
        """Test MeanSquaredError.local_error."""
        localErrors = [
         0.04, 0.09, 0.16, 0.25, 0.25, 0.09, 0.04, 0.36, 0.09, 0.25, 0]
        mse = MeanSquaredError()
        for i in xrange(len(self.dataOrg)):
            calc_local_error = mse.local_error([self.dataOrg[i]], [self.dataCalc[i]])
            self.assertEquals('%.3f' % calc_local_error, '%.3f' % localErrors[i])

    def error_calculation_test(self):
        """Test the calculation of the MeanSquaredError."""
        tsOrg = TimeSeries()
        tsCalc = TimeSeries()
        for idx in xrange(len(self.dataOrg)):
            tsOrg.add_entry(float(idx), self.dataOrg[idx])
            tsCalc.add_entry(float(idx), self.dataCalc[idx])

        mse = MeanSquaredError()
        mse.initialize(tsOrg, tsCalc)
        self.assertEquals('0.1472', str(mse.get_error())[:6])