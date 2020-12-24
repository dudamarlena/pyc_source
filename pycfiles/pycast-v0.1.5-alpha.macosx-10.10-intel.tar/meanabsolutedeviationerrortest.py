# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/meanabsolutedeviationerrortest.py
# Compiled at: 2015-05-28 03:51:33
import unittest
from pycast.errors import MeanAbsoluteDeviationError
from pycast.common.timeseries import TimeSeries

class MeanAbsoluteDeviationErrorTest(unittest.TestCase):
    """Testing Mean Absolute Deviation error."""

    def setUp(self):
        self.dataOrg = [
         1.0, 2.3, 0.1, -2.0, -1.0, 0.0, -0.2, -0.3, 0.15, -0.2, 0]
        self.dataCalc = [1.2, 2.0, -0.3, -1.5, -1.5, 0.3, 0.0, 0.3, -0.15, 0.3, 0]

    def local_error_test(self):
        """Test MeanAbsoluteDeviationError.local_error."""
        localErrors = [
         0.2, 0.3, 0.4, 0.5, 0.5, 0.3, 0.2, 0.6, 0.3, 0.5, 0]
        mad = MeanAbsoluteDeviationError()
        for idx in xrange(len(self.dataOrg)):
            le = mad.local_error([self.dataOrg[idx]], [self.dataCalc[idx]])
            ple = localErrors[idx]
            self.assertEqual(str(le), str(ple))

    def error_calculation_test(self):
        """Test the calculation of the Mean Absolute Deviation Error."""
        tsOrg = TimeSeries()
        tsCalc = TimeSeries()
        for idx in xrange(len(self.dataOrg)):
            tsOrg.add_entry(float(idx), self.dataOrg[idx])
            tsCalc.add_entry(float(idx), self.dataCalc[idx])

        mad = MeanAbsoluteDeviationError()
        mad.initialize(tsOrg, tsCalc)
        self.assertEqual('0.3454', str(mad.get_error())[:6])