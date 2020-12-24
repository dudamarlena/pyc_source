# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/geometricmeanabsolutepercentageerrortest.py
# Compiled at: 2015-05-28 03:51:35
import unittest
from pycast.common.timeseries import TimeSeries
from pycast.errors import GeometricMeanAbsolutePercentageError
import math

class GeometricMeanAbsolutePercentageErrorTest(unittest.TestCase):
    """Test class containing all tests for GeometricMeanAbsolutePercentageError."""

    def local_error_test(self):
        orgValues = [
         11, 33.1, 2.3, 6.54, 123.1, 12.54, 12.9]
        calValues = [24, 1.23, 342, 1.21, 4.112, 9.543, 3.54]
        gmape = GeometricMeanAbsolutePercentageError()
        for idx in xrange(len(orgValues)):
            res = math.fabs(calValues[idx] - orgValues[idx]) / orgValues[idx] * 100
            assert str(res)[:6] == str(gmape.local_error([orgValues[idx]], [calValues[idx]]))[:6]

    def error_calculation_test(self):
        """Test the calculation of the GeometricMeanAbsolutePercentageError."""
        dataOrg = [
         [
          1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 8], [7.3, 5], [8, 0], [9, 10]]
        dataCalc = [[1, 3], [2, 5], [3, 0], [4, 3], [5, 6], [6.1, 6], [7, 3], [7.3, 5], [8, 0], [9, 9]]
        tsOrg = TimeSeries.from_twodim_list(dataOrg)
        tsCalc = TimeSeries.from_twodim_list(dataCalc)
        gmape = GeometricMeanAbsolutePercentageError()
        gmape.initialize(tsOrg, tsCalc)
        assert str(gmape.get_error())[:6] == '31.368'
        error = gmape.get_error(startDate=1, endDate=9)
        assert str(error)[:6] == '31.368', '%s != 31.368' % error