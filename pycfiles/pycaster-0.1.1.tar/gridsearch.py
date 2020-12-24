# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/optimization/gridsearch.py
# Compiled at: 2015-05-28 05:25:17
from pycast.optimization import BaseOptimizationMethod

class GridSearch(BaseOptimizationMethod):
    """Implements the grid search method for parameter optimization. 

    GridSearch is the brute force method.
    """

    def optimize(self, timeSeries, forecastingMethods=None, startingPercentage=0.0, endPercentage=100.0):
        """Runs the optimization of the given TimeSeries.

        :param TimeSeries timeSeries:    TimeSeries instance that requires an optimized forecast.
        :param list forecastingMethods:    List of forecastingMethods that will be used for optimization.
        :param float startingPercentage: Defines the start of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, where the error calculation should be started. 
            25.0 for example means that the first 25% of all calculated errors will be ignored.
        :param float endPercentage:    Defines the end of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, after which all error values will be ignored. 90.0 for example means that
            the last 10% of all local errors will be ignored.

        :return:    Returns the optimized forecasting method, the corresponding error measure and the forecasting methods
            parameters.
        :rtype:     [BaseForecastingMethod, BaseErrorMeasure, Dictionary]

        :raise:    Raises a :py:exc:`ValueError` ValueError if no forecastingMethods is empty.
        """
        if forecastingMethods == None or len(forecastingMethods) == 0:
            raise ValueError('forecastingMethods cannot be empty.')
        self._startingPercentage = startingPercentage
        self._endPercentage = endPercentage
        results = []
        for forecastingMethod in forecastingMethods:
            results.append([forecastingMethod] + self.optimize_forecasting_method(timeSeries, forecastingMethod))

        bestForecastingMethod = min(results, key=lambda item: item[1].get_error(self._startingPercentage, self._endPercentage))
        for parameter in bestForecastingMethod[2]:
            bestForecastingMethod[0].set_parameter(parameter, bestForecastingMethod[2][parameter])

        return bestForecastingMethod

    def _generate_next_parameter_value(self, parameter, forecastingMethod):
        """Generator for a specific parameter of the given forecasting method.

        :param string parameter:    Name of the parameter the generator is used for.
        :param BaseForecastingMethod forecastingMethod:    Instance of a ForecastingMethod.

        :return:    Creates a generator used to iterate over possible parameters.
        :rtype:     generator
        """
        interval = forecastingMethod.get_interval(parameter)
        precision = 10 ** self._precison
        startValue = interval[0]
        endValue = interval[1]
        if not interval[2]:
            startValue += precision
        if interval[3]:
            endValue += precision
        while startValue < endValue:
            parameterValue = startValue
            yield parameterValue
            startValue += precision

    def optimize_forecasting_method(self, timeSeries, forecastingMethod):
        """Optimizes the parameters for the given timeSeries and forecastingMethod.

        :param TimeSeries timeSeries:    TimeSeries instance, containing hte original data.
        :param BaseForecastingMethod forecastingMethod:    ForecastingMethod that is used to optimize the parameters.

        :return: Returns a tuple containing only the smallest BaseErrorMeasure instance as defined in
            :py:meth:`BaseOptimizationMethod.__init__` and the forecastingMethods parameter.
        :rtype: tuple
        """
        tuneableParameters = forecastingMethod.get_optimizable_parameters()
        remainingParameters = []
        for tuneableParameter in tuneableParameters:
            remainingParameters.append([tuneableParameter, [ item for item in self._generate_next_parameter_value(tuneableParameter, forecastingMethod) ]])

        forecastingResults = self.optimization_loop(timeSeries, forecastingMethod, remainingParameters)
        bestForecastingResult = min(forecastingResults, key=lambda item: item[0].get_error(self._startingPercentage, self._endPercentage))
        return bestForecastingResult

    def optimization_loop(self, timeSeries, forecastingMethod, remainingParameters, currentParameterValues=None):
        """The optimization loop.

        This function is called recursively, until all parameter values were evaluated.

        :param TimeSeries timeSeries:    TimeSeries instance that requires an optimized forecast.
        :param BaseForecastingMethod forecastingMethod:    ForecastingMethod that is used to optimize the parameters.
        :param list remainingParameters:    List containing all parameters with their corresponding values that still
            need to be evaluated.
            When this list is empty, the most inner optimization loop is reached.
        :param dictionary currentParameterValues:    The currently evaluated forecast parameter combination.

        :return: Returns a list containing a BaseErrorMeasure instance as defined in
            :py:meth:`BaseOptimizationMethod.__init__` and the forecastingMethods parameter.
        :rtype: list
        """
        if currentParameterValues == None:
            currentParameterValues = {}
        if 0 == len(remainingParameters):
            for parameter in currentParameterValues:
                forecastingMethod.set_parameter(parameter, currentParameterValues[parameter])

            forecast = timeSeries.apply(forecastingMethod)
            error = self._errorClass(**self._errorMeasureKWArgs)
            if not error.initialize(timeSeries, forecast):
                return []
            return [
             [
              error, dict(currentParameterValues)]]
        else:
            localParameter = remainingParameters[(-1)]
            localParameterName = localParameter[0]
            localParameterValues = localParameter[1]
            results = []
            for value in localParameterValues:
                currentParameterValues[localParameterName] = value
                remainingParameters = remainingParameters[:-1]
                results += self.optimization_loop(timeSeries, forecastingMethod, remainingParameters, currentParameterValues)

            return results