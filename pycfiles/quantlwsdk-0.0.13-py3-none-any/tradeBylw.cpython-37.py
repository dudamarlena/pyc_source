# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\tradeBylw.py
# Compiled at: 2020-05-12 02:39:52
# Size of source mod 2**32: 5138 bytes
"""
20200410 lw

"""
import pandas as pd, pymongo
from pyalgotrade.utils import gmEnum
from pyalgotrade import calendayBylw
import datetime
from datetime import timezone, timedelta
import re

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
        self.aNewTradeCalendar = calendayBylw.getACalendarInstance()

    def addARecordFromGm(self, gmTrade, updateWrite=False, adjustID=False):
        tempdict = {}
        if adjustID:
            exchange = gmTrade['symbol'].split('.')[0]
            id_ = re.sub('[CZCE|DCE|SHFE|:]', '', gmTrade['exec_id'])
            id_ = id_.strip()
            if exchange == 'SHFE':
                id_ = id_.rjust(12, '0')
            tempdict['_id'] = id_
        else:
            tempdict['_id'] = gmTrade['exec_id']
        tempdict['symbol'] = gmTrade['symbol']
        tempdict['positionEffect'] = gmTrade['position_effect']
        tempdict['side'] = gmTrade['side']
        tempdict['price'] = gmTrade['price']
        tempdict['volume'] = gmTrade['volume']
        sourceDtStr = gmTrade['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        realDtStr = self.aNewTradeCalendar.getRealDateTime(tempdict['symbol'], sourceDtStr[0:10], sourceDtStr[11:])
        tempdict['created_at'] = datetime.datetime.strptime(realDtStr, '%Y-%m-%d %H:%M:%S')
        tempdict['created_at'] = tempdict['created_at'].replace(tzinfo=(timezone(timedelta(hours=8))))
        if not updateWrite:
            self.collection.insert_one(tempdict)
        else:
            self.collection.save(tempdict)

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