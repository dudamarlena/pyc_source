# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/symmetricmeanabsolutepercentageerrortest.py
# Compiled at: 2015-05-28 03:51:29
import unittest
from pycast.errors import SymmetricMeanAbsolutePercentageError
from pycast.common.timeseries import TimeSeries

class SymmetricMeanAbsolutePercentageErrorTest(unittest.TestCase):
    """Testing symmetric mean absolute percentage error."""

    def setUp(self):
        self.dataOrg = [
         1.0, 2.3, 0.1, -2.0, -1.0, 0.0, -0.2, -0.3, 0.15, -0.2, 0]
        self.dataCalc = [1.2, 2.0, -0.3, -1.5, -1.5, 0.3, 0.0, 0.3, -0.15, 0.3, 0]

    def tearDown(self):
        pass

    def local_error_test(self):
        """Test SymmetricMeanAbsolutePercentageError.local_error."""
        localErrors = [
         18.182, 13.953, 200, 28.571, 40, 200, 200, 200, 200, 200, 0]
        smape = SymmetricMeanAbsolutePercentageError()
        for i in xrange(len(self.dataOrg)):
            calc_local_error = smape.local_error([self.dataOrg[i]], [self.dataCalc[i]])
            self.assertEquals('%.3f' % calc_local_error, '%.3f' % localErrors[i])

    def error_calculation_test(self):
        """Test the calculation of the SymmetricMeanAbsolutePercentageError."""
        tsOrg = TimeSeries()
        tsCalc = TimeSeries()
        for idx in xrange(len(self.dataOrg)):
            tsOrg.add_entry(float(idx), self.dataOrg[idx])
            tsCalc.add_entry(float(idx), self.dataCalc[idx])

        smape = SymmetricMeanAbsolutePercentageError()
        smape.initialize(tsOrg, tsCalc)
        self.assertEquals('118.24', str(smape.get_error())[:6])