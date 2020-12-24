# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/bitbay.py
# Compiled at: 2018-04-27 06:36:21
from anyex.base.exchange import Exchange
try:
    basestring
except NameError:
    basestring = str

import hashlib, json
from anyex.base.errors import ExchangeError
from anyex.base.errors import AuthenticationError
from anyex.base.errors import InsufficientFunds
from anyex.base.errors import InvalidOrder
from anyex.base.errors import InvalidNonce

class bitbay(Exchange):

    def describe(self):
        return self.deep_extend(super(bitbay, self).describe(), {'id': 'bitbay', 
           'name': 'BitBay', 
           'countries': [
                       'PL', 'EU'], 
           'rateLimit': 1000, 
           'has': {'CORS': True, 
                   'withdraw': True}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27766132-978a7bd8-5ece-11e7-9540-bc96d1e9bbb8.jpg', 
                    'www': 'https://bitbay.net', 
                    'api': {'public': 'https://bitbay.net/API/Public', 
                            'private': 'https://bitbay.net/API/Trading/tradingApi.php'}, 
                    'doc': [
                          'https://bitbay.net/public-api',
                          'https://bitbay.net/account/tab-api',
                          'https://github.com/BitBayNet/API'], 
                    'fees': 'https://bitbay.net/en/fees'}, 
           'api': {'public': {'get': [
                                    '{id}/all',
                                    '{id}/market',
                                    '{id}/orderbook',
                                    '{id}/ticker',
                                    '{id}/trades']}, 
                   'private': {'post': [
                                      'info',
                                      'trade',
                                      'cancel',
                                      'orderbook',
                                      'orders',
                                      'transfer',
                                      'withdraw',
                                      'history',
                                      'transactions']}}, 
           'markets': {'BTC/USD': {'id': 'BTCUSD', 'symbol': 'BTC/USD', 'base': 'BTC', 'quote': 'USD', 'baseId': 'BTC', 'quoteId': 'USD'}, 'BTC/EUR': {'id': 'BTCEUR', 'symbol': 'BTC/EUR', 'base': 'BTC', 'quote': 'EUR', 'baseId': 'BTC', 'quoteId': 'EUR'}, 'BTC/PLN': {'id': 'BTCPLN', 'symbol': 'BTC/PLN', 'base': 'BTC', 'quote': 'PLN', 'baseId': 'BTC', 'quoteId': 'PLN'}, 'LTC/USD': {'id': 'LTCUSD', 'symbol': 'LTC/USD', 'base': 'LTC', 'quote': 'USD', 'baseId': 'LTC', 'quoteId': 'USD'}, 'LTC/EUR': {'id': 'LTCEUR', 'symbol': 'LTC/EUR', 'base': 'LTC', 'quote': 'EUR', 'baseId': 'LTC', 'quoteId': 'EUR'}, 'LTC/PLN': {'id': 'LTCPLN', 'symbol': 'LTC/PLN', 'base': 'LTC', 'quote': 'PLN', 'baseId': 'LTC', 'quoteId': 'PLN'}, 'LTC/BTC': {'id': 'LTCBTC', 'symbol': 'LTC/BTC', 'base': 'LTC', 'quote': 'BTC', 'baseId': 'LTC', 'quoteId': 'BTC'}, 'ETH/USD': {'id': 'ETHUSD', 'symbol': 'ETH/USD', 'base': 'ETH', 'quote': 'USD', 'baseId': 'ETH', 'quoteId': 'USD'}, 'ETH/EUR': {'id': 'ETHEUR', 'symbol': 'ETH/EUR', 'base': 'ETH', 'quote': 'EUR', 'baseId': 'ETH', 'quoteId': 'EUR'}, 'ETH/PLN': {'id': 'ETHPLN', 'symbol': 'ETH/PLN', 'base': 'ETH', 'quote': 'PLN', 'baseId': 'ETH', 'quoteId': 'PLN'}, 'ETH/BTC': {'id': 'ETHBTC', 'symbol': 'ETH/BTC', 'base': 'ETH', 'quote': 'BTC', 'baseId': 'ETH', 'quoteId': 'BTC'}, 'LSK/USD': {'id': 'LSKUSD', 'symbol': 'LSK/USD', 'base': 'LSK', 'quote': 'USD', 'baseId': 'LSK', 'quoteId': 'USD'}, 'LSK/EUR': {'id': 'LSKEUR', 'symbol': 'LSK/EUR', 'base': 'LSK', 'quote': 'EUR', 'baseId': 'LSK', 'quoteId': 'EUR'}, 'LSK/PLN': {'id': 'LSKPLN', 'symbol': 'LSK/PLN', 'base': 'LSK', 'quote': 'PLN', 'baseId': 'LSK', 'quoteId': 'PLN'}, 'LSK/BTC': {'id': 'LSKBTC', 'symbol': 'LSK/BTC', 'base': 'LSK', 'quote': 'BTC', 'baseId': 'LSK', 'quoteId': 'BTC'}, 'BCH/USD': {'id': 'BCCUSD', 'symbol': 'BCH/USD', 'base': 'BCH', 'quote': 'USD', 'baseId': 'BCC', 'quoteId': 'USD'}, 'BCH/EUR': {'id': 'BCCEUR', 'symbol': 'BCH/EUR', 'base': 'BCH', 'quote': 'EUR', 'baseId': 'BCC', 'quoteId': 'EUR'}, 'BCH/PLN': {'id': 'BCCPLN', 'symbol': 'BCH/PLN', 'base': 'BCH', 'quote': 'PLN', 'baseId': 'BCC', 'quoteId': 'PLN'}, 'BCH/BTC': {'id': 'BCCBTC', 'symbol': 'BCH/BTC', 'base': 'BCH', 'quote': 'BTC', 'baseId': 'BCC', 'quoteId': 'BTC'}, 'BTG/USD': {'id': 'BTGUSD', 'symbol': 'BTG/USD', 'base': 'BTG', 'quote': 'USD', 'baseId': 'BTG', 'quoteId': 'USD'}, 'BTG/EUR': {'id': 'BTGEUR', 'symbol': 'BTG/EUR', 'base': 'BTG', 'quote': 'EUR', 'baseId': 'BTG', 'quoteId': 'EUR'}, 'BTG/PLN': {'id': 'BTGPLN', 'symbol': 'BTG/PLN', 'base': 'BTG', 'quote': 'PLN', 'baseId': 'BTG', 'quoteId': 'PLN'}, 'BTG/BTC': {'id': 'BTGBTC', 'symbol': 'BTG/BTC', 'base': 'BTG', 'quote': 'BTC', 'baseId': 'BTG', 'quoteId': 'BTC'}, 'DASH/USD': {'id': 'DASHUSD', 'symbol': 'DASH/USD', 'base': 'DASH', 'quote': 'USD', 'baseId': 'DASH', 'quoteId': 'USD'}, 'DASH/EUR': {'id': 'DASHEUR', 'symbol': 'DASH/EUR', 'base': 'DASH', 'quote': 'EUR', 'baseId': 'DASH', 'quoteId': 'EUR'}, 'DASH/PLN': {'id': 'DASHPLN', 'symbol': 'DASH/PLN', 'base': 'DASH', 'quote': 'PLN', 'baseId': 'DASH', 'quoteId': 'PLN'}, 'DASH/BTC': {'id': 'DASHBTC', 'symbol': 'DASH/BTC', 'base': 'DASH', 'quote': 'BTC', 'baseId': 'DASH', 'quoteId': 'BTC'}, 'GAME/USD': {'id': 'GAMEUSD', 'symbol': 'GAME/USD', 'base': 'GAME', 'quote': 'USD', 'baseId': 'GAME', 'quoteId': 'USD'}, 'GAME/EUR': {'id': 'GAMEEUR', 'symbol': 'GAME/EUR', 'base': 'GAME', 'quote': 'EUR', 'baseId': 'GAME', 'quoteId': 'EUR'}, 'GAME/PLN': {'id': 'GAMEPLN', 'symbol': 'GAME/PLN', 'base': 'GAME', 'quote': 'PLN', 'baseId': 'GAME', 'quoteId': 'PLN'}, 'GAME/BTC': {'id': 'GAMEBTC', 'symbol': 'GAME/BTC', 'base': 'GAME', 'quote': 'BTC', 'baseId': 'GAME', 'quoteId': 'BTC'}, 'XRP/USD': {'id': 'XRPUSD', 'symbol': 'XRP/USD', 'base': 'XRP', 'quote': 'USD', 'baseId': 'XRP', 'quoteId': 'USD'}, 'XRP/EUR': {'id': 'XRPEUR', 'symbol': 'XRP/EUR', 'base': 'XRP', 'quote': 'EUR', 'baseId': 'XRP', 'quoteId': 'EUR'}, 'XRP/PLN': {'id': 'XRPPLN', 'symbol': 'XRP/PLN', 'base': 'XRP', 'quote': 'PLN', 'baseId': 'XRP', 'quoteId': 'PLN'}, 'XRP/BTC': {'id': 'XRPBTC', 'symbol': 'XRP/BTC', 'base': 'XRP', 'quote': 'BTC', 'baseId': 'XRP', 'quoteId': 'BTC'}, 'XIN/BTC': {'id': 'XINBTC', 'symbol': 'XIN/BTC', 'base': 'XIN', 'quote': 'BTC', 'baseId': 'XIN', 'quoteId': 'BTC'}}, 'fees': {'trading': {'maker': 0.3 / 100, 
                                'taker': 0.0043}, 
                    'funding': {'withdraw': {'BTC': 0.0009, 
                                             'LTC': 0.005, 
                                             'ETH': 0.00126, 
                                             'LSK': 0.2, 
                                             'BCH': 0.0006, 
                                             'GAME': 0.005, 
                                             'DASH': 0.001, 
                                             'BTG': 0.0008, 
                                             'PLN': 4, 
                                             'EUR': 1.5}}}, 
           'exceptions': {'400': ExchangeError, 
                          '401': InvalidOrder, 
                          '402': InvalidOrder, 
                          '403': InvalidOrder, 
                          '404': InvalidOrder, 
                          '405': InvalidOrder, 
                          '406': InsufficientFunds, 
                          '408': InvalidOrder, 
                          '501': AuthenticationError, 
                          '502': AuthenticationError, 
                          '503': InvalidNonce, 
                          '504': ExchangeError, 
                          '505': AuthenticationError, 
                          '506': AuthenticationError, 
                          '509': ExchangeError, 
                          '510': ExchangeError}})

    def fetch_balance(self, params={}):
        response = self.privatePostInfo()
        if 'balances' in response:
            balance = response['balances']
            result = {'info': balance}
            codes = list(self.currencies.keys())
            for i in range(0, len(codes)):
                code = codes[i]
                currency = self.currencies[code]
                id = currency['id']
                account = self.account()
                if id in balance:
                    account['free'] = float(balance[id]['available'])
                    account['used'] = float(balance[id]['locked'])
                    account['total'] = self.sum(account['free'], account['used'])
                result[code] = account

            return self.parse_balance(result)
        raise ExchangeError(self.id + ' empty balance response ' + self.json(response))

    def fetch_order_book(self, symbol, limit=None, params={}):
        orderbook = self.publicGetIdOrderbook(self.extend({'id': self.market_id(symbol)}, params))
        return self.parse_order_book(orderbook)

    def fetch_ticker(self, symbol, params={}):
        ticker = self.publicGetIdTicker(self.extend({'id': self.market_id(symbol)}, params))
        timestamp = self.milliseconds()
        baseVolume = self.safe_float(ticker, 'volume')
        vwap = self.safe_float(ticker, 'vwap')
        quoteVolume = baseVolume * vwap
        last = self.safe_float(ticker, 'last')
        return {'symbol': symbol, 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'high': self.safe_float(ticker, 'max'), 
           'low': self.safe_float(ticker, 'min'), 
           'bid': self.safe_float(ticker, 'bid'), 
           'bidVolume': None, 
           'ask': self.safe_float(ticker, 'ask'), 
           'askVolume': None, 
           'vwap': vwap, 
           'open': None, 
           'close': last, 
           'last': last, 
           'previousClose': None, 
           'change': None, 
           'percentage': None, 
           'average': self.safe_float(ticker, 'average'), 
           'baseVolume': baseVolume, 
           'quoteVolume': quoteVolume, 
           'info': ticker}

    def parse_trade(self, trade, market):
        timestamp = trade['date'] * 1000
        return {'id': trade['tid'], 
           'info': trade, 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'symbol': market['symbol'], 
           'type': None, 
           'side': trade['type'], 
           'price': trade['price'], 
           'amount': trade['amount']}

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        market = self.market(symbol)
        response = self.publicGetIdTrades(self.extend({'id': market['id']}, params))
        return self.parse_trades(response, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type != 'limit':
            raise ExchangeError(self.id + ' allows limit orders only')
        market = self.market(symbol)
        return self.privatePostTrade(self.extend({'type': side, 
           'currency': market['baseId'], 
           'amount': amount, 
           'payment_currency': market['quoteId'], 
           'rate': price}, params))

    def cancel_order(self, id, symbol=None, params={}):
        return self.privatePostCancel({'id': id})

    def is_fiat(self, currency):
        fiatCurrencies = {'USD': True, 
           'EUR': True, 
           'PLN': True}
        if currency in fiatCurrencies:
            return True
        return False

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        method = None
        currency = self.currency(code)
        request = {'currency': currency['id'], 
           'quantity': amount}
        if self.is_fiat(code):
            method = 'privatePostWithdraw'
        else:
            method = 'privatePostTransfer'
            if tag is not None:
                address += '?dt=' + str(tag)
            request['address'] = address
        response = getattr(self, method)(self.extend(request, params))
        return {'info': response, 
           'id': None}

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        if api == 'public':
            query = self.omit(params, self.extract_params(path))
            url += '/' + self.implode_params(path, params) + '.json'
            url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            body = self.urlencode(self.extend({'method': path, 
               'moment': self.nonce()}, params))
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 
               'API-Key': self.apiKey, 
               'API-Hash': self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512)}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body):
        if not isinstance(body, basestring):
            return
        if len(body) < 2:
            return
        if body[0] == '{' or body[0] == '[':
            response = json.loads(body)
            if 'code' in response:
                code = response['code']
                feedback = self.id + ' ' + self.json(response)
                exceptions = self.exceptions
                if code in self.exceptions:
                    raise exceptions[code](feedback)
                else:
                    raise ExchangeError(feedback)