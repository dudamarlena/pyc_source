# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/ethfinex.py
# Compiled at: 2018-04-27 06:35:56
from anyex.bitfinex import bitfinex

class ethfinex(bitfinex):

    def describe(self):
        return self.deep_extend(super(ethfinex, self).describe(), {'id': 'ethfinex', 
           'name': 'Ethfinex', 
           'countries': 'VG', 
           'version': 'v1', 
           'rateLimit': 1500, 
           'has': {'CORS': False, 
                   'createDepositAddress': True, 
                   'deposit': True, 
                   'fetchClosedOrders': True, 
                   'fetchDepositAddress': True, 
                   'fetchFees': True, 
                   'fetchFundingFees': True, 
                   'fetchMyTrades': True, 
                   'fetchOHLCV': True, 
                   'fetchOpenOrders': True, 
                   'fetchOrder': True, 
                   'fetchTickers': True, 
                   'fetchTradingFees': True, 
                   'withdraw': True}, 
           'timeframes': {'1m': '1m', 
                          '5m': '5m', 
                          '15m': '15m', 
                          '30m': '30m', 
                          '1h': '1h', 
                          '3h': '3h', 
                          '6h': '6h', 
                          '12h': '12h', 
                          '1d': '1D', 
                          '1w': '7D', 
                          '2w': '14D', 
                          '1M': '1M'}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/37555526-7018a77c-29f9-11e8-8835-8e415c038a18.jpg', 
                    'api': 'https://api.ethfinex.com', 
                    'www': 'https://www.ethfinex.com', 
                    'doc': [
                          'https://bitfinex.readme.io/v1/docs',
                          'https://github.com/bitfinexcom/bitfinex-api-node',
                          'https://www.ethfinex.com/api_docs']}})