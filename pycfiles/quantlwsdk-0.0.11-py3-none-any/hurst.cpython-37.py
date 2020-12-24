# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\technical\hurst.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 3256 bytes
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
        self._HurstExponentEventWindow__minLags = minLags
        self._HurstExponentEventWindow__maxLags = maxLags
        self._HurstExponentEventWindow__logValues = logValues

    def onNewValue(self, dateTime, value):
        if value is not None:
            if self._HurstExponentEventWindow__logValues:
                value = np.log10(value)
        super(HurstExponentEventWindow, self).onNewValue(dateTime, value)

    def getValue(self):
        ret = None
        if self.windowFull():
            ret = hurst_exp(self.getValues(), self._HurstExponentEventWindow__minLags, self._HurstExponentEventWindow__maxLags)
        return ret


class HurstExponent(technical.EventBasedFilter):
    __doc__ = 'Hurst exponent filter.\n\n    :param dataSeries: The DataSeries instance being filtered.\n    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.\n    :param period: The number of values to use to calculate the hurst exponent.\n    :type period: int.\n    :param minLags: The minimum number of lags to use. Must be >= 2.\n    :type minLags: int.\n    :param maxLags: The maximum number of lags to use. Must be > minLags.\n    :type maxLags: int.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded\n        from the opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, dataSeries, period, minLags=2, maxLags=20, logValues=True, maxLen=None):
        assert period > 0, 'period must be > 0'
        assert minLags >= 2, 'minLags must be >= 2'
        assert maxLags > minLags, 'maxLags must be > minLags'
        super(HurstExponent, self).__init__(dataSeries, HurstExponentEventWindow(period, minLags, maxLags, logValues), maxLen)