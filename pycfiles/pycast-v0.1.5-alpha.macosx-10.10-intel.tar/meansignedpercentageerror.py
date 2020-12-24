# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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