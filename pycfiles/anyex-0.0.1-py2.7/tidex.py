# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/tidex.py
# Compiled at: 2018-04-27 06:35:19
from anyex.liqui import liqui
import math

class tidex(liqui):

    def describe(self):
        return self.deep_extend(super(tidex, self).describe(), {'id': 'tidex', 
           'name': 'Tidex', 
           'countries': 'UK', 
           'rateLimit': 2000, 
           'version': '3', 
           'has': {'fetchCurrencies': True}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/30781780-03149dc4-a12e-11e7-82bb-313b269d24d4.jpg', 
                    'api': {'web': 'https://web.tidex.com/api', 
                            'public': 'https://api.tidex.com/api/3', 
                            'private': 'https://api.tidex.com/tapi'}, 
                    'www': 'https://tidex.com', 
                    'doc': 'https://tidex.com/exchange/public-api', 
                    'fees': [
                           'https://tidex.com/exchange/assets-spec',
                           'https://tidex.com/exchange/pairs-spec']}, 
           'api': {'web': {'get': [
                                 'currency',
                                 'pairs',
                                 'tickers',
                                 'orders',
                                 'ordershistory',
                                 'trade-data',
                                 'trade-data/{id}']}}, 
           'fees': {'trading': {'tierBased': False, 
                                'percentage': True, 
                                'taker': 0.1 / 100, 
                                'maker': 0.1 / 100}}, 
           'commonCurrencies': {'MGO': 'WMGO', 
                                'EMGO': 'MGO'}})

    def fetch_currencies(self, params={}):
        currencies = self.webGetCurrency(params)
        result = {}
        for i in range(0, len(currencies)):
            currency = currencies[i]
            id = currency['symbol']
            precision = currency['amountPoint']
            code = id.upper()
            code = self.common_currency_code(code)
            active = currency['visible'] is True
            status = 'ok'
            if not active:
                status = 'disabled'
            canWithdraw = currency['withdrawEnable'] is True
            canDeposit = currency['depositEnable'] is True
            if not canWithdraw or not canDeposit:
                active = False
            result[code] = {'id': id, 'code': code, 
               'name': currency['name'], 
               'active': active, 
               'status': status, 
               'precision': precision, 
               'funding': {'withdraw': {'active': canWithdraw, 
                                        'fee': currency['withdrawFee']}, 
                           'deposit': {'active': canDeposit, 
                                       'fee': 0.0}}, 
               'limits': {'amount': {'min': None, 
                                     'max': math.pow(10, precision)}, 
                          'price': {'min': math.pow(10, -precision), 
                                    'max': math.pow(10, precision)}, 
                          'cost': {'min': None, 
                                   'max': None}, 
                          'withdraw': {'min': currency['withdrawMinAmout'], 
                                       'max': None}, 
                          'deposit': {'min': currency['depositMinAmount'], 
                                      'max': None}}, 
               'info': currency}

        return result

    def get_version_string(self):
        return ''