# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\accountHelpBylw.py
# Compiled at: 2020-04-17 23:50:49
# Size of source mod 2**32: 1674 bytes
"""
20200410 lw

"""
from gm.api import get_orders, OrderSide_Buy, OrderSide_Sell, PositionEffect_Open, PositionEffect_Close, PositionEffect_CloseToday, PositionEffect_CloseYesterday
import pymongo
from datetime import timezone
from datetime import timedelta
from pyalgotrade.positionHelpBylw import Positions, cusHoldingPostion

class memoryAccount:

    def __init__(self, positions):
        self._positions = positions

    def ontrade(self, gmTrade):
        symbol_ = gmTrade.getSymbol()
        targetPositionSide = gmTrade.getTargetPositionSide()
        self._positions.get_or_create(symbol_, targetPositionSide).ontrade(gmTrade)
        self.clearZeroRecord()

    def clearZeroRecord(self):
        listKey = list(self._positions.keys())
        listKey = listKey.copy()
        for key in listKey:
            if self._positions[key].getVolume() == 0:
                del self._positions[key]

        i = 1


def _prePareMemAccout(context):
    positionsObj = Positions(cusHoldingPostion)
    cusAccout = memoryAccount(positionsObj)
    monTradeObj = mongoTrade((config.tradeDbName), (config.tradeCollectionName), host=(config.tradeDbHost))
    allstrade = monTradeObj.getAllTrades()
    for atrade in allstrade:
        cusAccout.ontrade(atrade)

    context.cusAccout = cusAccout