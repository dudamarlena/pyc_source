# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/technical/hurst.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import numpy as np
from pyalgotrade import technical

def hurst_exp(p, minLags, maxLags):
    tau = []
    lagvec = []
    for lag in range(minLags, maxLags):
        pp = np.subtract(p[lag:], p[:-lag])
        lagvec.append(lag)
        tau.append(np.sqrt(np.std(pp)))

    m = np.polyfit(np.log10(lagvec), np.log10(tau), 1)
    hurst = m[0] * 2
    return hurst


class HurstExponentEventWindow(technical.EventWindow):

    def __init__(self, period, minLags, maxLags, logValues=True):
        super(HurstExponentEventWindow, self).__init__(period)
        self.__minLags = minLags
        self.__maxLags = maxLags
        self.__logValues = logValues

    def onNewValue(self, dateTime, value):
        if value is not None and self.__logValues:
            value = np.log10(value)
        super(HurstExponentEventWindow, self).onNewValue(dateTime, value)
        return

    def getValue(self):
        ret = None
        if self.windowFull():
            ret = hurst_exp(self.getValues(), self.__minLags, self.__maxLags)
        return ret


class HurstExponent(technical.EventBasedFilter):
    """Hurst exponent filter.

    :param dataSeries: The DataSeries instance being filtered.
    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.
    :param period: The number of values to use to calculate the hurst exponent.
    :type period: int.
    :param minLags: The minimum number of lags to use. Must be >= 2.
    :type minLags: int.
    :param maxLags: The maximum number of lags to use. Must be > minLags.
    :type maxLags: int.
    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded
        from the opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """

    def __init__(self, dataSeries, period, minLags=2, maxLags=20, logValues=True, maxLen=None):
        assert period > 0, 'period must be > 0'
        assert minLags >= 2, 'minLags must be >= 2'
        assert maxLags > minLags, 'maxLags must be > minLags'
        super(HurstExponent, self).__init__(dataSeries, HurstExponentEventWindow(period, minLags, maxLags, logValues), maxLen)