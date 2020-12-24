# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/goncalopp/private/mydocs/programacao/python/mexbtcapi/mexbtcapi/concepts/currencies.py
# Compiled at: 2012-12-26 19:31:56
from mexbtcapi.util.constant_generator import constant_generator
from currency import Currency
names = ('BTC', 'USD', 'EUR', 'JPY', 'CAD', 'GBP', 'CHF', 'RUB', 'AUD', 'SEK', 'DKK',
         'HKD', 'PLN', 'CNY', 'SGD', 'THB', 'NZD', 'NOK')
currencies = map(Currency, names)
constant_generator(locals(), names, currencies)