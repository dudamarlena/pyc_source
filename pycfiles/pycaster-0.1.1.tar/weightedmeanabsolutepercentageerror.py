# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/errors/weightedmeanabsolutepercentageerror.py
# Compiled at: 2015-05-28 05:25:49
import math
from pycast.errors import MeanAbsolutePercentageError

class WeightedMeanAbsolutePercentageError(MeanAbsolutePercentageError):
    """Implements a weighted alternative of the MeanAbsolutePercentageError."""

    def local_error(self, originalValue, calculatedValue):
        """Calculates the error between the two given values.

        :param list originalValue:    List containing the values of the original data.
        :param list calculatedValue:    List containing the values of the calculated TimeSeries that
            corresponds to originalValue.

        :return:    Returns the error measure of the two given values.
        :rtype:     numeric
        """
        originalValue = originalValue[0]
        calculatedValue = calculatedValue[0]
        if 0 == originalValue:
            return None
        else:
            signed_mape = (calculatedValue - originalValue) / float(originalValue) * 100.0
            if signed_mape < 0:
                signed_mape *= 2
            return math.fabs(signed_mape)


WMAPE = WeightedMeanAbsolutePercentageError