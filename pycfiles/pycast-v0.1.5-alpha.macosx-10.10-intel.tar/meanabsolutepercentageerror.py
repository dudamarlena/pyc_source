# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/errors/meanabsolutepercentageerror.py
# Compiled at: 2015-05-28 05:37:43
import math
from pycast.errors import BaseErrorMeasure

class MeanAbsolutePercentageError(BaseErrorMeasure):

    def _calculate(self, startingPercentage, endPercentage, startDate, endDate):
        """This is the error calculation function that gets called by :py:meth:`BaseErrorMeasure.get_error`.

        Both parameters will be correct at this time.

        :param float startingPercentage: Defines the start of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, where the error calculation should be started. 
            25.0 for example means that the first 25% of all calculated errors will be ignored.
        :param float endPercentage:    Defines the end of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, after which all error values will be ignored. 90.0 for example means that
            the last 10% of all local errors will be ignored.
        :param float startDate: Epoch representing the start date used for error calculation.
        :param float endDate: Epoch representing the end date used in the error calculation.

        :return:    Returns a float representing the error.
        :rtype: float
        """
        errorValues = self._get_error_values(startingPercentage, endPercentage, startDate, endDate)
        errorValues = filter(lambda item: item != None, errorValues)
        return float(sum(errorValues)) / float(len(errorValues))

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
            return math.fabs((calculatedValue - originalValue) / float(originalValue)) * 100.0


MAPE = MeanAbsolutePercentageError