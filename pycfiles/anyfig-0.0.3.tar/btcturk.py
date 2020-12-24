# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/btcturk.py
# Compiled at: 2018-04-27 06:36:08
from anyex.base.exchange import Exchange
import base64, hashlib
from anyex.base.errors import ExchangeError

class btcturk(Exchange):

    def describe(self):
        return self.deep_extend(super(btcturk, self).describe(), {'id': 'btcturk', 
           'name': 'BTCTurk', 
           'countries': 'TR', 
           'rateLimit': 1000, 
           'has': {'CORS': True, 
                   'fetchTickers': True, 
                   'fetchOHLCV': True}, 
           'timeframes': {'1d': '1d'}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27992709-18e15646-64a3-11e7-9fa2-b0950ec7712f.jpg', 
                    'api': 'https://www.btcturk.com/api', 
                    'www': 'https://www.btcturk.com', 
                    'doc': 'https://github.com/BTCTrader/broker-api-docs'}, 
           'api': {'public': {'get': [
                                    'ohlcdata',
                                    'orderbook',
                                    'ticker',
                                    'trades']}, 
                   'private': {'get': [
                                     'balance',
                                     'openOrders',
                                     'userTransactions'], 
                               'post': [
                                      'exchange',
                                      'cancelOrder']}}, 
           'markets': {'BTC/TRY': {'id': 'BTCTRY', 'symbol': 'BTC/TRY', 'base': 'BTC', 'quote': 'TRY', 'maker': 0.00236, 'taker': 0.00413}, 'ETH/TRY': {'id': 'ETHTRY', 'symbol': 'ETH/TRY', 'base': 'ETH', 'quote': 'TRY', 'maker': 0.00236, 'taker': 0.00413}, 'XRP/TRY': {'id': 'XRPTRY', 'symbol': 'XRP/TRY', 'base': 'XRP', 'quote': 'TRY', 'maker': 0.00236, 'taker': 0.00413}, 'ETH/BTC': {'id': 'ETHBTC', 'symbol': 'ETH/BTC', 'base': 'ETH', 'quote': 'BTC', 'maker': 0.00236, 'taker': 0.00413}}})

    def fetch_balance(self, params={}):
        response = self.privateGetBalance()
        result = {'info': response}
        base = {'free': response['bitcoin_available'], 
           'used': response['bitcoin_reserved'], 
           'total': response['bitcoin_balance']}
        quote = {'free': response['money_available'], 
           'used': response['money_reserved'], 
           'total': response['money_balance']}
        symbol = self.symbols[0]
        market = self.markets[symbol]
        result[market['base']] = base
        result[market['quote']] = quote
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        market = self.market(symbol)
        orderbook = self.publicGetOrderbook(self.extend({'pairSymbol': market['id']}, params))
        timestamp = int(orderbook['timestamp'] * 1000)
        return self.parse_order_book(orderbook, timestamp)

    def parse_ticker(self, ticker, market=None):
        symbol = None
        if market:
            symbol = market['symbol']
        timestamp = int(ticker['timestamp']) * 1000
        last = float(ticker['last'])
        return {'symbol': symbol, 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'high': float(ticker['high']), 
           'low': float(ticker['low']), 
           'bid': float(ticker['bid']), 
           'bidVolume': None, 
           'ask': float(ticker['ask']), 
           'askVolume': None, 
           'vwap': None, 
           'open': float(ticker['open']), 
           'close': last, 
           'last': last, 
           'previousClose': None, 
           'change': None, 
           'percentage': None, 
           'average': float(ticker['average']), 
           'baseVolume': float(ticker['volume']), 
           'quoteVolume': None, 
           'info': ticker}

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        tickers = self.publicGetTicker(params)
        result = {}
        for i in range(0, len(tickers)):
            ticker = tickers[i]
            symbol = ticker['pair']
            market = None
            if symbol in self.markets_by_id:
                market = self.markets_by_id[symbol]
                symbol = market['symbol']
            result[symbol] = self.parse_ticker(ticker, market)

        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        tickers = self.fetch_tickers()
        result = None
        if symbol in tickers:
            result = tickers[symbol]
        return result

    def parse_trade(self, trade, market):
        timestamp = trade['date'] * 1000
        return {'id': trade['tid'], 
           'info': trade, 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'symbol': market['symbol'], 
           'type': None, 
           'side': None, 
           'price': trade['price'], 
           'amount': trade['amount']}

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        market = self.market(symbol)
        response = self.publicGetTrades(self.extend({'pairSymbol': market['id']}, params))
        return self.parse_trades(response, market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1d', since=None, limit=None):
        timestamp = self.parse8601(ohlcv['Time'])
        return [
         timestamp,
         ohlcv['Open'],
         ohlcv['High'],
         ohlcv['Low'],
         ohlcv['Close'],
         ohlcv['Volume']]

    def fetch_ohlcv(self, symbol, timeframe='1d', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {}
        if limit is not None:
            request['last'] = limit
        response = self.publicGetOhlcdata(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        order = {'PairSymbol': self.market_id(symbol), 
           'OrderType': 0 if side == 'buy' else 1, 
           'OrderMethod': 1 if type == 'market' else 0}
        if type == 'market':
            if 'Total' not in list(params.keys()):
                raise ExchangeError(self.id + ' createOrder requires the "Total" extra parameter for market orders(amount and price are both ignored)')
        else:
            order['Price'] = price
            order['Amount'] = amount
        response = self.privatePostExchange(self.extend(order, params))
        return {'info': response, 
           'id': response['id']}

    def cancel_order(self, id, symbol=None, params={}):
        return self.privatePostCancelOrder({'id': id})

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        if self.id == 'btctrader':
            raise ExchangeError(self.id + ' is an abstract base API for BTCExchange, BTCTurk')
        url = self.urls['api'] + '/' + path
        if api == 'public':
            if params:
                url += '?' + self.urlencode(params)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            body = self.urlencode(params)
            secret = base64.b64decode(self.secret)
            auth = self.apiKey + nonce
            headers = {'X-PCK': self.apiKey, 
               'X-Stamp': nonce, 
               'X-Signature': base64.b64encode(self.hmac(self.encode(auth), secret, hashlib.sha256, 'binary')), 
               'Content-Type': 'application/x-www-form-urlencoded'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}