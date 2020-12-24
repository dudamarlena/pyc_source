# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Programmieren\dataScryer\datascryer\methods\abc_forecast.py
# Compiled at: 2016-08-15 03:23:45
import math
from abc import ABCMeta, abstractmethod
from datascryer.helper.python import python_3, xrange

class ForecastMethod:
    __metaclass__ = ABCMeta
    if python_3():
        INF = math.inf
    else:
        INF = float('inf')

    @abstractmethod
    def calc_forecast(self, options, forecast_start, forecast_range, forecast_interval, lookback_range, lookback_data):
        """
        Generates an array bases on the given data.
        :param options: dict with whatever the config passes.
        :param forecast_start: timestamp to start forecast.
        :param forecast_range: Time in seconds to forecast after start.
        :param forecast_interval: Timeinterval to forecast.
        :param lookback_range: Time in seconds of existing data.
        :param lookback_data: Two dimensional array of data of existing data.
        :return: Two dimensional array of forecasted data.
        """
        raise NotImplementedError()

    @abstractmethod
    def calc_intersection(self, options, forecast_start, forecast_range, forecast_interval, lookback_range, lookback_data, y):
        """
        Returns the x value of the intersection of the given y and the estimated forecast function.
        :param options: dict with whatever the config passes.
        :param forecast_start: timestamp to start forecast.
        :param forecast_range: Time in seconds to forecast after start.
        :param forecast_interval: Timeinterval to forecast.
        :param lookback_range: Time in seconds of existing data.
        :param lookback_data: Two dimensional array of data of existing data.
        :param y: Value to be reached.
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def gen_forecast_data(func, forecast_start, forecast_range, forecast_interval):
        return [ (x, func(x)) for x in xrange(forecast_start, forecast_start + forecast_range, forecast_interval) ]

    def gen_intersection(self, forecast_data, forecast_start, y):
        for i in range(len(forecast_data) - 1):
            if forecast_data[i][1] <= y <= forecast_data[(i + 1)][1] or forecast_data[i][1] >= y >= forecast_data[(i + 1)][1]:
                return forecast_data[i][0] - forecast_start

        return self.INF

    @staticmethod
    def sum_x_y(data, power=1):
        sum_x = 0
        sum_y = 0
        if power == 1:
            for x, y in data:
                sum_x += x
                sum_y += y

        else:
            for x, y in data:
                sum_x += pow(x, power)
                sum_y += pow(y, power)

        return (
         sum_x, sum_y)