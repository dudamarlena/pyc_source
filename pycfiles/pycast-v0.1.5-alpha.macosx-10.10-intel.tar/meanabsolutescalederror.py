# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/errors/meanabsolutescalederror.py
# Compiled at: 2015-05-28 03:51:44
from pycast.errors import BaseErrorMeasure

class MeanAbsoluteScaledError(BaseErrorMeasure):
    """Implements the mean absolute scaled error.

    R J Hyndman and A B Koehler, "Another look at measures of forecast accuracy"
    """

    def __init__(self, minimalErrorCalculationPercentage=60, historyLength=10.0):
        """Initializes the error measure.

        :param integer minimalErrorCalculationPercentage:    The number of entries in an
            original TimeSeries that have to have corresponding partners in the calculated
            TimeSeries. Corresponding partners have the same time stamp.
            Valid values are in [0.0, 100.0].
        :param numeric historyLength:    Length of the TimeSeries used to calculate the mean
            of the history. If this is an Integer, the last historyLength data points will be used.
            If this is a Float, the last historyLength percent of the TimeSeries will be used for
            error calculation.

        :raise: Raises a :py:exc:`ValueError` if minimalErrorCalculationPercentage is not
            in [0.0, 100.0].
        :raise: Raises a :py:exc:`ValueError` if historyLength is a Float and not 
            in (0.0, 100.0).
        :raise: Raises a :py:exc:`ValueError` if historyLength + minimalErrorCalculationPercentage
            is not in (0.0, 100.0].
        """
        if not 0.0 < historyLength < 100.0:
            raise ValueError('historyLength has to be in (0.0, 100.0).')
        if isinstance(historyLength, float) and historyLength + minimalErrorCalculationPercentage > 100.0:
            raise ValueError('historyLength + minimalErrorCalculationPercentage has to be in (0.0, 100.0].')
        super(MeanAbsoluteScaledError, self).__init__(minimalErrorCalculationPercentage)
        self._historyLength = historyLength
        self._historicMeans = []

    def _get_historic_means(self, timeSeries):
        """Calculates the mean value for the history of the MeanAbsoluteScaledError.

        :param TimeSeries timeSeries:    Original TimeSeries used to calculate the mean historic values.

        :return:    Returns a list containing the historic means.
        :rtype: list
        """
        historyLength = self._historyLength
        historicMeans = []
        append = historicMeans.append
        for startIdx in xrange(len(timeSeries) - historyLength - 1):
            value = 0
            for idx in xrange(startIdx, startIdx + historyLength):
                value += abs(timeSeries[(idx + 1)][1] - timeSeries[idx][1])

            append(value / float(historyLength))

        return historicMeans

    def initialize(self, originalTimeSeries, calculatedTimeSeries):
        """Initializes the ErrorMeasure.

        During initialization, all :py:meth:`BaseErrorMeasure.local_error()` are calculated.

        :param TimeSeries originalTimeSeries:    TimeSeries containing the original data.
        :param TimeSeries calculatedTimeSeries:    TimeSeries containing calculated data.
            Calculated data is smoothed or forecasted data.

        :return:    Return :py:const:`True` if the error could be calculated, :py:const:`False`
            otherwise based on the minimalErrorCalculationPercentage.
        :rtype: boolean

        :raise:    Raises a :py:exc:`StandardError` if the error measure is initialized multiple times.
        """
        if 0 < len(self._errorValues):
            raise StandardError('An ErrorMeasure can only be initialized once.')
        if isinstance(self._historyLength, float):
            self._historyLength = int(self._historyLength * len(originalTimeSeries) / 100.0)
        originalTimeSeries.sort_timeseries()
        calculatedTimeSeries.sort_timeseries()
        self._historicMeans = self._get_historic_means(originalTimeSeries)
        append = self._errorValues.append
        appendDates = self._errorDates.append
        local_error = self.local_error
        minCalcIdx = self._historyLength + 1
        for orgPair in originalTimeSeries[minCalcIdx:]:
            for calcIdx in xrange(minCalcIdx, len(calculatedTimeSeries)):
                calcPair = calculatedTimeSeries[calcIdx]
                if calcPair[0] != orgPair[0]:
                    continue
                append(local_error(orgPair[1:], calcPair[1:]))
                appendDates(orgPair[0])

        if len(filter(lambda item: item != None, self._errorValues)) < self._minimalErrorCalculationPercentage * len(originalTimeSeries):
            self._errorValues = []
            self._errorDates = []
            self._historicMeans = []
            return False
        return True

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
        if None != startDate:
            possibleDates = filter(lambda date: date >= startDate, self._errorDates)
            meanIdx = self._errorDates.index(min(possibleDates))
        else:
            meanIdx = int(startingPercentage * len(self._errorValues) / 100.0)
        mad = sum(errorValues) / float(len(errorValues))
        historicMean = self._historicMeans[meanIdx]
        return mad / historicMean

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
        return abs(originalValue - calculatedValue)


MASE = MeanAbsoluteScaledError