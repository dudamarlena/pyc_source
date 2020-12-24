# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\tradeBylw.py
# Compiled at: 2020-04-16 22:30:55
# Size of source mod 2**32: 3757 bytes
"""
20200410 lw

"""
import pandas as pd, pymongo
from pyalgotrade.utils import gmEnum
from pyalgotrade.positionHelpBylw import Positions, cusHoldingPostion

class cusTrade:

    def __init__(self, tradeId, symbol, side, positionEffect, price, volume, datetime):
        self._tradeid = tradeId
        self._symbol = symbol
        self._side = side
        self._positionEffect = positionEffect
        self._price = price
        self._volume = volume
        self._created_at = datetime
        self._targetPositionSide = self._calPositionSide()

    def _calPositionSide(self):
        if self._positionEffect in [gmEnum.PositionEffect_Close, gmEnum.PositionEffect_CloseToday,
         gmEnum.PositionEffect_CloseYesterday]:
            side_ = self._side
            if side_ == 1:
                gmPos_ = 2
            if side_ == 2:
                gmPos_ = 1
        if self._positionEffect in [gmEnum.PositionEffect_Open]:
            side_ = self._side
            gmPos_ = side_
        return gmPos_

    def getSymbol(self):
        return self._symbol

    def getSide(self):
        return self._side

    def getPositionEffect(self):
        return self._positionEffect

    def getPrice(self):
        return self._price

    def getVolume(self):
        return self._volume

    def getTradeTime(self):
        return self._created_at

    def getTargetPositionSide(self):
        return self._targetPositionSide


class mongoTrade:

    def __init__(self, dbname, collectionname, host='localhost'):
        client = pymongo.MongoClient(host=host, port=27017, tz_aware=True)
        db = client[dbname]
        self.collection = db[collectionname]

    def addARecordFromGm(self, gmTrade):
        tempdict = {}
        tempdict['_id'] = gmTrade['exec_id']
        tempdict['symbol'] = gmTrade['symbol']
        tempdict['positionEffect'] = gmTrade['position_effect']
        tempdict['side'] = gmTrade['side']
        tempdict['price'] = gmTrade['price']
        tempdict['volume'] = gmTrade['volume']
        tempdict['created_at'] = gmTrade['created_at']
        self.collection.insert_one(tempdict)

    def getAllTrades(self, timeZoneNum=8, returnType=1):
        trades = self.collection.find().sort('created_at', 1)
        if returnType == 2:
            dftrades = pd.DataFrame(list(trades))
            return dftrades
        if returnType == 1:
            cusTradeList = []
            for atrade in trades:
                acusTradeObj = cusTrade(atrade['_id'], atrade['symbol'], atrade['side'], atrade['positionEffect'], atrade['price'], atrade['volume'], atrade['created_at'])
                cusTradeList.append(acusTradeObj)

            return cusTradeList