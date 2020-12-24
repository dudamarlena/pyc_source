# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\feed\seqFeedBylw.py
# Compiled at: 2019-02-26 04:41:50
# Size of source mod 2**32: 4474 bytes
"""
Created on Sun Dec  2 22:19:16 2018

@author: SH
"""
from pyalgotrade import dataseries
from pyalgotrade import feed
from pyalgotrade import commonHelpBylw

class serialFeed(feed.BaseOuterFeed):

    def __init__(self, frequency, maxLen=None):
        super(serialFeed, self).__init__(maxLen)
        self._serialFeed__frequency = frequency
        self._serialFeed__currDatetime = None
        self._serialFeed__currValue = None

    def createDataSeries(self, key, maxLen):
        ret = dataseries.SequenceDataSeries(maxLen)
        return ret

    def setACurrValue(self, datetime_, value):
        self._serialFeed__currDatetime = datetime_
        self._serialFeed__currValue = value

    def stop(self):
        pass

    def start(self):
        pass

    def join(self):
        pass

    def getNextValues(self):
        return (
         self._serialFeed__currDatetime, self._serialFeed__currValue)

    def peekDateTime(self):
        pass

    def eof(self):
        pass


class serialMainContractsFeed(serialFeed):
    __doc__ = '\n    这个类用来处理 主力连续的 一系列数据\n\n    '

    def __init__(self, mainContractData, frequency, maxLen=None):
        super(serialMainContractsFeed, self).__init__(frequency, maxLen)
        self._serialMainContractsFeed__mainContractData = mainContractData

    def getCurrHotSymbol(self, mainContract, date_):
        aHotSymbol = self._serialMainContractsFeed__mainContractData.loc[(date_, mainContract)]
        return aHotSymbol

    def getHotContractNextTDays(self, symbol, currTDays):
        if self._serialMainContractsFeed__mainContractData is not None:
            nextTradeDates = self.calendarObj.tradingDaysOffset(currTDays, 1)
            if nextTradeDates is not None:
                mainContract = commonHelpBylw.getMainContinContract(symbol)
                nextSymbol = self._serialMainContractsFeed__mainContractData.loc[(nextTradeDates, mainContract)]
                return nextSymbol

    def getHotContractCurrDays(self, symbol, currTDays):
        mainContract = commonHelpBylw.getMainContinContract(symbol)
        currMainSymbol = self._serialMainContractsFeed__mainContractData.loc[(currTDays, mainContract)]
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

    def isHotChangeTDays(self, symbol, currTDays):
        flag = False
        nexHotSymbol = self.getHotContractNextTDays(symbol, currTDays)
        currHotSymbol = self.getHotContractCurrDays(symbol, currTDays)
        if currHotSymbol != nexHotSymbol:
            if symbol == currHotSymbol:
                flag = True
        return flag