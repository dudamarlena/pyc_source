# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/meansigneddifferenceerrortest.py
# Compiled at: 2015-05-28 03:51:32
import unittest
from pycast.errors import MeanSignedDifferenceError
from pycast.common.timeseries import TimeSeries

class MeanSignedDifferenceErrorTest(unittest.TestCase):
    """Test for the MeanSignedDifferenceError."""

    def setUp(self):
        self.dataOrg = [
         1.0, 2.3, 0.1, -2.0, -1.0, 0.0, -0.2, -0.3, 0.15, -0.2, 0]
        self.dataCalc = [1.2, 2.0, -0.3, -1.5, -1.5, 0.3, 0.0, 0.3, -0.15, 0.3, 0]

    def local_error_test(self):
        """Test MeanSignedDifferenceError.local_error."""
        localErrors = [
         0.2, -0.3, -0.4, 0.5, -0.5, 0.3, 0.2, 0.6, -0.3, 0.5, 0]
        msd = MeanSignedDifferenceError()
        for i in xrange(len(self.dataOrg)):
            calc_local_error = msd.local_error([self.dataOrg[i]], [self.dataCalc[i]])
            self.assertEquals('%.4f' % calc_local_error, '%.4f' % localErrors[i])

    def error_calculation_test(self):
        msd = MeanSignedDifferenceError()
        tsOrg = TimeSeries()
        tsCalc = TimeSeries()
        for idx in xrange(len(self.dataOrg)):
            tsOrg.add_entry(float(idx), self.dataOrg[idx])
            tsCalc.add_entry(float(idx), self.dataCalc[idx])

        msd.initialize(tsOrg, tsCalc)
        self.assertEquals(str(msd.get_error())[:6], '0.0727')