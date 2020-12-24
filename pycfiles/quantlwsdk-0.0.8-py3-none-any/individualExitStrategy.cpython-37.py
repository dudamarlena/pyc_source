# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\strategy\individualExitStrategy.py
# Compiled at: 2020-04-10 07:25:53
# Size of source mod 2**32: 21556 bytes
"""
.. moduleauthor:: lw
用来处理独立出场逻辑
"""
from gm.api import *
from pyalgotrade import commonHelpBylw
from pyalgotrade import gm3HelpBylw
from pyalgotrade import dataseries
from pyalgotrade.broker import gmEnum
import copy
from pyalgotrade import loggerHelpbylw
import pandas as pd

class timeExitStrategy:

    def __init__(self, symbol, **kwargs):
        i = 1
        self.symbol = symbol
        self.context = kwargs.get('context', None)
        self.exitTime = kwargs.get('exitTime', None)
        underLySym = commonHelpBylw.getMainContinContract(symbol)
        self.orderLog = loggerHelpbylw.getFileLogger((self.context.bTestID + '-' + underLySym + '-orderlog'), ('log\\' + self.context.bTestID + '\\' + underLySym + '-orderRecord.txt'),
          mode_='a')

    def runbar4exitAfterTime(self, barTime):
        if barTime[11:16] >= self.exitTime:
            if barTime[11:16] < '16:00':
                if self.context.normalLog is not None:
                    self.context.normalLog.info('%s,%s', barTime, 'timeExit in')
                symbolHolding = self.context.account().position(symbol=(self.symbol), side=PositionSide_Long)
                if symbolHolding:
                    vol_ = symbolHolding['volume']
                    clearLongOrderRes = gm3HelpBylw.gmOrder.clearLong((self.symbol), vol_, 'time-cLong', barTime, ordrLog=(self.orderLog), context=(self.context))
                symbolHolding = self.context.account().position(symbol=(self.symbol), side=PositionSide_Short)
                if symbolHolding:
                    vol_ = symbolHolding['volume']
                    clearShortOrderRes = gm3HelpBylw.gmOrder.clearShort((self.symbol), vol_, 'time-cShort', barTime, orderLog=(self.orderLog), context=(self.context))
                return True
        return False


def clearPositionByDeliveryDay(positions, nextTradeDate, context, moveOrderLog=None, orderType=2):
    if len(positions) <= 0:
        return
    from pandas.tseries.offsets import MonthBegin
    symbolList = []
    dt = context.now.strftime('%Y-%m-%d %H:%M:%S')
    for aposition in positions:
        aSymbol = aposition.symbol
        symbolList.append(aSymbol)

    instuInfo = gm3HelpBylw.getInstumInfo(symbolList)
    for aposition in positions:
        aSymbol = aposition.symbol
        delistDate = instuInfo.loc[(instuInfo['symbol'] == aSymbol, 'delisted_date')].iloc[0]
        deliveryMothDate = pd.Timestamp(delistDate) + MonthBegin(-1)
        deliveryMothDate = deliveryMothDate.strftime('%Y-%m-%d')
        nextTradeMothDate = nextTradeDate[0:8] + '01'
        delistDateStr = delistDate.strftime('%Y-%m-%d')
        clearFlag = False
        controlList = [
         'SHFE.fu2005', 'SHFE.fu2009']
        if aSymbol not in controlList:
            if nextTradeMothDate >= deliveryMothDate:
                clearFlag = True
        elif nextTradeDate >= delistDateStr:
            clearFlag = True
        if clearFlag:
            vol_ = aposition['volume']
            side_ = aposition['side']
        if side_ == PositionSide_Long:
            if orderType == 2:
                gm3HelpBylw.gmOrder.clearLong(aSymbol, vol_, 'Delivery-cLong', dt, orderLog=(context.orderLog),
                  context=context)
            if orderType == 5:
                gm3HelpBylw.gmOrder.clearLongWithNdang(aSymbol, vol_, 'Delivery-cLong', dt, orderLog=(context.orderLog),
                  context=context)
            if moveOrderLog is not None:
                moveOrderLog.info('%s,%s,%s', aSymbol, vol_, '卖平')
            if side_ == PositionSide_Short:
                if orderType == 2:
                    gm3HelpBylw.gmOrder.clearShort(aSymbol, vol_, 'Delivery-cShort', dt, orderLog=(context.orderLog),
                      context=context)
                if orderType == 5:
                    gm3HelpBylw.gmOrder.clearShortWithNdang(aSymbol, vol_, 'Delivery-cShort', dt, orderLog=(context.orderLog),
                      context=context)
                if moveOrderLog is not None:
                    moveOrderLog.info('%s,%s,%s', aSymbol, vol_, '买平')