# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\technical\ma.py
# Compiled at: 2020-04-04 05:11:32
# Size of source mod 2**32: 6912 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import numpy as np
from pyalgotrade import technical
from pyalgotrade import commonHelpBylw

class SMAEventWindow(technical.EventWindow):

    def __init__(self, period):
        assert period > 0
        super(SMAEventWindow, self).__init__(period)
        self._SMAEventWindow__value = None

    def onNewValue(self, dateTime, value):
        super(SMAEventWindow, self).onNewValue(dateTime, value)
        if value is not None:
            if self.windowFull():
                self._SMAEventWindow__value = commonHelpBylw.round_up(self.getValues().mean(), 4)
                i = 1

    def getValue(self):
        return self._SMAEventWindow__value


class SMA(technical.EventBasedFilter):
    __doc__ = 'Simple Moving Average filter.\n\n    :param dataSeries: The DataSeries instance being filtered.\n    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.\n    :param period: The number of values to use to calculate the SMA.\n    :type period: int.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, dataSeries, period, maxLen=None):
        super(SMA, self).__init__(dataSeries, SMAEventWindow(period), maxLen)


class EMAEventWindow(technical.EventWindow):

    def __init__(self, period):
        assert period > 1
        super(EMAEventWindow, self).__init__(period)
        self._EMAEventWindow__multiplier = 2.0 / (period + 1)
        self._EMAEventWindow__value = None

    def onNewValue(self, dateTime, value):
        super(EMAEventWindow, self).onNewValue(dateTime, value)
        if value is not None:
            if self.windowFull():
                if self._EMAEventWindow__value is None:
                    self._EMAEventWindow__value = self.getValues().mean()
                else:
                    self._EMAEventWindow__value = (value - self._EMAEventWindow__value) * self._EMAEventWindow__multiplier + self._EMAEventWindow__value
                self._EMAEventWindow__value = commonHelpBylw.round_up(self._EMAEventWindow__value, 2)

    def getValue(self):
        return self._EMAEventWindow__value


class EMA(technical.EventBasedFilter):
    __doc__ = 'Exponential Moving Average filter.\n\n    :param dataSeries: The DataSeries instance being filtered.\n    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.\n    :param period: The number of values to use to calculate the EMA. Must be an integer greater than 1.\n    :type period: int.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, dataSeries, period, maxLen=None):
        super(EMA, self).__init__(dataSeries, EMAEventWindow(period), maxLen)


class WMAEventWindow(technical.EventWindow):

    def __init__(self, weights):
        assert len(weights) > 0
        super(WMAEventWindow, self).__init__(len(weights))
        self._WMAEventWindow__weights = np.asarray(weights)

    def getValue(self):
        ret = None
        if self.windowFull():
            accum = (self.getValues() * self._WMAEventWindow__weights).sum()
            weightSum = self._WMAEventWindow__weights.sum()
            ret = accum / float(weightSum)
        return ret


class WMA(technical.EventBasedFilter):
    __doc__ = 'Weighted Moving Average filter.\n\n    :param dataSeries: The DataSeries instance being filtered.\n    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.\n    :param weights: A list of int/float with the weights.\n    :type weights: list.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, dataSeries, weights, maxLen=None):
        super(WMA, self).__init__(dataSeries, WMAEventWindow(weights), maxLen)