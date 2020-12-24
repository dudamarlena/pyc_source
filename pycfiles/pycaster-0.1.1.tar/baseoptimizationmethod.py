# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/optimization/baseoptimizationmethod.py
# Compiled at: 2015-05-28 03:51:38
import types
from pycast.errors import BaseErrorMeasure
from pycast.common import PyCastObject

class BaseOptimizationMethod(PyCastObject):
    """Baseclass for all optimization methods."""

    def __init__(self, errorMeasureClass, errorMeasureInitializationParameters=None, precision=-1):
        r"""Initializes the optimization method.

        :param BaseErrorMeasure errorMeasureClass:    Error measure class from :py:mod:`pycast.errors`.
        :param dictionary errorMeasureInitializationParameters:    Parameters used to initialize
            the errorMeasureClass. This dictionary will be passed to the errorMeasureClass as \*\*kwargs.
        :param integer precision:    Defines the accuracy for parameter tuning in 10^precision.
            This parameter has to be an integer in [-7, 0].

        :raise:    Raises a :py:exc:`TypeError` if errorMeasureClass is not a valid class.
            Valid classes are derived from :py:class:`pycast.errors.BaseErrorMeasure`.
        :raise:    Raises a :py:exc:`ValueError` if precision is not in [-7, 0].
        """
        if errorMeasureInitializationParameters == None:
            errorMeasureInitializationParameters = {}
        if not isinstance(errorMeasureClass, (type, types.ClassType)):
            raise TypeError('errorMeasureClass has to be of type pycast.errors.BaseErrorMeasure or of an inherited class.')
        if not issubclass(errorMeasureClass, BaseErrorMeasure):
            raise TypeError('errorMeasureClass has to be of type pycast.errors.BaseErrorMeasure or of an inherited class.')
        if not -7 <= precision <= 0:
            raise ValueError('precision has to be in [-7,0].')
        super(BaseOptimizationMethod, self).__init__()
        self._precison = int(precision)
        self._errorClass = errorMeasureClass
        self._errorMeasureKWArgs = errorMeasureInitializationParameters
        return

    def optimize(self, timeSeries, forecastingMethods=None):
        """Runs the optimization on the given TimeSeries.

        :param TimeSeries timeSeries:    TimeSeries instance that requires an optimized forecast.
        :param list forecastingMethods:    List of forecastingMethods that will be used for optimization.

        :return:    Returns the optimized forecasting method with the smallest error.
        :rtype:     (BaseForecastingMethod, Dictionary)

        :raise:    Raises a :py:exc:`ValueError` ValueError if no forecastingMethods is empty.
        """
        if forecastingMethods == None or len(forecastingMethods) == 0:
            raise ValueError('forecastingMethods cannot be empty.')
        return