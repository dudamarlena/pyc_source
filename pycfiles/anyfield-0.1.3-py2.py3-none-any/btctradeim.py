# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/btctradeim.py
# Compiled at: 2018-04-27 06:36:10
from anyex.coinegg import coinegg
from anyex.base.errors import ExchangeError

class btctradeim(coinegg):

    def describe(self):
        return self.deep_extend(super(btctradeim, self).describe(), {'id': 'btctradeim', 
           'name': 'BtcTrade.im', 
           'countries': 'HK', 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/36770531-c2142444-1c5b-11e8-91e2-a4d90dc85fe8.jpg', 
                    'api': {'web': 'https://api.btctrade.im/coin', 
                            'rest': 'https://api.btctrade.im/api/v1'}, 
                    'www': 'https://www.btctrade.im', 
                    'doc': 'https://www.btctrade.im/help.api.html', 
                    'fees': 'https://www.btctrade.im/spend.price.html'}, 
           'fees': {'trading': {'maker': 0.2 / 100, 
                                'taker': 0.2 / 100}, 
                    'funding': {'withdraw': {'BTC': 0.001}}}})

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if api == 'web':
            return response
        data = self.safe_value(response, 'data')
        if data:
            code = self.safe_string(response, 'code')
            if code != '0':
                message = self.safe_string(response, 'msg', 'Error')
                raise ExchangeError(message)
            return data
        return response