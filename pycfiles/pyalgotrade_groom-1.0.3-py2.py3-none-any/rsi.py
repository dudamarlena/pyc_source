# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/technical/rsi.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
from pyalgotrade import technical

def gain_loss_one(prevValue, nextValue):
    change = nextValue - prevValue
    if change < 0:
        gain = 0
        loss = abs(change)
    else:
        gain = change
        loss = 0
    return (gain, loss)


def avg_gain_loss(values, begin, end):
    rangeLen = end - begin
    if rangeLen < 2:
        return None
    else:
        gain = 0
        loss = 0
        for i in xrange(begin + 1, end):
            currGain, currLoss = gain_loss_one(values[(i - 1)], values[i])
            gain += currGain
            loss += currLoss

        return (gain / float(rangeLen - 1), loss / float(rangeLen - 1))


def rsi(values, period):
    assert period > 1
    if len(values) < period + 1:
        return None
    else:
        avgGain, avgLoss = avg_gain_loss(values, 0, period)
        for i in xrange(period, len(values)):
            gain, loss = gain_loss_one(values[(i - 1)], values[i])
            avgGain = (avgGain * (period - 1) + gain) / float(period)
            avgLoss = (avgLoss * (period - 1) + loss) / float(period)

        if avgLoss == 0:
            return 100
        rs = avgGain / avgLoss
        return 100 - 100 / (1 + rs)


class RSIEventWindow(technical.EventWindow):

    def __init__(self, period):
        assert period > 1
        super(RSIEventWindow, self).__init__(period + 1)
        self.__value = None
        self.__prevGain = None
        self.__prevLoss = None
        self.__period = period
        return

    def onNewValue(self, dateTime, value):
        super(RSIEventWindow, self).onNewValue(dateTime, value)
        if value is not None and self.windowFull():
            if self.__prevGain is None:
                assert self.__prevLoss is None
                avgGain, avgLoss = avg_gain_loss(self.getValues(), 0, len(self.getValues()))
            else:
                assert self.__prevLoss is not None
                prevValue = self.getValues()[(-2)]
                currValue = self.getValues()[(-1)]
                currGain, currLoss = gain_loss_one(prevValue, currValue)
                avgGain = (self.__prevGain * (self.__period - 1) + currGain) / float(self.__period)
                avgLoss = (self.__prevLoss * (self.__period - 1) + currLoss) / float(self.__period)
            if avgLoss == 0:
                self.__value = 100
            else:
                rs = avgGain / avgLoss
                self.__value = 100 - 100 / (1 + rs)
            self.__prevGain = avgGain
            self.__prevLoss = avgLoss
        return

    def getValue(self):
        return self.__value


class RSI(technical.EventBasedFilter):
    """Relative Strength Index filter as described in http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi.

    :param dataSeries: The DataSeries instance being filtered.
    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.
    :param period: The period. Note that if period is **n**, then **n+1** values are used. Must be > 1.
    :type period: int.
    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """

    def __init__(self, dataSeries, period, maxLen=None):
        super(RSI, self).__init__(dataSeries, RSIEventWindow(period), maxLen)