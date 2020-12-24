# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/btcexchange.py
# Compiled at: 2018-04-27 06:36:11
from anyex.btcturk import btcturk

class btcexchange(btcturk):

    def describe(self):
        return self.deep_extend(super(btcexchange, self).describe(), {'id': 'btcexchange', 
           'name': 'BTCExchange', 
           'countries': 'PH', 
           'rateLimit': 1500, 
           'has': {'CORS': False}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27993052-4c92911a-64aa-11e7-96d8-ec6ac3435757.jpg', 
                    'api': 'https://www.btcexchange.ph/api', 
                    'www': 'https://www.btcexchange.ph', 
                    'doc': 'https://github.com/BTCTrader/broker-api-docs'}, 
           'markets': {'BTC/PHP': {'id': 'BTC/PHP', 'symbol': 'BTC/PHP', 'base': 'BTC', 'quote': 'PHP'}}})