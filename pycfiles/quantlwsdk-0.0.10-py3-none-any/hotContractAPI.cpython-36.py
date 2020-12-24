# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\hotContractAPI.py
# Compiled at: 2019-11-07 01:24:37
# Size of source mod 2**32: 5773 bytes
"""
.. moduleauthor:: lw
"""
from pyalgotrade import commonHelpBylw

class hotContractObj(object):
    __doc__ = 'A group of :class:`Bar` objects.\n\n    :param barDict: A map of instrument to :class:`Bar` objects.\n    :type barDict: map.\n\n    .. note::\n        All bars must have the same datetime.\n    '

    def __init__(self, mainContractData, calendarObj):
        self._hotContractObj__mainContractData = mainContractData
        self.calendarObj = calendarObj

    def getCurrHotSymbol(self, mainContract, date_):
        aHotSymbol = self._hotContractObj__mainContractData.loc[(date_, mainContract)]
        return aHotSymbol

    def getHotContractLastTDays(self, symbol, currTDays, mainContinueContract=None):
        if self._hotContractObj__mainContractData is not None:
            lastTradeDates = self.calendarObj.tradingDaysOffset(currTDays, -1)
            if lastTradeDates is not None:
                if not mainContinueContract:
                    mainContinueContract = commonHelpBylw.getMainContinContract(symbol)
                lastSymbol = self._hotContractObj__mainContractData.loc[(lastTradeDates, mainContinueContract)]
                return lastSymbol

    def getHotContractNextTDays(self, symbol, currTDays):
        if self._hotContractObj__mainContractData is not None:
            nextTradeDates = self.calendarObj.tradingDaysOffset(currTDays, 1)
            if nextTradeDates is not None:
                mainContract = commonHelpBylw.getMainContinContract(symbol)
                nextSymbol = self._hotContractObj__mainContractData.loc[(nextTradeDates, mainContract)]
                return nextSymbol

    def getHotContractCurrDays(self, symbol, currTDays):
        if self._hotContractObj__mainContractData.index.contains(currTDays):
            mainContract = commonHelpBylw.getMainContinContract(symbol)
            currMainSymbol = self._hotContractObj__mainContractData.loc[(currTDays, mainContract)]
        else:
            currMainSymbol = None
        return currMainSymbol

    def isHotNextTDays(self, symbol, currTDays):
        flag = False
        nextSymbol = self.getHotContractNextTDays(symbol, currTDays)
        if nextSymbol == symbol:
            flag = True
        return flag

    def isHotTDays(self, symbol, currTDays):
        flag = False
        currSymbol = self.getHotContractCurrDays(symbol, currTDays)
        if currSymbol == symbol:
            flag = True
        return flag

    def isHotLastTDays(self, symbol, currTDays):
        flag = False
        lasthotSymbol = self.getHotContractLastTDays(symbol, currTDays)
        if lasthotSymbol == symbol:
            flag = True
        return flag

    def isHotLastTDatetimes(self, symbol, aDatetime):
        lastTradingDay = self.calendarObj.tradeDateTimeTradingDateOffset(aDatetime, -1)
        lasthotSymbol = self.getHotContractCurrDays(symbol, lastTradingDay)
        flag = False
        if lasthotSymbol == symbol:
            flag = True
        return flag

    def isHotChangeTDays(self, symbol, currTDays):
        flag = False
        nexHotSymbol = self.getHotContractNextTDays(symbol, currTDays)
        currHotSymbol = self.getHotContractCurrDays(symbol, currTDays)
        if currHotSymbol != nexHotSymbol:
            if symbol == currHotSymbol:
                flag = True
        return flag

    def isNeedMovePositionNDays(self, symbol, currTDays):
        flag = False
        lastHotSymbol = self.getHotContractLastTDays(symbol, currTDays)
        currHotSymbol = self.getHotContractCurrDays(symbol, currTDays)
        if currHotSymbol != lastHotSymbol:
            if symbol == lastHotSymbol:
                flag = True
        return flag