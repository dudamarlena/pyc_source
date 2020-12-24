# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\technical\valleyPattern.py
# Compiled at: 2019-07-21 23:05:31
# Size of source mod 2**32: 6085 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import dataseries
from pyalgotrade.technical import lw_crossSeries
from pyalgotrade.technical import ma

class GoldValley(dataseries.SequenceDataSeries):
    __doc__ = '\n    '

    def __init__(self, shortSeries, middleSeries, longSeries, maxLen=None):
        super(GoldValley, self).__init__(maxLen)
        longSeries.getNewValueEvent().subscribe(self._GoldValley__onNewValue)
        self._GoldValley__shortMiddCross = lw_crossSeries.crossSignals(shortSeries, middleSeries)
        self._GoldValley__shortLongCross = lw_crossSeries.crossSignals(shortSeries, longSeries)
        self._GoldValley__middLongCross = lw_crossSeries.crossSignals(middleSeries, longSeries)
        self.shortMiddGoldCrossFlag = False
        self.shortLongGoldCrossFlag = False
        self.middleLongGoldCrossFlag = False

    def __onNewValue(self):
        if len(self._GoldValley__shortMiddCross) >= 1:
            if self._GoldValley__shortMiddCross[(-1)] is None:
                return
        else:
            return
            if self._GoldValley__shortMiddCross[(-1)] == 1:
                self.shortMiddGoldCrossFlag = True
            if self._GoldValley__shortMiddCross[(-1)] == -1:
                self.shortMiddGoldCrossFlag = False
            if len(self._GoldValley__shortLongCross) >= 1:
                if self._GoldValley__shortLongCross[(-1)] is None:
                    return
            else:
                return
                if self._GoldValley__shortLongCross[(-1)] == 1:
                    self.shortLongGoldCrossFlag = True
                if self._GoldValley__shortLongCross[(-1)] == -1:
                    self.shortLongGoldCrossFlag = False
                if len(self._GoldValley__middLongCross) >= 2:
                    if self._GoldValley__middLongCross[(-2)] is None:
                        return
                else:
                    return
            dtFromDs3 = self._GoldValley__middLongCross.getDateTimes()[(-1)]
            if self.shortMiddGoldCrossFlag and self.shortLongGoldCrossFlag and self._GoldValley__middLongCross[(-1)] == 1 and self._GoldValley__middLongCross[(-2)] != 1:
                self.appendWithDateTime(dtFromDs3, 1)
            else:
                self.appendWithDateTime(dtFromDs3, -88)


class valleySignal(dataseries.SequenceDataSeries):
    __doc__ = '\n    '

    def __init__(self, dataSeries, shortPeriod, middlePeriod, longPeriod, maxLen=None):
        super(valleySignal, self).__init__(maxLen)
        maxLen = 20
        self._valleySignal__maShort = ma.SMA(dataSeries, period=shortPeriod, maxLen=maxLen)
        self._valleySignal__maMid = ma.SMA(dataSeries, period=middlePeriod, maxLen=maxLen)
        self._valleySignal__maLong = ma.SMA(dataSeries, period=longPeriod, maxLen=maxLen)
        self._valleySignal__shortMiddCross = lw_crossSeries.crossSignals((self._valleySignal__maShort), (self._valleySignal__maMid), maxLen=maxLen)
        self._valleySignal__shortLongCross = lw_crossSeries.crossSignals((self._valleySignal__maShort), (self._valleySignal__maLong), maxLen=maxLen)
        self._valleySignal__middLongCross = lw_crossSeries.crossSignals((self._valleySignal__maMid), (self._valleySignal__maLong), maxLen=maxLen)
        dataSeries.getNewValueEvent().subscribe(self._valleySignal__onNewValue)
        self.shortMiddGoldCrossFlag = 0
        self.shortLongGoldCrossFlag = 0
        self.middleLongGoldCrossFlag = 0

    def __onNewValue(self, dataSeries, dateTime, value):
        if len(self._valleySignal__shortMiddCross) >= 1:
            if self._valleySignal__shortMiddCross[(-1)] is None:
                return
        else:
            return
            if self._valleySignal__shortMiddCross[(-1)] == 1:
                self.shortMiddGoldCrossFlag = 1
            if self._valleySignal__shortMiddCross[(-1)] == -1:
                self.shortMiddGoldCrossFlag = -1
            if len(self._valleySignal__shortLongCross) >= 1:
                if self._valleySignal__shortLongCross[(-1)] is None:
                    return
            else:
                return
                if self._valleySignal__shortLongCross[(-1)] == 1:
                    self.shortLongGoldCrossFlag = 1
                if self._valleySignal__shortLongCross[(-1)] == -1:
                    self.shortLongGoldCrossFlag = -1
                if len(self._valleySignal__middLongCross) >= 2:
                    if self._valleySignal__middLongCross[(-2)] is None:
                        return
                else:
                    return
            sigvalue = 0
            dtFromDs3 = self._valleySignal__middLongCross.getDateTimes()[(-1)]
            if self.shortMiddGoldCrossFlag == 1:
                if self.shortLongGoldCrossFlag == 1:
                    if self._valleySignal__middLongCross[(-1)] == 1:
                        if self._valleySignal__middLongCross[(-2)] != 1:
                            sigvalue = 1
            if self.shortMiddGoldCrossFlag == -1:
                if self.shortLongGoldCrossFlag == -1:
                    if self._valleySignal__middLongCross[(-1)] == -1:
                        if self._valleySignal__middLongCross[(-2)] != -1:
                            sigvalue = -1
        self.appendWithDateTime(dtFromDs3, sigvalue)