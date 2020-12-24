# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/technical/macd.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
from pyalgotrade.technical import ma
from pyalgotrade import dataseries

class MACD(dataseries.SequenceDataSeries):
    """Moving Average Convergence-Divergence indicator as described in http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:moving_average_convergence_divergence_macd.

    :param dataSeries: The DataSeries instance being filtered.
    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.
    :param fastEMA: The number of values to use to calculate the fast EMA.
    :type fastEMA: int.
    :param slowEMA: The number of values to use to calculate the slow EMA.
    :type slowEMA: int.
    :param signalEMA: The number of values to use to calculate the signal EMA.
    :type signalEMA: int.
    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """

    def __init__(self, dataSeries, fastEMA, slowEMA, signalEMA, maxLen=None):
        assert fastEMA > 0
        assert slowEMA > 0
        assert fastEMA < slowEMA
        assert signalEMA > 0
        super(MACD, self).__init__(maxLen)
        self.__fastEMASkip = slowEMA - fastEMA
        self.__fastEMAWindow = ma.EMAEventWindow(fastEMA)
        self.__slowEMAWindow = ma.EMAEventWindow(slowEMA)
        self.__signalEMAWindow = ma.EMAEventWindow(signalEMA)
        self.__signal = dataseries.SequenceDataSeries(maxLen)
        self.__histogram = dataseries.SequenceDataSeries(maxLen)
        dataSeries.getNewValueEvent().subscribe(self.__onNewValue)

    def getSignal(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the EMA over the MACD."""
        return self.__signal

    def getHistogram(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the histogram (the difference between the MACD and the Signal)."""
        return self.__histogram

    def __onNewValue(self, dataSeries, dateTime, value):
        diff = None
        macdValue = None
        signalValue = None
        histogramValue = None
        self.__slowEMAWindow.onNewValue(dateTime, value)
        if self.__fastEMASkip > 0:
            self.__fastEMASkip -= 1
        else:
            self.__fastEMAWindow.onNewValue(dateTime, value)
            if self.__fastEMAWindow.windowFull():
                diff = self.__fastEMAWindow.getValue() - self.__slowEMAWindow.getValue()
        self.__signalEMAWindow.onNewValue(dateTime, diff)
        if self.__signalEMAWindow.windowFull():
            macdValue = diff
            signalValue = self.__signalEMAWindow.getValue()
            histogramValue = macdValue - signalValue
        self.appendWithDateTime(dateTime, macdValue)
        self.__signal.appendWithDateTime(dateTime, signalValue)
        self.__histogram.appendWithDateTime(dateTime, histogramValue)
        return