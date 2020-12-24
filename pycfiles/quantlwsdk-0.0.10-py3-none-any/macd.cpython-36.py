# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\technical\macd.py
# Compiled at: 2019-07-15 22:34:54
# Size of source mod 2**32: 4695 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade.technical import ma
from pyalgotrade import dataseries

class MACD(dataseries.SequenceDataSeries):
    __doc__ = 'Moving Average Convergence-Divergence indicator as described in http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:moving_average_convergence_divergence_macd.\n\n    :param dataSeries: The DataSeries instance being filtered.\n    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.\n    :param fastEMA: The number of values to use to calculate the fast EMA.\n    :type fastEMA: int.\n    :param slowEMA: The number of values to use to calculate the slow EMA.\n    :type slowEMA: int.\n    :param signalEMA: The number of values to use to calculate the signal EMA.\n    :type signalEMA: int.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, dataSeries, fastEMA, slowEMA, signalEMA, maxLen=None):
        if not fastEMA > 0:
            raise AssertionError
        else:
            if not slowEMA > 0:
                raise AssertionError
            elif not fastEMA < slowEMA:
                raise AssertionError
            assert signalEMA > 0
        super(MACD, self).__init__(maxLen)
        self._MACD__fastEMASkip = slowEMA - fastEMA
        self._MACD__fastEMAWindow = ma.EMAEventWindow(fastEMA)
        self._MACD__slowEMAWindow = ma.EMAEventWindow(slowEMA)
        self._MACD__signalEMAWindow = ma.EMAEventWindow(signalEMA)
        self._MACD__signal = dataseries.SequenceDataSeries(maxLen)
        self._MACD__histogram = dataseries.SequenceDataSeries(maxLen)
        dataSeries.getNewValueEvent().subscribe(self._MACD__onNewValue)

    def getSignal(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the EMA over the MACD."""
        return self._MACD__signal

    def getHistogram(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the histogram (the difference between the MACD and the Signal)."""
        return self._MACD__histogram

    def __onNewValue(self, dataSeries, dateTime, value):
        diff = None
        macdValue = None
        signalValue = None
        histogramValue = None
        self._MACD__slowEMAWindow.onNewValue(dateTime, value)
        if self._MACD__fastEMASkip > 0:
            self._MACD__fastEMASkip -= 1
        else:
            self._MACD__fastEMAWindow.onNewValue(dateTime, value)
        if self._MACD__fastEMAWindow.windowFull():
            diff = self._MACD__fastEMAWindow.getValue() - self._MACD__slowEMAWindow.getValue()
            macdValue = diff
        self._MACD__signalEMAWindow.onNewValue(dateTime, diff)
        if self._MACD__signalEMAWindow.windowFull():
            signalValue = self._MACD__signalEMAWindow.getValue()
            histogramValue = macdValue - signalValue
        self.appendWithDateTime(dateTime, macdValue)
        self._MACD__signal.appendWithDateTime(dateTime, signalValue)
        self._MACD__histogram.appendWithDateTime(dateTime, histogramValue)