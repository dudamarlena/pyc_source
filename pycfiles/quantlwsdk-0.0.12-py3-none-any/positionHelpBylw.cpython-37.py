# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\positionHelpBylw.py
# Compiled at: 2020-05-06 22:09:14
# Size of source mod 2**32: 9785 bytes
"""
20200410 lw

"""
from gm.api import get_orders, OrderSide_Buy, OrderSide_Sell, PositionEffect_Open, PositionEffect_Close, PositionEffect_CloseToday, PositionEffect_CloseYesterday
import pymongo
from datetime import timezone
from datetime import timedelta

class Positions(dict):

    def __init__(self, position_cls):
        super(Positions, self).__init__()
        self._position_cls = position_cls
        self._cached_positions = {}

    def __missing__(self, key):
        if key not in self._cached_positions:
            self._cached_positions[key] = self._position_cls(key)
        return self._cached_positions[key]

    def get_or_create(self, symbol, positionSide):
        key = symbol + '_' + str(positionSide)
        if key not in self:
            self[key] = self._position_cls(symbol, positionSide)
        return self[key]

    def getAPosition(self, symbol, positionSide):
        key = symbol + '_' + str(positionSide)
        if key not in self:
            return
        return self[key]

    def add(self, position):
        key = position.getSymbol() + '_' + str(position.getPositionSide())
        self[key] = position


class cusHoldingPostion:

    def __init__(self, symbol, positionSide):
        self._symbol = symbol
        self._positionSide = positionSide
        self._volume = 0
        self._vwap = 0
        self._created_at = None
        self._updated_at = None
        self._available = None

    def set_state(self, state):
        self._volume = state.get('volume', 0)
        self._vwap = state.get('vwap', 0)
        self._created_at = state.get('created_at')
        self._updated_at = state.get('updated_at')
        self._available = state.get('available')

    def getAvailableVolume(self):
        return self._available

    def getVolume(self):
        return self._volume

    def getSymbol(self):
        return self._symbol

    def getPositionSide(self):
        return self._positionSide

    def getVwap(self):
        return self._vwap

    def getUpdateTime(self):
        return self._updated_at

    def ontrade(self, cusTrade):
        symbol_ = cusTrade.getSymbol()
        side_ = cusTrade.getSide()
        vol_ = cusTrade.getVolume()
        price_ = cusTrade.getPrice()
        time_ = cusTrade.getTradeTime()
        if self._created_at is None:
            self._created_at = cusTrade.getTradeTime()
        else:
            self._updated_at = cusTrade.getTradeTime()
            if cusTrade.getPositionEffect() in [PositionEffect_Close, PositionEffect_CloseToday,
             PositionEffect_CloseYesterday]:
                if not self._symbol == symbol_:
                    raise AssertionError
                else:
                    if side_ == 1:
                        assert self._positionSide == 2
                    if side_ == 2 and not self._positionSide == 1:
                        raise AssertionError
                assert self._volume >= vol_
                self._volume = self._volume - vol_
            if cusTrade.getPositionEffect() in [PositionEffect_Open]:
                assert self._symbol == symbol_
                assert self._positionSide == side_
                if self._volume < 0:
                    print('error in positions class')
                else:
                    self._vwap = (self._vwap * self._volume + price_ * vol_) / (self._volume + vol_)
                self._volume = self._volume + vol_


class mongoPosition:

    def __init__(self, dbname, collectionname, host='localhost'):
        client = pymongo.MongoClient(host=host, port=27017, tz_aware=True)
        db = client[dbname]
        self.collection = db[collectionname]

    def ontrade(self, gmTrade):
        symbol_ = gmTrade.getSymbol()
        side_ = gmTrade.getSide()
        vol_ = gmTrade.getVolume()
        price_ = gmTrade.getPrice()
        time_ = gmTrade.getTradeTime()
        psitionSide = gmTrade.getTargetPositionSide()
        idstr = symbol_ + '_' + str(psitionSide)
        if gmTrade.getPositionEffect() in [PositionEffect_Close, PositionEffect_CloseToday,
         PositionEffect_CloseYesterday]:
            self.collection.update({'_id': idstr}, {'$inc':{'vol': -vol_},  '$set':{'updated_at': time_}})
            self.collection.remove({'vol': 0})
        elif gmTrade.getPositionEffect() in [PositionEffect_Open]:
            currHolding = self.collection.find_one({'_id': idstr})
            if currHolding is not None:
                newVwap = (currHolding['vwap'] * currHolding['vol'] + price_ * vol_) / (currHolding['vol'] + vol_)
                self.collection.update({'_id': idstr}, {'$set':{'vwap':newVwap,  'updated_at':time_},  '$inc':{'vol':vol_,  'available':vol_}})
            else:
                adoc = {}
                adoc['_id'] = idstr
                adoc['vwap'] = price_
                adoc['vol'] = vol_
                adoc['created_at'] = time_
                adoc['updated_at'] = time_
                adoc['available'] = vol_
                self.collection.insert(adoc)

    def clearAll(self):
        self.collection.delete_many({})

    def getHolding(self, symbol, poside, timeZoneNum=8):
        idstr = symbol + '_' + poside
        currHolding = self.collection.find_one({'_id': idstr})
        if currHolding is not None:
            idstr = currHolding['_id']
            symbol_, positionSide = idstr.split('_')
            positionSide = int(positionSide)
            volume = currHolding['vol']
            vwap = currHolding['vwap']
            if currHolding['created_at'] is not None:
                created_at = currHolding['created_at'].astimezone(timezone(timedelta(hours=timeZoneNum)))
                updated_at = currHolding['updated_at'].astimezone(timezone(timedelta(hours=timeZoneNum)))
            else:
                created_at = currHolding['created_at']
                updated_at = currHolding['updated_at']
            available = currHolding['available']
            state = {}
            state['volume'] = volume
            state['vwap'] = vwap
            state['created_at'] = created_at
            state['updated_at'] = updated_at
            state['available'] = available
            ahol = cusHoldingPostion(symbol, positionSide)
            ahol.set_state(state)
            return ahol

    def _trasfer(self, mongoHolding, timeZoneNum):
        idstr = mongoHolding['_id']
        symbol_, positionSide = idstr.split('_')
        positionSide = int(positionSide)
        volume = mongoHolding['vol']
        vwap = mongoHolding['vwap']
        if mongoHolding['created_at'] is not None:
            created_at = mongoHolding['created_at'].astimezone(timezone(timedelta(hours=timeZoneNum)))
            updated_at = mongoHolding['updated_at'].astimezone(timezone(timedelta(hours=timeZoneNum)))
        else:
            created_at = currHolding['created_at']
            updated_at = currHolding['updated_at']
        available = mongoHolding['available']
        state = {}
        state['volume'] = volume
        state['vwap'] = vwap
        state['created_at'] = created_at
        state['updated_at'] = updated_at
        state['available'] = available
        ahol = cusHoldingPostion(symbol_, positionSide)
        ahol.set_state(state)
        return ahol

    def getPositions(self, timeZoneNum=8):
        holdings = self.collection.find()
        positionsObj = Positions(cusHoldingPostion)
        for ahol in holdings:
            commonHolding = self._trasfer(ahol, timeZoneNum)
            positionsObj.add(commonHolding)

        return positionsObj

    def setAvailableVolume(self, symbol, poside, availVol):
        idstr = symbol + '_' + str(poside)
        self.collection.update({'_id': idstr}, {'$set': {'available': availVol}})

    def addPositions(self, positionsList):
        if len(positionsList) > 0:
            self.collection.insert(positionsList)