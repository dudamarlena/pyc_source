# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/technical/ma.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
import numpy as np
from pyalgotrade import technical

class SMAEventWindow(technical.EventWindow):

    def __init__(self, period):
        assert period > 0
        super(SMAEventWindow, self).__init__(period)
        self.__value = None
        return

    def onNewValue(self, dateTime, value):
        firstValue = None
        if len(self.getValues()) > 0:
            firstValue = self.getValues()[0]
            assert firstValue is not None
        super(SMAEventWindow, self).onNewValue(dateTime, value)
        if value is not None and self.windowFull():
            if self.__value is None:
                self.__value = self.getValues().mean()
            else:
                self.__value = self.__value + value / float(self.getWindowSize()) - firstValue / float(self.getWindowSize())
        return

    def getValue(self):
        return self.__value


class SMA(technical.EventBasedFilter):
    """Simple Moving Average filter.

    :param dataSeries: The DataSeries instance being filtered.
    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.
    :param period: The number of values to use to calculate the SMA.
    :type period: int.
    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """

    def __init__(self, dataSeries, period, maxLen=None):
        super(SMA, self).__init__(dataSeries, SMAEventWindow(period), maxLen)


class EMAEventWindow(technical.EventWindow):

    def __init__(self, period):
        assert period > 1
        super(EMAEventWindow, self).__init__(period)
        self.__multiplier = 2.0 / (period + 1)
        self.__value = None
        return

    def onNewValue(self, dateTime, value):
        super(EMAEventWindow, self).onNewValue(dateTime, value)
        if value is not None and self.windowFull():
            if self.__value is None:
                self.__value = self.getValues().mean()
            else:
                self.__value = (value - self.__value) * self.__multiplier + self.__value
        return

    def getValue(self):
        return self.__value


class EMA(technical.EventBasedFilter):
    """Exponential Moving Average filter.

    :param dataSeries: The DataSeries instance being filtered.
    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.
    :param period: The number of values to use to calculate the EMA. Must be an integer greater than 1.
    :type period: int.
    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """

    def __init__(self, dataSeries, period, maxLen=None):
        super(EMA, self).__init__(dataSeries, EMAEventWindow(period), maxLen)


class WMAEventWindow(technical.EventWindow):

    def __init__(self, weights):
        assert len(weights) > 0
        super(WMAEventWindow, self).__init__(len(weights))
        self.__weights = np.asarray(weights)

    def getValue(self):
        ret = None
        if self.windowFull():
            accum = (self.getValues() * self.__weights).sum()
            weightSum = self.__weights.sum()
            ret = accum / float(weightSum)
        return ret


class WMA(technical.EventBasedFilter):
    """Weighted Moving Average filter.

    :param dataSeries: The DataSeries instance being filtered.
    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.
    :param weights: A list of int/float with the weights.
    :type weights: list.
    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """

    def __init__(self, dataSeries, weights, maxLen=None):
        super(WMA, self).__init__(dataSeries, WMAEventWindow(weights), maxLen)