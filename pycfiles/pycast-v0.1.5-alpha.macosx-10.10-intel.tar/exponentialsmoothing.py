# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/methods/exponentialsmoothing.py
# Compiled at: 2015-05-28 03:51:40
from pycast.methods import BaseForecastingMethod
from pycast.common.timeseries import TimeSeries

class ExponentialSmoothing(BaseForecastingMethod):
    """Implements an exponential smoothing algorithm.

    Explanation:
        http://www.youtube.com/watch?v=J4iODLa9hYw
    """

    def __init__(self, smoothingFactor=0.1, valuesToForecast=1):
        """Initializes the ExponentialSmoothing.

        :param float smoothingFactor:    Defines the alpha for the ExponentialSmoothing.
            Valid values are in (0.0, 1.0).
        :param integer valuesToForecast:    Number of values that should be forecasted.

        :raise: Raises a :py:exc:`ValueError` when smoothingFactor has an invalid value.
        """
        super(ExponentialSmoothing, self).__init__(['smoothingFactor'], valuesToForecast, True, True)
        self.set_parameter('smoothingFactor', smoothingFactor)

    def _get_parameter_intervals(self):
        """Returns the intervals for the methods parameter.

        Only parameters with defined intervals can be used for optimization!

        :return:    Returns a dictionary containing the parameter intervals, using the parameter
            name as key, while the value hast the following format:
            [minValue, maxValue, minIntervalClosed, maxIntervalClosed]

                - minValue
                    Minimal value for the parameter
                - maxValue
                    Maximal value for the parameter
                - minIntervalClosed
                    :py:const:`True`, if minValue represents a valid value for the parameter.
                    :py:const:`False` otherwise.
                - maxIntervalClosed:
                    :py:const:`True`, if maxValue represents a valid value for the parameter.
                    :py:const:`False` otherwise.
        :rtype: dictionary
        """
        parameterIntervals = {}
        parameterIntervals['smoothingFactor'] = [
         0.0, 1.0, False, False]
        return parameterIntervals

    def execute(self, timeSeries):
        """Creates a new TimeSeries containing the smoothed and forcasted values.

        :return:    TimeSeries object containing the smoothed TimeSeries,
           including the forecasted values.
        :rtype:     TimeSeries
        
        :note:    The first normalized value is chosen as the starting point.
        """
        self._calculate_values_to_forecast(timeSeries)
        alpha = self._parameters['smoothingFactor']
        valuesToForecast = self._parameters['valuesToForecast']
        resultList = []
        estimator = None
        lastT = None
        append = resultList.append
        for idx in xrange(len(timeSeries)):
            t = timeSeries[idx]
            if None == estimator:
                estimator = t[1]
                continue
            if 0 == len(resultList):
                append([t[0], estimator])
                lastT = t
                continue
            error = lastT[1] - estimator
            estimator = estimator + alpha * error
            lastT = t
            append([t[0], estimator])

        if valuesToForecast > 0:
            currentTime = resultList[(-1)][0]
            normalizedTimeDiff = currentTime - resultList[(-2)][0]
            for idx in xrange(valuesToForecast):
                currentTime += normalizedTimeDiff
                error = lastT[1] - estimator
                estimator = estimator + alpha * error
                append([currentTime, estimator])
                lastT = resultList[(-1)]

        return TimeSeries.from_twodim_list(resultList)


class HoltMethod(BaseForecastingMethod):
    """Implements the Holt algorithm.

    Explanation:
        http://en.wikipedia.org/wiki/Exponential_smoothing#Double_exponential_smoothing
    """

    def __init__(self, smoothingFactor=0.1, trendSmoothingFactor=0.5, valuesToForecast=1):
        """Initializes the HoltMethod.

        :param float smoothingFactor:    Defines the alpha for the ExponentialSmoothing.
            Valid values are in (0.0, 1.0).
        :param float trendSmoothingFactor:    Defines the beta for the HoltMethod.
            Valid values are in (0.0, 1.0).
        :param integer valuesToForecast:    Defines the number of forecasted values that will
            be part of the result.

        :raise:    Raises a :py:exc:`ValueError` when smoothingFactor or trendSmoothingFactor has an invalid value.
        """
        super(HoltMethod, self).__init__(['smoothingFactor',
         'trendSmoothingFactor'], valuesToForecast, True, True)
        self.set_parameter('smoothingFactor', smoothingFactor)
        self.set_parameter('trendSmoothingFactor', trendSmoothingFactor)

    def _get_parameter_intervals(self):
        """Returns the intervals for the methods parameter.

        Only parameters with defined intervals can be used for optimization!

        :return:    Returns a dictionary containing the parameter intervals, using the parameter
            name as key, while the value hast the following format:
            [minValue, maxValue, minIntervalClosed, maxIntervalClosed]

                - minValue
                    Minimal value for the parameter
                - maxValue
                    Maximal value for the parameter
                - minIntervalClosed
                    :py:const:`True`, if minValue represents a valid value for the parameter.
                    :py:const:`False` otherwise.
                - maxIntervalClosed:
                    :py:const:`True`, if maxValue represents a valid value for the parameter.
                    :py:const:`False` otherwise.
        :rtype: dictionary
        """
        parameterIntervals = {}
        parameterIntervals['smoothingFactor'] = [
         0.0, 1.0, False, False]
        parameterIntervals['trendSmoothingFactor'] = [0.0, 1.0, False, False]
        return parameterIntervals

    def execute(self, timeSeries):
        """Creates a new TimeSeries containing the smoothed values.

        :return:    TimeSeries object containing the smoothed TimeSeries,
            including the forecasted values.
        :rtype:     TimeSeries
        
        :note: The first normalized value is chosen as the starting point.
        """
        self._calculate_values_to_forecast(timeSeries)
        alpha = self._parameters['smoothingFactor']
        beta = self._parameters['trendSmoothingFactor']
        valuesToForecast = self._parameters['valuesToForecast']
        resultList = []
        estimator = None
        trend = None
        lastT = None
        append = resultList.append
        for idx in xrange(len(timeSeries)):
            t = timeSeries[idx]
            if None == estimator:
                estimator = t[1]
                lastT = t
                continue
            if 0 == len(resultList):
                append([t[0], estimator])
                trend = t[1] - lastT[1]
                lastT = t
                lastEstimator = estimator
                continue
            estimator = alpha * t[1] + (1 - alpha) * (estimator + trend)
            trend = beta * (estimator - lastEstimator) + (1 - beta) * trend
            append([t[0], estimator])
            lastT = t
            lastEstimator = estimator

        if valuesToForecast > 0:
            currentTime = resultList[(-1)][0]
            normalizedTimeDiff = currentTime - resultList[(-2)][0]
            for idx in xrange(1, valuesToForecast + 1):
                currentTime += normalizedTimeDiff
                forecast = estimator + idx * trend
                append([currentTime, forecast])

        return TimeSeries.from_twodim_list(resultList)


class HoltWintersMethod(BaseForecastingMethod):
    """Implements the Holt-Winters algorithm.

    Explanation:
        http://en.wikipedia.org/wiki/Exponential_smoothing#Triple_exponential_smoothing
    """

    def __init__(self, smoothingFactor=0.1, trendSmoothingFactor=0.5, seasonSmoothingFactor=0.5, seasonLength=0, valuesToForecast=1):
        """Initializes the HoltWintersMethod.

        :param float smoothingFactor:    Defines the alpha for the Holt-Winters algorithm.
            Valid values are (0.0, 1.0).
        :param float trendSmoothingFactor:    Defines the beta for the Holt-Winters algorithm..
            Valid values are (0.0, 1.0).
        :param float seasonSmoothingFactor:    Defines the gamma for the Holt-Winters algorithm.
            Valid values are (0.0, 1.0). 
        :param integer seasonLength:    The expected length for the seasons. Please use a good estimate here!
        :param integer valuesToForecast:    Defines the number of forecasted values that will be part of the result.
        """
        super(HoltWintersMethod, self).__init__(['smoothingFactor',
         'trendSmoothingFactor',
         'seasonSmoothingFactor',
         'seasonLength'], valuesToForecast, True, True)
        if not 0 < seasonLength:
            raise ValueError('Please specify season length that is greater than 0.')
        self.set_parameter('smoothingFactor', smoothingFactor)
        self.set_parameter('trendSmoothingFactor', trendSmoothingFactor)
        self.set_parameter('seasonSmoothingFactor', seasonSmoothingFactor)
        self.set_parameter('seasonLength', seasonLength)

    def _get_parameter_intervals(self):
        """Returns the intervals for the methods parameter.

        Only parameters with defined intervals can be used for optimization!

        :return:    Returns a dictionary containing the parameter intervals, using the parameter
            name as key, while the value hast the following format:
            [minValue, maxValue, minIntervalClosed, maxIntervalClosed]

                - minValue
                    Minimal value for the parameter
                - maxValue
                    Maximal value for the parameter
                - minIntervalClosed
                    :py:const:`True`, if minValue represents a valid value for the parameter.
                    :py:const:`False` otherwise.
                - maxIntervalClosed:
                    :py:const:`True`, if maxValue represents a valid value for the parameter.
                    :py:const:`False` otherwise.
        :rtype: dictionary
        """
        parameterIntervals = {}
        parameterIntervals['smoothingFactor'] = [
         0.0, 1.0, False, False]
        parameterIntervals['trendSmoothingFactor'] = [0.0, 1.0, False, False]
        parameterIntervals['seasonSmoothingFactor'] = [0.0, 1.0, False, False]
        return parameterIntervals

    def execute(self, timeSeries):
        """Creates a new TimeSeries containing the smoothed values.

        :return:    TimeSeries object containing the exponentially smoothed TimeSeries,
            including the forecasted values.
        :rtype:     TimeSeries
        
        :note: Currently the first normalized value is simply chosen as the starting point.
        """
        self._calculate_values_to_forecast(timeSeries)
        seasonLength = self.get_parameter('seasonLength')
        if len(timeSeries) < seasonLength:
            raise ValueError('The time series must contain at least one full season.')
        alpha = self.get_parameter('smoothingFactor')
        beta = self.get_parameter('trendSmoothingFactor')
        gamma = self.get_parameter('seasonSmoothingFactor')
        valuesToForecast = self._parameters['valuesToForecast']
        seasonValues = self.initSeasonFactors(timeSeries)
        resultList = []
        lastEstimator = 0
        for idx in xrange(len(timeSeries)):
            t = timeSeries[idx][0]
            x_t = timeSeries[idx][1]
            if idx == 0:
                lastTrend = self.initialTrendSmoothingFactors(timeSeries)
                lastEstimator = x_t
                resultList.append([t, x_t])
                continue
            lastSeasonValue = seasonValues[(idx % seasonLength)]
            estimator = alpha * x_t / lastSeasonValue + (1 - alpha) * (lastEstimator + lastTrend)
            lastTrend = beta * (estimator - lastEstimator) + (1 - beta) * lastTrend
            seasonValues[idx % seasonLength] = gamma * x_t / estimator + (1 - gamma) * lastSeasonValue
            lastEstimator = estimator
            resultList.append([t, estimator])

        currentTime = resultList[(-1)][0]
        normalizedTimeDiff = currentTime - resultList[(-2)][0]
        for m in xrange(1, valuesToForecast + 1):
            currentTime += normalizedTimeDiff
            lastSeasonValue = seasonValues[((idx + m - 1) % seasonLength)]
            forecast = (lastEstimator + m * lastTrend) * lastSeasonValue
            resultList.append([currentTime, forecast])

        return TimeSeries.from_twodim_list(resultList)

    def initSeasonFactors(self, timeSeries):
        """ Computes the initial season smoothing factors.

        :return:    Returns a list of season vectors of length "seasonLength".
        :rtype: list
        """
        seasonLength = self.get_parameter('seasonLength')
        try:
            seasonValues = self.get_parameter('seasonValues')
            assert seasonLength == len(seasonValues), "Preset Season Values have to have to be of season's length"
            return seasonValues
        except KeyError:
            pass

        seasonValues = []
        completeCycles = len(timeSeries) / seasonLength
        A = {}
        for i in xrange(seasonLength):
            c_i = 0
            for j in xrange(completeCycles):
                if j not in A:
                    A[j] = self.computeA(j, timeSeries)
                c_i += timeSeries[(seasonLength * j + i)][1] / A[j]

            c_i /= completeCycles
            seasonValues.append(c_i)

        return seasonValues

    def initialTrendSmoothingFactors(self, timeSeries):
        """ Calculate the initial Trend smoothing Factor b0.
        
        Explanation:
            http://en.wikipedia.org/wiki/Exponential_smoothing#Triple_exponential_smoothing

        :return:   Returns the initial trend smoothing factor b0
        """
        result = 0.0
        seasonLength = self.get_parameter('seasonLength')
        k = min(len(timeSeries) - seasonLength, seasonLength)
        for i in xrange(0, k):
            result += (timeSeries[(seasonLength + i)][1] - timeSeries[i][1]) / seasonLength

        return result / k

    def computeA(self, j, timeSeries):
        """ Calculates A_j. Aj is the average value of x in the jth cycle of your data

        :return:    A_j
        :rtype:     numeric
        """
        seasonLength = self.get_parameter('seasonLength')
        A_j = 0
        for i in range(seasonLength):
            A_j += timeSeries[(seasonLength * j + i)][1]

        return A_j / seasonLength