# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/chbtc.py
# Compiled at: 2018-04-27 06:36:06
from anyex.zb import zb
from anyex.base.errors import ExchangeError

class chbtc(zb):

    def describe(self):
        return self.deep_extend(super(chbtc, self).describe(), {'id': 'chbtc', 
           'name': 'CHBTC', 
           'countries': 'CN', 
           'rateLimit': 1000, 
           'version': 'v1', 
           'has': {'CORS': False, 
                   'fetchOrder': True}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/28555659-f0040dc2-7109-11e7-9d99-688a438bf9f4.jpg', 
                    'api': {'public': 'http://api.chbtc.com/data', 
                            'private': 'https://trade.chbtc.com/api'}, 
                    'www': 'https://trade.chbtc.com/api', 
                    'doc': 'https://www.chbtc.com/i/developer'}, 
           'markets': {'BTC/CNY': {'id': 'btc_cny', 'symbol': 'BTC/CNY', 'base': 'BTC', 'quote': 'CNY'}, 'LTC/CNY': {'id': 'ltc_cny', 'symbol': 'LTC/CNY', 'base': 'LTC', 'quote': 'CNY'}, 'ETH/CNY': {'id': 'eth_cny', 'symbol': 'ETH/CNY', 'base': 'ETH', 'quote': 'CNY'}, 'ETC/CNY': {'id': 'etc_cny', 'symbol': 'ETC/CNY', 'base': 'ETC', 'quote': 'CNY'}, 'BTS/CNY': {'id': 'bts_cny', 'symbol': 'BTS/CNY', 'base': 'BTS', 'quote': 'CNY'}, 'BCH/CNY': {'id': 'bcc_cny', 'symbol': 'BCH/CNY', 'base': 'BCH', 'quote': 'CNY'}, 'HSR/CNY': {'id': 'hsr_cny', 'symbol': 'HSR/CNY', 'base': 'HSR', 'quote': 'CNY'}, 'QTUM/CNY': {'id': 'qtum_cny', 'symbol': 'QTUM/CNY', 'base': 'QTUM', 'quote': 'CNY'}}})

    def get_market_field_name(self):
        return 'currency'

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if api == 'private':
            if 'code' in response:
                raise ExchangeError(self.id + ' ' + self.json(response))
        if 'result' in response:
            if not response['result']:
                raise ExchangeError(self.id + ' ' + self.json(response))
        return response