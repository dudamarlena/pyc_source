# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\../gm3\indicatorModule\pyalgotrade\technical\bollinger.py
# Compiled at: 2019-06-05 03:26:15
# Size of source mod 2**32: 3146 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import dataseries
from pyalgotrade.technical import ma
from pyalgotrade.technical import stats

class BollingerBands(object):
    __doc__ = 'Bollinger Bands filter as described in http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:bollinger_bands.\n\n    :param dataSeries: The DataSeries instance being filtered.\n    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.\n    :param period: The number of values to use in the calculation. Must be > 1.\n    :type period: int.\n    :param numStdDev: The number of standard deviations to use for the upper and lower bands.\n    :type numStdDev: int.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n    '

    def __init__(self, dataSeries, period, numStdDev, maxLen=None):
        self._BollingerBands__sma = ma.SMA(dataSeries, period, maxLen=maxLen)
        self._BollingerBands__stdDev = stats.StdDev(dataSeries, period, maxLen=maxLen)
        self._BollingerBands__upperBand = dataseries.SequenceDataSeries(maxLen)
        self._BollingerBands__lowerBand = dataseries.SequenceDataSeries(maxLen)
        self._BollingerBands__numStdDev = numStdDev
        dataSeries.getNewValueEvent().subscribe(self._BollingerBands__onNewValue)

    def __onNewValue(self, dataSeries, dateTime, value):
        upperValue = None
        lowerValue = None
        if value is not None:
            sma = self._BollingerBands__sma[(-1)]
            if sma is not None:
                stdDev = self._BollingerBands__stdDev[(-1)]
                upperValue = sma + stdDev * self._BollingerBands__numStdDev
                lowerValue = sma + stdDev * self._BollingerBands__numStdDev * -1
        self._BollingerBands__upperBand.appendWithDateTime(dateTime, upperValue)
        self._BollingerBands__lowerBand.appendWithDateTime(dateTime, lowerValue)

    def getUpperBand(self):
        """
        Returns the upper band as a :class:`pyalgotrade.dataseries.DataSeries`.
        """
        return self._BollingerBands__upperBand

    def getMiddleBand(self):
        """
        Returns the middle band as a :class:`pyalgotrade.dataseries.DataSeries`.
        """
        return self._BollingerBands__sma

    def getLowerBand(self):
        """
        Returns the lower band as a :class:`pyalgotrade.dataseries.DataSeries`.
        """
        return self._BollingerBands__lowerBand