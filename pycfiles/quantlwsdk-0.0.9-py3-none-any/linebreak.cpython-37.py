# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\technical\linebreak.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 5225 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import dataseries
from pyalgotrade.dataseries import bards

class Line(object):
    __doc__ = 'A line in a line break chart.'

    def __init__(self, low, high, dateTime, white):
        self._Line__low = low
        self._Line__high = high
        self._Line__dateTime = dateTime
        self._Line__white = white

    def getDateTime(self):
        """The datetime."""
        return self._Line__dateTime

    def getLow(self):
        """The low value."""
        return self._Line__low

    def getHigh(self):
        """The high value."""
        return self._Line__high

    def isWhite(self):
        """True if the line is white (rising prices)."""
        return self._Line__white

    def isBlack(self):
        """True if the line is black (falling prices)."""
        return not self._Line__white


class LineBreak(dataseries.SequenceDataSeries):
    __doc__ = "Line Break filter as described in http://stockcharts.com/school/doku.php?id=chart_school:chart_analysis:three_line_break.\n    .\n    This is a DataSeries of :class:`Line` instances.\n\n    :param barDataSeries: The DataSeries instance being filtered.\n    :type barDataSeries: :class:`pyalgotrade.dataseries.bards.BarDataSeries`.\n    :param reversalLines: The number of lines back to check to calculate a reversal. Must be greater than 1.\n    :type reversalLines: int.\n    :param useAdjustedValues: True to use adjusted high/low/close values.\n    :type useAdjustedValues: boolean.\n    :param maxLen: The maximum number of values to hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n        This value can't be smaller than reversalLines.\n    :type maxLen: int.\n    "

    def __init__(self, barDataSeries, reversalLines, useAdjustedValues=False, maxLen=None):
        if not isinstance(barDataSeries, bards.BarDataSeries):
            raise Exception('barDataSeries must be a dataseries.bards.BarDataSeries instance')
        if reversalLines < 2:
            raise Exception('reversalLines must be greater than 1')
        if dataseries.get_checked_max_len(maxLen) < reversalLines:
            raise Exception("maxLen can't be smaller than reversalLines")
        super(LineBreak, self).__init__(maxLen)
        self._LineBreak__reversalLines = reversalLines
        self._LineBreak__useAdjustedValues = useAdjustedValues
        barDataSeries.getNewValueEvent().subscribe(self._LineBreak__onNewBar)

    def __onNewBar(self, dataSeries, dateTime, value):
        line = self._LineBreak__getNextLine(value)
        if line is not None:
            self.appendWithDateTime(dateTime, line)

    def __isReversal(self, value, breakUp):
        if not len(self):
            raise AssertionError
        else:
            lines = self[self._LineBreak__reversalLines * -1:]
            if breakUp:
                breakPoint = max([line.getHigh() for line in lines])
                ret = value > breakPoint
            else:
                breakPoint = min([line.getLow() for line in lines])
            ret = value < breakPoint
        return ret

    def __getNextLine(self, bar):
        ret = None
        if len(self) > 0:
            lastLine = self[(-1)]
            close = bar.getClose(self._LineBreak__useAdjustedValues)
            if lastLine.isWhite():
                if close > lastLine.getHigh():
                    ret = Line(lastLine.getHigh(), close, bar.getDateTime(), True)
            elif self._LineBreak__isReversal(close, False):
                ret = Line(close, lastLine.getLow(), bar.getDateTime(), False)
            elif close < lastLine.getLow():
                ret = Line(close, lastLine.getLow(), bar.getDateTime(), False)
            elif self._LineBreak__isReversal(close, True):
                ret = Line(lastLine.getHigh(), close, bar.getDateTime(), True)
            else:
                white = False
                if bar.getClose(self._LineBreak__useAdjustedValues) >= bar.getOpen(self._LineBreak__useAdjustedValues):
                    white = True
        else:
            ret = Line(bar.getLow(self._LineBreak__useAdjustedValues), bar.getHigh(self._LineBreak__useAdjustedValues), bar.getDateTime(), white)
        return ret

    def setMaxLen(self, maxLen):
        if maxLen < self._LineBreak__reversalLines:
            raise Exception("maxLen can't be smaller than reversalLines")
        super(LineBreak, self).setMaxLen(maxLen)