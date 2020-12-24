# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/goncalopp/private/mydocs/programacao/python/mexbtcapi/mexbtcapi/api/mtgox/http_v1/high_level.py
# Compiled at: 2012-12-26 19:31:56
from decimal import Decimal
import functools, datetime, mexbtcapi
from mexbtcapi import concepts
from mexbtcapi.concepts.currencies import BTC
from mexbtcapi.concepts.market import Market as BaseMarket
import mtgox as low_level
MARKET_NAME = 'MtGox'

class MtgoxTicker(concepts.market.Ticker):
    TIME_PERIOD = 86400


class Market(BaseMarket):

    def __init__(self, currency):
        mexbtcapi.concepts.market.Market.__init__(self, MARKET_NAME, BTC, currency)
        self.multiplier = low_level.multiplier[currency.name]
        self.xchg_factory = functools.partial(concepts.currency.ExchangeRate, BTC, currency)

    def getTicker(self):
        data = low_level.ticker(self.c2.name)
        data2 = [ Decimal(data[name]['value_int']) / self.multiplier for name in ('high',
                                                                                  'low',
                                                                                  'avg',
                                                                                  'last',
                                                                                  'sell',
                                                                                  'buy') ]
        hi, lo, av, la, se, bu = map(self.xchg_factory, data2)
        volume = long(data['vol']['value_int'])
        time = datetime.datetime.now()
        return MtgoxTicker(market=self, time=time, high=hi, low=lo, average=av, last=la, sell=se, buy=bu)