# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/errors/meansignedpercentageerror.py
# Compiled at: 2015-05-28 05:26:03
import math
from pycast.errors import MeanAbsolutePercentageError

class MeanSignedPercentageError(MeanAbsolutePercentageError):
    """An over/under estimation aware percentage error."""

    def local_error(self, originalValue, calculatedValue):
        """Calculates the error between the two given values.

        :param list originalValue:    List containing the values of the original data.
        :param list calculatedValue:    List containing the values of the calculated TimeSeries that
            corresponds to originalValue.

        :return:    Returns the error measure of the two given values.
        :rtype:     numeric
        """
        if originalValue[0]:
            return float(calculatedValue[0] - originalValue[0]) / originalValue[0] * 100
        else:
            return


MSPE = MeanSignedPercentageError