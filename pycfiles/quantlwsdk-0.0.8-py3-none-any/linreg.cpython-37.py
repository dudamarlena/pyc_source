# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\technical\linreg.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 5667 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import technical
from pyalgotrade.utils import collections
from pyalgotrade.utils import dt
import numpy as np
from scipy import stats

def lsreg(x, y):
    x = np.asarray(x)
    y = np.asarray(y)
    res = stats.linregress(x, y)
    return (res[0], res[1])


class LeastSquaresRegressionWindow(technical.EventWindow):

    def __init__(self, windowSize):
        assert windowSize > 1
        super(LeastSquaresRegressionWindow, self).__init__(windowSize)
        self._timestamps = collections.NumPyDeque(windowSize)

    def onNewValue(self, dateTime, value):
        technical.EventWindow.onNewValue(self, dateTime, value)
        if value is not None:
            timestamp = dt.datetime_to_timestamp(dateTime)
            if len(self._timestamps):
                assert timestamp > self._timestamps[(-1)]
            self._timestamps.append(timestamp)

    def __getValueAtImpl(self, timestamp):
        ret = None
        if self.windowFull():
            a, b = lsreg(self._timestamps.data(), self.getValues())
            ret = a * timestamp + b
        return ret

    def getValueAt(self, dateTime):
        return self._LeastSquaresRegressionWindow__getValueAtImpl(dt.datetime_to_timestamp(dateTime))

    def getValue(self):
        ret = None
        if self.windowFull():
            ret = self._LeastSquaresRegressionWindow__getValueAtImpl(self._timestamps.data()[(-1)])
        return ret


class LeastSquaresRegression(technical.EventBasedFilter):
    __doc__ = 'Calculates values based on a least-squares regression.\n\n    :param dataSeries: The DataSeries instance being filtered.\n    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.\n    :param windowSize: The number of values to use to calculate the regression.\n    :type windowSize: int.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, dataSeries, windowSize, maxLen=None):
        super(LeastSquaresRegression, self).__init__(dataSeries, LeastSquaresRegressionWindow(windowSize), maxLen)

    def getValueAt(self, dateTime):
        """Calculates the value at a given time based on the regression line.

        :param dateTime: The datetime to calculate the value at.
            Will return None if there are not enough values in the underlying DataSeries.
        :type dateTime: :class:`datetime.datetime`.
        """
        return self.getEventWindow().getValueAt(dateTime)


class SlopeEventWindow(technical.EventWindow):

    def __init__(self, windowSize):
        super(SlopeEventWindow, self).__init__(windowSize)
        self._SlopeEventWindow__x = np.asarray(range(windowSize))

    def getValue(self):
        ret = None
        if self.windowFull():
            y = self.getValues()
            ret = lsreg(self._SlopeEventWindow__x, y)[0]
        return ret


class Slope(technical.EventBasedFilter):
    __doc__ = 'The Slope filter calculates the slope of a least-squares regression line.\n\n    :param dataSeries: The DataSeries instance being filtered.\n    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.\n    :param period: The number of values to use to calculate the slope.\n    :type period: int.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n\n    .. note::\n        This filter ignores the time elapsed between the different values.\n    '

    def __init__(self, dataSeries, period, maxLen=None):
        super(Slope, self).__init__(dataSeries, SlopeEventWindow(period), maxLen)


class TrendEventWindow(SlopeEventWindow):

    def __init__(self, windowSize, positiveThreshold, negativeThreshold):
        if negativeThreshold > positiveThreshold:
            raise Exception('Invalid thresholds')
        super(TrendEventWindow, self).__init__(windowSize)
        self._TrendEventWindow__positiveThreshold = positiveThreshold
        self._TrendEventWindow__negativeThreshold = negativeThreshold

    def getValue(self):
        ret = super(TrendEventWindow, self).getValue()
        if ret is not None:
            if ret > self._TrendEventWindow__positiveThreshold:
                ret = True
            else:
                if ret < self._TrendEventWindow__negativeThreshold:
                    ret = False
                else:
                    ret = None
        return ret


class Trend(technical.EventBasedFilter):

    def __init__(self, dataSeries, trendDays, positiveThreshold=0, negativeThreshold=0, maxLen=None):
        super(Trend, self).__init__(dataSeries, TrendEventWindow(trendDays, positiveThreshold, negativeThreshold), maxLen)