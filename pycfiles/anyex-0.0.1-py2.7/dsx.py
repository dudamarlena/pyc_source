# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/dsx.py
# Compiled at: 2018-04-27 06:35:56
from anyex.liqui import liqui
import hashlib

class dsx(liqui):

    def describe(self):
        return self.deep_extend(super(dsx, self).describe(), {'id': 'dsx', 
           'name': 'DSX', 
           'countries': 'UK', 
           'rateLimit': 1500, 
           'has': {'CORS': False, 
                   'fetchOrder': True, 
                   'fetchOrders': True, 
                   'fetchOpenOrders': True, 
                   'fetchClosedOrders': True, 
                   'fetchTickers': True, 
                   'fetchMyTrades': True}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27990275-1413158a-645a-11e7-931c-94717f7510e3.jpg', 
                    'api': {'public': 'https://dsx.uk/mapi', 
                            'private': 'https://dsx.uk/tapi', 
                            'dwapi': 'https://dsx.uk/dwapi'}, 
                    'www': 'https://dsx.uk', 
                    'doc': [
                          'https://api.dsx.uk',
                          'https://dsx.uk/api_docs/public',
                          'https://dsx.uk/api_docs/private',
                          '']}, 
           'api': {'public': {'get': [
                                    'barsFromMoment/{id}/{period}/{start}',
                                    'depth/{pair}',
                                    'info',
                                    'lastBars/{id}/{period}/{amount}',
                                    'periodBars/{id}/{period}/{start}/{end}',
                                    'ticker/{pair}',
                                    'trades/{pair}']}, 
                   'private': {'post': [
                                      'getInfo',
                                      'TransHistory',
                                      'TradeHistory',
                                      'OrderHistory',
                                      'ActiveOrders',
                                      'Trade',
                                      'CancelOrder']}, 
                   'dwapi': {'post': [
                                    'getCryptoDepositAddress',
                                    'cryptoWithdraw',
                                    'fiatWithdraw',
                                    'getTransactionStatus',
                                    'getTransactions']}}})

    def get_base_quote_from_market_id(self, id):
        uppercase = id.upper()
        base = uppercase[0:3]
        quote = uppercase[3:6]
        base = self.common_currency_code(base)
        quote = self.common_currency_code(quote)
        return [base, quote]

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostGetInfo()
        balances = response['return']
        result = {'info': balances}
        funds = balances['funds']
        currencies = list(funds.keys())
        for c in range(0, len(currencies)):
            currency = currencies[c]
            uppercase = currency.upper()
            uppercase = self.common_currency_code(uppercase)
            account = {'free': funds[currency], 
               'used': 0.0, 
               'total': balances['total'][currency]}
            account['used'] = account['total'] - account['free']
            result[uppercase] = account

        return self.parse_balance(result)

    def parse_ticker(self, ticker, market=None):
        timestamp = ticker['updated'] * 1000
        symbol = None
        if market:
            symbol = market['symbol']
        average = self.safe_float(ticker, 'avg')
        if average is not None:
            if average > 0:
                average = 1 / average
        last = self.safe_float(ticker, 'last')
        return {'symbol': symbol, 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'high': self.safe_float(ticker, 'high'), 
           'low': self.safe_float(ticker, 'low'), 
           'bid': self.safe_float(ticker, 'buy'), 
           'bidVolume': None, 
           'ask': self.safe_float(ticker, 'sell'), 
           'askVolume': None, 
           'vwap': None, 
           'open': None, 
           'close': last, 
           'last': last, 
           'previousClose': None, 
           'change': None, 
           'percentage': None, 
           'average': average, 
           'baseVolume': self.safe_float(ticker, 'vol'), 
           'quoteVolume': self.safe_float(ticker, 'vol_cur'), 
           'info': ticker}

    def get_order_id_key(self):
        return 'orderId'

    def sign_body_with_secret(self, body):
        return self.decode(self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512, 'base64'))

    def get_version_string(self):
        return ''