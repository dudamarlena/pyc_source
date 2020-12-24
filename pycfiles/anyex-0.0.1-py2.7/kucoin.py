# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/kucoin.py
# Compiled at: 2018-04-27 06:35:43
from anyex.base.exchange import Exchange
import base64, hashlib, math, json
from anyex.base.errors import ExchangeError
from anyex.base.errors import AuthenticationError
from anyex.base.errors import InsufficientFunds
from anyex.base.errors import InvalidOrder
from anyex.base.errors import OrderNotFound
from anyex.base.errors import InvalidNonce

class kucoin(Exchange):

    def describe(self):
        return self.deep_extend(super(kucoin, self).describe(), {'id': 'kucoin', 
           'name': 'Kucoin', 
           'countries': 'HK', 
           'version': 'v1', 
           'rateLimit': 2000, 
           'userAgent': self.userAgents['chrome'], 
           'has': {'CORS': False, 
                   'cancelOrders': True, 
                   'createMarketOrder': False, 
                   'fetchDepositAddress': True, 
                   'fetchTickers': True, 
                   'fetchOHLCV': True, 
                   'fetchOrder': True, 
                   'fetchOrders': False, 
                   'fetchClosedOrders': True, 
                   'fetchOpenOrders': True, 
                   'fetchMyTrades': 'emulated', 
                   'fetchCurrencies': True, 
                   'withdraw': True}, 
           'timeframes': {'1m': 1, 
                          '5m': 5, 
                          '15m': 15, 
                          '30m': 30, 
                          '1h': 60, 
                          '8h': 480, 
                          '1d': 'D', 
                          '1w': 'W'}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/33795655-b3c46e48-dcf6-11e7-8abe-dc4588ba7901.jpg', 
                    'api': {'public': 'https://api.kucoin.com', 
                            'private': 'https://api.kucoin.com', 
                            'kitchen': 'https://kitchen.kucoin.com', 
                            'kitchen-2': 'https://kitchen-2.kucoin.com'}, 
                    'www': 'https://kucoin.com', 
                    'doc': 'https://kucoinapidocs.docs.apiary.io', 
                    'fees': 'https://news.kucoin.com/en/fee'}, 
           'api': {'kitchen': {'get': [
                                     'open/chart/history']}, 
                   'public': {'get': [
                                    'open/chart/config',
                                    'open/chart/history',
                                    'open/chart/symbol',
                                    'open/currencies',
                                    'open/deal-orders',
                                    'open/kline',
                                    'open/lang-list',
                                    'open/orders',
                                    'open/orders-buy',
                                    'open/orders-sell',
                                    'open/tick',
                                    'market/open/coin-info',
                                    'market/open/coins',
                                    'market/open/coins-trending',
                                    'market/open/symbols']}, 
                   'private': {'get': [
                                     'account/balance',
                                     'account/{coin}/wallet/address',
                                     'account/{coin}/wallet/records',
                                     'account/{coin}/balance',
                                     'account/promotion/info',
                                     'account/promotion/sum',
                                     'deal-orders',
                                     'order/active',
                                     'order/active-map',
                                     'order/dealt',
                                     'order/detail',
                                     'referrer/descendant/count',
                                     'user/info'], 
                               'post': [
                                      'account/{coin}/withdraw/apply',
                                      'account/{coin}/withdraw/cancel',
                                      'account/promotion/draw',
                                      'cancel-order',
                                      'order',
                                      'order/cancel-all',
                                      'user/change-lang']}}, 
           'fees': {'trading': {'maker': 0.001, 
                                'taker': 0.001}, 
                    'funding': {'tierBased': False, 
                                'percentage': False, 
                                'withdraw': {'KCS': 2.0, 
                                             'BTC': 0.0005, 
                                             'USDT': 10.0, 
                                             'ETH': 0.01, 
                                             'LTC': 0.001, 
                                             'NEO': 0.0, 
                                             'GAS': 0.0, 
                                             'KNC': 0.5, 
                                             'BTM': 5.0, 
                                             'QTUM': 0.1, 
                                             'EOS': 0.5, 
                                             'CVC': 3.0, 
                                             'OMG': 0.1, 
                                             'PAY': 0.5, 
                                             'SNT': 20.0, 
                                             'BHC': 1.0, 
                                             'HSR': 0.01, 
                                             'WTC': 0.1, 
                                             'VEN': 2.0, 
                                             'MTH': 10.0, 
                                             'RPX': 1.0, 
                                             'REQ': 20.0, 
                                             'EVX': 0.5, 
                                             'MOD': 0.5, 
                                             'NEBL': 0.1, 
                                             'DGB': 0.5, 
                                             'CAG': 2.0, 
                                             'CFD': 0.5, 
                                             'RDN': 0.5, 
                                             'UKG': 5.0, 
                                             'BCPT': 5.0, 
                                             'PPT': 0.1, 
                                             'BCH': 0.0005, 
                                             'STX': 2.0, 
                                             'NULS': 1.0, 
                                             'GVT': 0.1, 
                                             'HST': 2.0, 
                                             'PURA': 0.5, 
                                             'SUB': 2.0, 
                                             'QSP': 5.0, 
                                             'POWR': 1.0, 
                                             'FLIXX': 10.0, 
                                             'LEND': 20.0, 
                                             'AMB': 3.0, 
                                             'RHOC': 2.0, 
                                             'R': 2.0, 
                                             'DENT': 50.0, 
                                             'DRGN': 1.0, 
                                             'ACT': 0.1}, 
                                'deposit': {}}}, 
           'options': {'timeDifference': 0, 
                       'adjustForTimeDifference': False}})

    def nonce(self):
        return self.milliseconds() - self.options['timeDifference']

    def load_time_difference(self):
        response = self.publicGetOpenTick()
        after = self.milliseconds()
        self.options['timeDifference'] = int(after - response['timestamp'])
        return self.options['timeDifference']

    def fetch_markets(self):
        response = self.publicGetMarketOpenSymbols()
        if self.options['adjustForTimeDifference']:
            self.load_time_difference()
        markets = response['data']
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = market['symbol']
            base = market['coinType']
            quote = market['coinTypePair']
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
            precision = {'amount': 8, 
               'price': 8}
            active = market['trading']
            result.append({'id': id, 
               'symbol': symbol, 
               'base': base, 
               'quote': quote, 
               'active': active, 
               'taker': self.safe_float(market, 'feeRate'), 
               'maker': self.safe_float(market, 'feeRate'), 
               'info': market, 
               'lot': math.pow(10, -precision['amount']), 
               'precision': precision, 
               'limits': {'amount': {'min': math.pow(10, -precision['amount']), 
                                     'max': None}, 
                          'price': {'min': None, 
                                    'max': None}}})

        return result

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        response = self.privateGetAccountCoinWalletAddress(self.extend({'coin': currency['id']}, params))
        data = response['data']
        address = self.safe_string(data, 'address')
        self.check_address(address)
        tag = self.safe_string(data, 'userOid')
        return {'currency': code, 
           'address': address, 
           'tag': tag, 
           'status': 'ok', 
           'info': response}

    def fetch_currencies(self, params={}):
        response = self.publicGetMarketOpenCoins(params)
        currencies = response['data']
        result = {}
        for i in range(0, len(currencies)):
            currency = currencies[i]
            id = currency['coin']
            code = self.common_currency_code(id)
            precision = currency['tradePrecision']
            deposit = currency['enableDeposit']
            withdraw = currency['enableWithdraw']
            active = deposit and withdraw
            result[code] = {'id': id, 
               'code': code, 
               'info': currency, 
               'name': currency['name'], 
               'active': active, 
               'status': 'ok', 
               'fee': currency['withdrawMinFee'], 
               'precision': precision, 
               'limits': {'amount': {'min': math.pow(10, -precision), 
                                     'max': math.pow(10, precision)}, 
                          'price': {'min': math.pow(10, -precision), 
                                    'max': math.pow(10, precision)}, 
                          'cost': {'min': None, 
                                   'max': None}, 
                          'withdraw': {'min': currency['withdrawMinAmount'], 
                                       'max': math.pow(10, precision)}}}

        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetAccountBalance(self.extend({'limit': 20, 
           'page': 1}, params))
        balances = response['data']
        result = {'info': balances}
        indexed = self.index_by(balances, 'coinType')
        keys = list(indexed.keys())
        for i in range(0, len(keys)):
            id = keys[i]
            currency = self.common_currency_code(id)
            account = self.account()
            balance = indexed[id]
            used = float(balance['freezeBalance'])
            free = float(balance['balance'])
            total = self.sum(free, used)
            account['free'] = free
            account['used'] = used
            account['total'] = total
            result[currency] = account

        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetOpenOrders(self.extend({'symbol': market['id']}, params))
        orderbook = response['data']
        return self.parse_order_book(orderbook, None, 'BUY', 'SELL')

    def parse_order(self, order, market=None):
        side = self.safe_value(order, 'direction')
        if side is None:
            side = order['type']
        if side is not None:
            side = side.lower()
        orderId = self.safe_string(order, 'orderOid')
        if orderId is None:
            orderId = self.safe_string(order, 'oid')
        trades = None
        if 'dealOrders' in order:
            trades = self.safe_value(order['dealOrders'], 'datas')
        if trades is not None:
            trades = self.parse_trades(trades, market)
            for i in range(0, len(trades)):
                trades[i]['side'] = side
                trades[i]['order'] = orderId

        symbol = None
        if market is not None:
            symbol = market['symbol']
        else:
            symbol = order['coinType'] + '/' + order['coinTypePair']
        timestamp = self.safe_value(order, 'createdAt')
        remaining = self.safe_float(order, 'pendingAmount')
        status = self.safe_value(order, 'status')
        filled = self.safe_float(order, 'dealAmount')
        amount = self.safe_float(order, 'amount')
        cost = self.safe_float(order, 'dealValue')
        if cost is None:
            cost = self.safe_float(order, 'dealValueTotal')
        if status is None:
            if remaining is not None:
                if remaining > 0:
                    status = 'open'
                else:
                    status = 'closed'
        if filled is None:
            if status is not None:
                if status == 'closed':
                    filled = self.safe_float(order, 'amount')
        elif filled == 0.0:
            if trades is not None:
                cost = 0
                for i in range(0, len(trades)):
                    filled += trades[i]['amount']
                    cost += trades[i]['cost']

        price = None
        if filled is not None:
            if filled > 0.0:
                price = self.safe_float(order, 'price')
                if price is None:
                    price = self.safe_float(order, 'dealPrice')
                if price is None:
                    price = self.safe_float(order, 'dealPriceAverage')
            else:
                price = self.safe_float(order, 'orderPrice')
                if price is None:
                    price = self.safe_float(order, 'price')
            if price is not None:
                if cost is None:
                    cost = price * filled
            if amount is None:
                if remaining is not None:
                    amount = self.sum(filled, remaining)
            elif remaining is None:
                remaining = amount - filled
        if status == 'open':
            if cost is None or cost == 0.0:
                if price is not None:
                    if amount is not None:
                        cost = amount * price
        feeCurrency = None
        if market is not None:
            feeCurrency = market['quote'] if side == 'sell' else market['base']
        else:
            feeCurrencyField = 'coinTypePair' if side == 'sell' else 'coinType'
            feeCurrency = self.safe_string(order, feeCurrencyField)
            if feeCurrency is not None:
                if feeCurrency in self.currencies_by_id:
                    feeCurrency = self.currencies_by_id[feeCurrency]['code']
        feeCost = self.safe_float(order, 'fee')
        fee = {'cost': self.safe_float(order, 'feeTotal', feeCost), 
           'rate': self.safe_float(order, 'feeRate'), 
           'currency': feeCurrency}
        result = {'info': order, 
           'id': orderId, 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'lastTradeTimestamp': None, 
           'symbol': symbol, 
           'type': 'limit', 
           'side': side, 
           'price': price, 
           'amount': amount, 
           'cost': cost, 
           'filled': filled, 
           'remaining': remaining, 
           'status': status, 
           'fee': fee, 
           'trades': trades}
        return result

    def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrder requires a symbol argument')
        orderType = self.safe_value(params, 'type')
        if orderType is None:
            raise ExchangeError(self.id + ' fetchOrder requires a type parameter("BUY" or "SELL")')
        self.load_markets()
        market = self.market(symbol)
        request = {'symbol': market['id'], 
           'type': orderType, 
           'orderOid': id}
        response = self.privateGetOrderDetail(self.extend(request, params))
        if not response['data']:
            raise OrderNotFound(self.id + ' ' + self.json(response))
        return self.parse_order(response['data'], market)

    def parse_orders_by_status(self, orders, market, since, limit, status):
        result = []
        for i in range(0, len(orders)):
            order = self.parse_order(self.extend(orders[i], {'status': status}), market)
            result.append(order)

        symbol = market['symbol'] if market is not None else None
        return self.filter_by_symbol_since_limit(result, symbol, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchOpenOrders requires a symbol')
        self.load_markets()
        market = self.market(symbol)
        request = {'symbol': market['id']}
        response = self.privateGetOrderActiveMap(self.extend(request, params))
        sell = self.safe_value(response['data'], 'SELL')
        if sell is None:
            sell = []
        buy = self.safe_value(response['data'], 'BUY')
        if buy is None:
            buy = []
        orders = self.array_concat(sell, buy)
        return self.parse_orders_by_status(orders, market, since, limit, 'open')

    def fetch_closed_orders(self, symbol=None, since=None, limit=20, params={}):
        request = {}
        self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        if since is not None:
            request['since'] = since
        if limit is not None:
            request['limit'] = limit
        response = self.privateGetOrderDealt(self.extend(request, params))
        orders = response['data']['datas']
        return self.parse_orders_by_status(orders, market, since, limit, 'closed')

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type != 'limit':
            raise ExchangeError(self.id + ' allows limit orders only')
        self.load_markets()
        market = self.market(symbol)
        quote = market['quote']
        base = market['base']
        request = {'symbol': market['id'], 
           'type': side.upper(), 
           'price': self.truncate(price, self.currencies[quote]['precision']), 
           'amount': self.truncate(amount, self.currencies[base]['precision'])}
        price = float(price)
        amount = float(amount)
        cost = price * amount
        response = self.privatePostOrder(self.extend(request, params))
        orderId = self.safe_string(response['data'], 'orderOid')
        timestamp = self.safe_integer(response, 'timestamp')
        iso8601 = None
        if timestamp is not None:
            iso8601 = self.iso8601(timestamp)
        order = {'info': response, 'id': orderId, 
           'timestamp': timestamp, 
           'datetime': iso8601, 
           'lastTradeTimestamp': None, 
           'symbol': market['symbol'], 
           'type': type, 
           'side': side, 
           'amount': amount, 
           'filled': None, 
           'remaining': None, 
           'price': price, 
           'cost': cost, 
           'status': 'open', 
           'fee': None, 
           'trades': None}
        self.orders[orderId] = order
        return order

    def cancel_orders(self, symbol=None, params={}):
        request = {}
        if symbol:
            self.load_markets()
            market = self.market(symbol)
            request['symbol'] = market['id']
        if 'type' in params:
            request['type'] = params['type'].upper()
            params = self.omit(params, 'type')
        return self.privatePostOrderCancelAll(self.extend(request, params))

    def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' cancelOrder requires a symbol')
        self.load_markets()
        market = self.market(symbol)
        request = {'symbol': market['id'], 
           'orderOid': id}
        if 'type' in params:
            request['type'] = params['type'].upper()
            params = self.omit(params, 'type')
        else:
            raise ExchangeError(self.id + ' cancelOrder requires parameter type=["BUY"|"SELL"]')
        return self.privatePostCancelOrder(self.extend(request, params))

    def parse_ticker(self, ticker, market=None):
        timestamp = ticker['datetime']
        symbol = None
        if market:
            symbol = market['symbol']
        else:
            symbol = ticker['coinType'] + '/' + ticker['coinTypePair']
        change = self.safe_float(ticker, 'change')
        last = self.safe_float(ticker, 'lastDealPrice')
        open = None
        if last is not None:
            if change is not None:
                open = last - change
        changePercentage = self.safe_float(ticker, 'changeRate')
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
           'open': open, 
           'close': last, 
           'last': last, 
           'previousClose': None, 
           'change': change, 
           'percentage': changePercentage, 
           'average': None, 
           'baseVolume': self.safe_float(ticker, 'vol'), 
           'quoteVolume': self.safe_float(ticker, 'volValue'), 
           'info': ticker}

    def fetch_tickers(self, symbols=None, params={}):
        response = self.publicGetMarketOpenSymbols(params)
        tickers = response['data']
        result = {}
        for t in range(0, len(tickers)):
            ticker = self.parse_ticker(tickers[t])
            symbol = ticker['symbol']
            result[symbol] = ticker

        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetOpenTick(self.extend({'symbol': market['id']}, params))
        ticker = response['data']
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        id = None
        order = None
        info = trade
        timestamp = None
        type = None
        side = None
        price = None
        cost = None
        amount = None
        fee = None
        if isinstance(trade, list):
            timestamp = trade[0]
            type = 'limit'
            if trade[1] == 'BUY':
                side = 'buy'
            elif trade[1] == 'SELL':
                side = 'sell'
            price = trade[2]
            amount = trade[3]
        else:
            timestamp = self.safe_value(trade, 'createdAt')
            order = self.safe_string(trade, 'orderOid')
            id = self.safe_string(trade, 'oid')
            side = self.safe_string(trade, 'direction')
            if side is not None:
                side = side.lower()
            price = self.safe_float(trade, 'dealPrice')
            amount = self.safe_float(trade, 'amount')
            cost = self.safe_float(trade, 'dealValue')
            feeCurrency = None
            if market is not None:
                feeCurrency = market['quote'] if side == 'sell' else market['base']
            else:
                feeCurrencyField = 'coinTypePair' if side == 'sell' else 'coinType'
                feeCurrency = self.safe_string(order, feeCurrencyField)
                if feeCurrency is not None:
                    if feeCurrency in self.currencies_by_id:
                        feeCurrency = self.currencies_by_id[feeCurrency]['code']
            fee = {'cost': self.safe_float(trade, 'fee'), 
               'currency': feeCurrency}
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {'id': id, 'order': order, 
           'info': info, 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'symbol': symbol, 
           'type': type, 
           'side': side, 
           'price': price, 
           'cost': cost, 
           'amount': amount, 
           'fee': fee}

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetOpenDealOrders(self.extend({'symbol': market['id']}, params))
        return self.parse_trades(response['data'], market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchMyTrades is deprecated and requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {'symbol': market['id']}
        if limit:
            request['limit'] = limit
        response = self.privateGetDealOrders(self.extend(request, params))
        return self.parse_trades(response['data']['datas'], market, since, limit)

    def parse_trading_view_ohlcv(self, ohlcvs, market=None, timeframe='1m', since=None, limit=None):
        result = self.convert_trading_view_to_ohlcv(ohlcvs)
        return self.parse_ohlcvs(result, market, timeframe, since, limit)

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        end = self.seconds()
        resolution = self.timeframes[timeframe]
        minutes = resolution
        if minutes == 'D':
            if limit is None:
                limit = 30
            minutes = 1440
        elif minutes == 'W':
            if limit is None:
                limit = 52
            minutes = 10080
        elif limit is None:
            limit = 1440
        start = end - limit * minutes * 60
        if since is not None:
            start = int(since / 1000)
            end = min(end, self.sum(start, limit * minutes * 60))
        request = {'symbol': market['id'], 'resolution': resolution, 
           'from': start, 
           'to': end}
        response = self.publicGetOpenChartHistory(self.extend(request, params))
        return self.parse_trading_view_ohlcv(response, market, timeframe, since, limit)

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        self.check_address(address)
        response = self.privatePostAccountCoinWithdrawApply(self.extend({'coin': currency['id'], 
           'amount': amount, 
           'address': address}, params))
        return {'info': response, 
           'id': None}

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        endpoint = '/' + self.version + '/' + self.implode_params(path, params)
        url = self.urls['api'][api] + endpoint
        query = self.omit(params, self.extract_params(path))
        if api == 'private':
            self.check_required_credentials()
            nonce = self.nonce()
            queryString = ''
            nonce = str(nonce)
            if query:
                queryString = self.rawencode(self.keysort(query))
                url += '?' + queryString
                if method != 'GET':
                    body = queryString
            auth = endpoint + '/' + nonce + '/' + queryString
            payload = base64.b64encode(self.encode(auth))
            signature = self.hmac(payload, self.encode(self.secret), hashlib.sha256)
            headers = {'KC-API-KEY': self.apiKey, 
               'KC-API-NONCE': nonce, 
               'KC-API-SIGNATURE': signature}
        elif query:
            url += '?' + self.urlencode(query)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def throw_exception_on_error(self, response):
        if 'success' not in list(response.keys()):
            return
        if response['success'] is True:
            return
        if 'code' not in list(response.keys()) or 'msg' not in list(response.keys()):
            raise ExchangeError(self.id + ': malformed response: ' + self.json(response))
        code = self.safe_string(response, 'code')
        message = self.safe_string(response, 'msg')
        feedback = self.id + ' ' + self.json(response)
        if code == 'UNAUTH':
            if message == 'Invalid nonce':
                raise InvalidNonce(feedback)
            raise AuthenticationError(feedback)
        elif code == 'ERROR':
            if message.find('The precision of amount') >= 0:
                raise InvalidOrder(feedback)
            if message.find('Min amount each order') >= 0:
                raise InvalidOrder(feedback)
            if message.find('Min price:') >= 0:
                raise InvalidOrder(feedback)
            if message.find('The precision of price') >= 0:
                raise InvalidOrder(feedback)
        elif code == 'NO_BALANCE':
            if message.find('Insufficient balance') >= 0:
                raise InsufficientFunds(feedback)
        raise ExchangeError(self.id + ': unknown response: ' + self.json(response))

    def handle_errors(self, code, reason, url, method, headers, body, response=None):
        if response is not None:
            self.throw_exception_on_error(response)
        elif body and body[0] == '{':
            self.throw_exception_on_error(json.loads(body))
        return