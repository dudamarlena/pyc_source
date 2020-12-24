# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/weightedmapetest.py
# Compiled at: 2015-05-28 03:51:28
import unittest
from pycast.errors import WeightedMeanAbsolutePercentageError
from pycast.common.timeseries import TimeSeries

class WeightedMeanAbsolutePercentageErrorTest(unittest.TestCase):
    """Test class containing all tests for WeightedMeanAbsolutePercentageError."""

    def local_error_test(self):
        orgValues = [
         11, 33.1, 2.3, 6.54, 123.1, 12.54, 12.9]
        calValues = [24, 1.23, 342, 1.21, 4.112, 9.543, 3.54]
        resValues = ['118.181', '192.567', '14769.5', '162.996', '193.319', '47.7990', '145.116']
        wmape = WeightedMeanAbsolutePercentageError()
        for idx in xrange(len(orgValues)):
            localError = wmape.local_error([orgValues[idx]], [calValues[idx]])
            assert str(resValues[idx]) == str(localError)[:7], str(resValues[idx]) + '!=' + str(localError)[:7]

    def error_calculation_test(self):
        """Test the calculation of the MeanAbsolutePercentageError."""
        dataOrg = [
         [
          1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 8], [7.3, 5], [8, 0], [9, 10]]
        dataCalc = [[1, 3], [2, 5], [3, 0], [4, 3], [5, 5], [6.1, 6], [7, 3], [7.3, 5], [8, 0], [9, 9]]
        tsOrg = TimeSeries.from_twodim_list(dataOrg)
        tsCalc = TimeSeries.from_twodim_list(dataCalc)
        wmape = WeightedMeanAbsolutePercentageError()
        wmape.initialize(tsOrg, tsCalc)
        assert str(wmape.get_error())[:6] == '93.125'