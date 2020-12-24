# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\technical\stoch.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 3531 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import technical
from pyalgotrade.dataseries import bards
from pyalgotrade.technical import ma

def get_low_high_values(useAdjusted, bars):
    currBar = bars[0]
    lowestLow = currBar.getLow(useAdjusted)
    highestHigh = currBar.getHigh(useAdjusted)
    for i in range(len(bars)):
        currBar = bars[i]
        lowestLow = min(lowestLow, currBar.getLow(useAdjusted))
        highestHigh = max(highestHigh, currBar.getHigh(useAdjusted))

    return (
     lowestLow, highestHigh)


class SOEventWindow(technical.EventWindow):

    def __init__(self, period, useAdjustedValues):
        assert period > 1
        super(SOEventWindow, self).__init__(period, dtype=object)
        self._SOEventWindow__useAdjusted = useAdjustedValues

    def getValue(self):
        ret = None
        if self.windowFull():
            lowestLow, highestHigh = get_low_high_values(self._SOEventWindow__useAdjusted, self.getValues())
            currentClose = self.getValues()[(-1)].getClose(self._SOEventWindow__useAdjusted)
            closeDelta = currentClose - lowestLow
            if closeDelta:
                ret = closeDelta / float(highestHigh - lowestLow) * 100
            else:
                ret = 0.0
        return ret


class StochasticOscillator(technical.EventBasedFilter):
    __doc__ = 'Fast Stochastic Oscillator filter as described in\n    http://stockcharts.com/school/doku.php?st=stochastic+oscillator&id=chart_school:technical_indicators:stochastic_oscillator_fast_slow_and_full.\n    Note that the value returned by this filter is %K. To access %D use :meth:`getD`.\n\n    :param barDataSeries: The BarDataSeries instance being filtered.\n    :type barDataSeries: :class:`pyalgotrade.dataseries.bards.BarDataSeries`.\n    :param period: The period. Must be > 1.\n    :type period: int.\n    :param dSMAPeriod: The %D SMA period. Must be > 1.\n    :type dSMAPeriod: int.\n    :param useAdjustedValues: True to use adjusted Low/High/Close values.\n    :type useAdjustedValues: boolean.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, barDataSeries, period, dSMAPeriod=3, useAdjustedValues=False, maxLen=None):
        assert dSMAPeriod > 1, 'dSMAPeriod must be > 1'
        assert isinstance(barDataSeries, bards.BarDataSeries), 'barDataSeries must be a dataseries.bards.BarDataSeries instance'
        super(StochasticOscillator, self).__init__(barDataSeries, SOEventWindow(period, useAdjustedValues), maxLen)
        self._StochasticOscillator__d = ma.SMA(self, dSMAPeriod, maxLen)

    def getD(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the %D values."""
        return self._StochasticOscillator__d