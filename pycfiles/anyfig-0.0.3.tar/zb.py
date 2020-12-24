# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/zb.py
# Compiled at: 2018-04-27 06:35:14
from anyex.base.exchange import Exchange
try:
    basestring
except NameError:
    basestring = str

import hashlib, math, json
from anyex.base.errors import ExchangeError
from anyex.base.errors import AuthenticationError
from anyex.base.errors import InsufficientFunds
from anyex.base.errors import InvalidOrder
from anyex.base.errors import OrderNotFound
from anyex.base.errors import DDoSProtection
from anyex.base.errors import ExchangeNotAvailable

class zb(Exchange):

    def describe(self):
        return self.deep_extend(super(zb, self).describe(), {'id': 'zb', 
           'name': 'ZB', 
           'countries': 'CN', 
           'rateLimit': 1000, 
           'version': 'v1', 
           'has': {'CORS': False, 
                   'createMarketOrder': False, 
                   'fetchOrder': True, 
                   'fetchOrders': True, 
                   'fetchOpenOrders': True, 
                   'withdraw': True}, 
           'timeframes': {'1m': '1min', 
                          '3m': '3min', 
                          '5m': '5min', 
                          '15m': '15min', 
                          '30m': '30min', 
                          '1h': '1hour', 
                          '2h': '2hour', 
                          '4h': '4hour', 
                          '6h': '6hour', 
                          '12h': '12hour', 
                          '1d': '1day', 
                          '3d': '3day', 
                          '1w': '1week'}, 
           'exceptions': {'1001': ExchangeError, 
                          '1002': ExchangeError, 
                          '1003': AuthenticationError, 
                          '1004': AuthenticationError, 
                          '1005': AuthenticationError, 
                          '1006': AuthenticationError, 
                          '1009': ExchangeNotAvailable, 
                          '2001': InsufficientFunds, 
                          '2002': InsufficientFunds, 
                          '2003': InsufficientFunds, 
                          '2005': InsufficientFunds, 
                          '2006': InsufficientFunds, 
                          '2007': InsufficientFunds, 
                          '2009': InsufficientFunds, 
                          '3001': OrderNotFound, 
                          '3002': InvalidOrder, 
                          '3003': InvalidOrder, 
                          '3004': AuthenticationError, 
                          '3005': ExchangeError, 
                          '3006': AuthenticationError, 
                          '3007': AuthenticationError, 
                          '3008': OrderNotFound, 
                          '4001': ExchangeNotAvailable, 
                          '4002': DDoSProtection}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/32859187-cd5214f0-ca5e-11e7-967d-96568e2e2bd1.jpg', 
                    'api': {'public': 'http://api.zb.com/data', 
                            'private': 'https://trade.zb.com/api'}, 
                    'www': 'https://www.zb.com', 
                    'doc': 'https://www.zb.com/i/developer', 
                    'fees': 'https://www.zb.com/i/rate'}, 
           'api': {'public': {'get': [
                                    'markets',
                                    'ticker',
                                    'depth',
                                    'trades',
                                    'kline']}, 
                   'private': {'get': [
                                     'order',
                                     'cancelOrder',
                                     'getOrder',
                                     'getOrders',
                                     'getOrdersNew',
                                     'getOrdersIgnoreTradeType',
                                     'getUnfinishedOrdersIgnoreTradeType',
                                     'getAccountInfo',
                                     'getUserAddress',
                                     'getWithdrawAddress',
                                     'getWithdrawRecord',
                                     'getChargeRecord',
                                     'getCnyWithdrawRecord',
                                     'getCnyChargeRecord',
                                     'withdraw',
                                     'getLeverAssetsInfo',
                                     'getLeverBills',
                                     'transferInLever',
                                     'transferOutLever',
                                     'loan',
                                     'cancelLoan',
                                     'getLoans',
                                     'getLoanRecords',
                                     'borrow',
                                     'repay',
                                     'getRepayments']}}, 
           'fees': {'funding': {'withdraw': {'BTC': 0.0001, 
                                             'BCH': 0.0006, 
                                             'LTC': 0.005, 
                                             'ETH': 0.01, 
                                             'ETC': 0.01, 
                                             'BTS': 3, 
                                             'EOS': 1, 
                                             'QTUM': 0.01, 
                                             'HSR': 0.001, 
                                             'XRP': 0.1, 
                                             'USDT': '0.1%', 
                                             'QCASH': 5, 
                                             'DASH': 0.002, 
                                             'BCD': 0, 
                                             'UBTC': 0, 
                                             'SBTC': 0, 
                                             'INK': 20, 
                                             'TV': 0.1, 
                                             'BTH': 0, 
                                             'BCX': 0, 
                                             'LBTC': 0, 
                                             'CHAT': 20, 
                                             'bitCNY': 20, 
                                             'HLC': 20, 
                                             'BTP': 0, 
                                             'BCW': 0}}, 
                    'trading': {'maker': 0.2 / 100, 
                                'taker': 0.2 / 100}}})

    def fetch_markets(self):
        markets = self.publicGetMarkets()
        keys = list(markets.keys())
        result = []
        for i in range(0, len(keys)):
            id = keys[i]
            market = markets[id]
            baseId, quoteId = id.split('_')
            base = self.common_currency_code(baseId.upper())
            quote = self.common_currency_code(quoteId.upper())
            symbol = base + '/' + quote
            precision = {'amount': market['amountScale'], 
               'price': market['priceScale']}
            lot = math.pow(10, -precision['amount'])
            result.append({'id': id, 
               'symbol': symbol, 
               'baseId': baseId, 
               'quoteId': quoteId, 
               'base': base, 
               'quote': quote, 
               'lot': lot, 
               'active': True, 
               'precision': precision, 
               'limits': {'amount': {'min': lot, 
                                     'max': None}, 
                          'price': {'min': math.pow(10, -precision['price']), 
                                    'max': None}, 
                          'cost': {'min': 0, 
                                   'max': None}}, 
               'info': market})

        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetGetAccountInfo(params)
        balances = response['result']['coins']
        result = {'info': response}
        for i in range(0, len(balances)):
            balance = balances[i]
            account = self.account()
            currency = balance['key']
            if currency in self.currencies_by_id:
                currency = self.currencies_by_id[currency]['code']
            else:
                currency = self.common_currency_code(balance['enName'])
            account['free'] = float(balance['available'])
            account['used'] = float(balance['freez'])
            account['total'] = self.sum(account['free'], account['used'])
            result[currency] = account

        return self.parse_balance(result)

    def get_market_field_name(self):
        return 'market'

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        marketFieldName = self.get_market_field_name()
        request = {}
        request[marketFieldName] = market['id']
        orderbook = self.publicGetDepth(self.extend(request, params))
        return self.parse_order_book(orderbook)

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        marketFieldName = self.get_market_field_name()
        request = {}
        request[marketFieldName] = market['id']
        response = self.publicGetTicker(self.extend(request, params))
        ticker = response['ticker']
        timestamp = self.milliseconds()
        last = float(ticker['last'])
        return {'symbol': symbol, 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'high': float(ticker['high']), 
           'low': float(ticker['low']), 
           'bid': float(ticker['buy']), 
           'bidVolume': None, 
           'ask': float(ticker['sell']), 
           'askVolume': None, 
           'vwap': None, 
           'open': None, 
           'close': last, 
           'last': last, 
           'previousClose': None, 
           'change': None, 
           'percentage': None, 
           'average': None, 
           'baseVolume': float(ticker['vol']), 
           'quoteVolume': None, 
           'info': ticker}

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 1000
        request = {'market': market['id'], 'type': self.timeframes[timeframe], 
           'limit': limit}
        if since is not None:
            request['since'] = since
        response = self.publicGetKline(self.extend(request, params))
        return self.parse_ohlcvs(response['data'], market, timeframe, since, limit)

    def parse_trade(self, trade, market=None):
        timestamp = trade['date'] * 1000
        side = 'buy' if trade['trade_type'] == 'bid' else 'sell'
        return {'info': trade, 
           'id': str(trade['tid']), 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'symbol': market['symbol'], 
           'type': None, 
           'side': side, 
           'price': float(trade['price']), 
           'amount': float(trade['amount'])}

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        marketFieldName = self.get_market_field_name()
        request = {}
        request[marketFieldName] = market['id']
        response = self.publicGetTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type != 'limit':
            raise InvalidOrder(self.id + ' allows limit orders only')
        self.load_markets()
        order = {'price': self.price_to_precision(symbol, price), 
           'amount': self.amount_to_string(symbol, amount), 
           'tradeType': '1' if side == 'buy' else '0', 
           'currency': self.market_id(symbol)}
        response = self.privateGetOrder(self.extend(order, params))
        return {'info': response, 
           'id': response['id']}

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        order = {'id': str(id), 
           'currency': self.market_id(symbol)}
        order = self.extend(order, params)
        return self.privateGetCancelOrder(order)

    def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrder() requires a symbol argument')
        self.load_markets()
        order = {'id': str(id), 
           'currency': self.market_id(symbol)}
        order = self.extend(order, params)
        response = self.privateGetGetOrder(order)
        return self.parse_order(response, None, True)

    def fetch_orders(self, symbol=None, since=None, limit=50, params={}):
        if not symbol:
            raise ExchangeError(self.id + 'fetchOrders requires a symbol parameter')
        self.load_markets()
        market = self.market(symbol)
        request = {'currency': market['id'], 
           'pageIndex': 1, 
           'pageSize': limit}
        method = 'privateGetGetOrdersIgnoreTradeType'
        if 'tradeType' in params:
            method = 'privateGetGetOrdersNew'
        response = None
        try:
            response = getattr(self, method)(self.extend(request, params))
        except Exception as e:
            if isinstance(e, OrderNotFound):
                return []
            raise e

        return self.parse_orders(response, market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=10, params={}):
        if not symbol:
            raise ExchangeError(self.id + 'fetchOpenOrders requires a symbol parameter')
        self.load_markets()
        market = self.market(symbol)
        request = {'currency': market['id'], 
           'pageIndex': 1, 
           'pageSize': limit}
        method = 'privateGetGetUnfinishedOrdersIgnoreTradeType'
        if 'tradeType' in params:
            method = 'privateGetGetOrdersNew'
        response = None
        try:
            response = getattr(self, method)(self.extend(request, params))
        except Exception as e:
            if isinstance(e, OrderNotFound):
                return []
            raise e

        return self.parse_orders(response, market, since, limit)

    def parse_order(self, order, market=None):
        side = order['type'] == 'buy' if 1 else 'sell'
        type = 'limit'
        timestamp = None
        createDateField = self.get_create_date_field()
        if createDateField in order:
            timestamp = order[createDateField]
        symbol = None
        if 'currency' in order:
            market = self.marketsById[order['currency']]
        if market:
            symbol = market['symbol']
        price = order['price']
        average = order['trade_price']
        filled = order['trade_amount']
        amount = order['total_amount']
        remaining = amount - filled
        cost = order['trade_money']
        status = self.safe_string(order, 'status')
        if status is not None:
            status = self.parse_order_status(status)
        result = {'info': order, 'id': order['id'], 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'lastTradeTimestamp': None, 
           'symbol': symbol, 
           'type': type, 
           'side': side, 
           'price': price, 
           'average': average, 
           'cost': cost, 
           'amount': amount, 
           'filled': filled, 
           'remaining': remaining, 
           'status': status, 
           'fee': None}
        return result

    def parse_order_status(self, status):
        statuses = {'0': 'open', 
           '1': 'canceled', 
           '2': 'closed', 
           '3': 'open'}
        if status in statuses:
            return statuses[status]
        return status

    def get_create_date_field(self):
        return 'trade_date'

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        if api == 'public':
            url += '/' + self.version + '/' + path
            if params:
                url += '?' + self.urlencode(params)
        else:
            query = self.keysort(self.extend({'method': path, 
               'accesskey': self.apiKey}, params))
            nonce = self.nonce()
            query = self.keysort(query)
            auth = self.rawencode(query)
            secret = self.hash(self.encode(self.secret), 'sha1')
            signature = self.hmac(self.encode(auth), self.encode(secret), hashlib.md5)
            suffix = 'sign=' + signature + '&reqTime=' + str(nonce)
            url += '/' + path + '?' + auth + '&' + suffix
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body):
        if not isinstance(body, basestring):
            return
        if len(body) < 2:
            return
        if body[0] == '{':
            response = json.loads(body)
            if 'code' in response:
                code = self.safe_string(response, 'code')
                message = self.id + ' ' + self.json(response)
                if code in self.exceptions:
                    ExceptionClass = self.exceptions[code]
                    raise ExceptionClass(message)
                elif code != '1000':
                    raise ExchangeError(message)