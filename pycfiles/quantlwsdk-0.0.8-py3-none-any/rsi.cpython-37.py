# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\technical\rsi.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 5089 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from six.moves import xrange
from pyalgotrade import technical

def gain_loss_one(prevValue, nextValue):
    change = nextValue - prevValue
    if change < 0:
        gain = 0
        loss = abs(change)
    else:
        gain = change
        loss = 0
    return (
     gain, loss)


def avg_gain_loss(values, begin, end):
    rangeLen = end - begin
    if rangeLen < 2:
        return
    gain = 0
    loss = 0
    for i in xrange(begin + 1, end):
        currGain, currLoss = gain_loss_one(values[(i - 1)], values[i])
        gain += currGain
        loss += currLoss

    return (
     gain / float(rangeLen - 1), loss / float(rangeLen - 1))


class RSIEventWindow(technical.EventWindow):

    def __init__(self, period):
        assert period > 1
        super(RSIEventWindow, self).__init__(period + 1)
        self._RSIEventWindow__value = None
        self._RSIEventWindow__prevGain = None
        self._RSIEventWindow__prevLoss = None
        self._RSIEventWindow__period = period

    def onNewValue(self, dateTime, value):
        super(RSIEventWindow, self).onNewValue(dateTime, value)
        if value is not None:
            if self.windowFull():
                if self._RSIEventWindow__prevGain is None:
                    assert self._RSIEventWindow__prevLoss is None
                    avgGain, avgLoss = avg_gain_loss(self.getValues(), 0, len(self.getValues()))
                else:
                    assert self._RSIEventWindow__prevLoss is not None
                    prevValue = self.getValues()[(-2)]
                    currValue = self.getValues()[(-1)]
                    currGain, currLoss = gain_loss_one(prevValue, currValue)
                    avgGain = (self._RSIEventWindow__prevGain * (self._RSIEventWindow__period - 1) + currGain) / float(self._RSIEventWindow__period)
                    avgLoss = (self._RSIEventWindow__prevLoss * (self._RSIEventWindow__period - 1) + currLoss) / float(self._RSIEventWindow__period)
                if avgLoss == 0:
                    self._RSIEventWindow__value = 100
                else:
                    rs = avgGain / avgLoss
                    self._RSIEventWindow__value = 100 - 100 / (1 + rs)
                self._RSIEventWindow__prevGain = avgGain
                self._RSIEventWindow__prevLoss = avgLoss

    def getValue(self):
        return self._RSIEventWindow__value


class RSI(technical.EventBasedFilter):
    __doc__ = 'Relative Strength Index filter as described in http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi.\n\n    :param dataSeries: The DataSeries instance being filtered.\n    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.\n    :param period: The period. Note that if period is **n**, then **n+1** values are used. Must be > 1.\n    :type period: int.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, dataSeries, period, maxLen=None):
        super(RSI, self).__init__(dataSeries, RSIEventWindow(period), maxLen)