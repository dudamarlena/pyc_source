# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/okcoinusd.py
# Compiled at: 2018-04-27 06:35:35
from anyex.base.exchange import Exchange
import math, json
from anyex.base.errors import ExchangeError
from anyex.base.errors import AuthenticationError
from anyex.base.errors import InsufficientFunds
from anyex.base.errors import InvalidOrder
from anyex.base.errors import OrderNotFound

class okcoinusd(Exchange):

    def describe(self):
        return self.deep_extend(super(okcoinusd, self).describe(), {'id': 'okcoinusd', 
           'name': 'OKCoin USD', 
           'countries': [
                       'CN', 'US'], 
           'version': 'v1', 
           'rateLimit': 1000, 
           'has': {'CORS': False, 
                   'fetchOHLCV': True, 
                   'fetchOrder': True, 
                   'fetchOrders': False, 
                   'fetchOpenOrders': True, 
                   'fetchClosedOrders': True, 
                   'withdraw': True, 
                   'futures': False}, 
           'extension': '.do', 
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
           'api': {'web': {'get': [
                                 'markets/currencies',
                                 'markets/products']}, 
                   'public': {'get': [
                                    'depth',
                                    'exchange_rate',
                                    'future_depth',
                                    'future_estimated_price',
                                    'future_hold_amount',
                                    'future_index',
                                    'future_kline',
                                    'future_price_limit',
                                    'future_ticker',
                                    'future_trades',
                                    'kline',
                                    'otcs',
                                    'ticker',
                                    'tickers',
                                    'trades']}, 
                   'private': {'post': [
                                      'account_records',
                                      'batch_trade',
                                      'borrow_money',
                                      'borrow_order_info',
                                      'borrows_info',
                                      'cancel_borrow',
                                      'cancel_order',
                                      'cancel_otc_order',
                                      'cancel_withdraw',
                                      'future_batch_trade',
                                      'future_cancel',
                                      'future_devolve',
                                      'future_explosive',
                                      'future_order_info',
                                      'future_orders_info',
                                      'future_position',
                                      'future_position_4fix',
                                      'future_trade',
                                      'future_trades_history',
                                      'future_userinfo',
                                      'future_userinfo_4fix',
                                      'lend_depth',
                                      'order_fee',
                                      'order_history',
                                      'order_info',
                                      'orders_info',
                                      'otc_order_history',
                                      'otc_order_info',
                                      'repayment',
                                      'submit_otc_order',
                                      'trade',
                                      'trade_history',
                                      'trade_otc_order',
                                      'withdraw',
                                      'withdraw_info',
                                      'unrepayments_info',
                                      'userinfo']}}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27766791-89ffb502-5ee5-11e7-8a5b-c5950b68ac65.jpg', 
                    'api': {'web': 'https://www.okcoin.com/v2', 
                            'public': 'https://www.okcoin.com/api', 
                            'private': 'https://www.okcoin.com/api'}, 
                    'www': 'https://www.okcoin.com', 
                    'doc': [
                          'https://www.okcoin.com/rest_getStarted.html',
                          'https://www.npmjs.com/package/okcoin.com']}, 
           'fees': {'trading': {'taker': 0.002, 
                                'maker': 0.002}}, 
           'exceptions': {'1009': OrderNotFound, 
                          '1051': OrderNotFound, 
                          '20015': OrderNotFound, 
                          '1013': InvalidOrder, 
                          '1027': InvalidOrder, 
                          '1002': InsufficientFunds, 
                          '1050': InvalidOrder, 
                          '10000': ExchangeError, 
                          '10005': AuthenticationError, 
                          '10008': ExchangeError}, 
           'options': {'warnOnFetchOHLCVLimitArgument': True}})

    def fetch_markets(self):
        response = self.webGetMarketsProducts()
        markets = response['data']
        result = []
        futureMarkets = {'BCH/USD': True, 
           'BTC/USD': True, 
           'ETC/USD': True, 
           'ETH/USD': True, 
           'LTC/USD': True, 
           'XRP/USD': True, 
           'EOS/USD': True, 
           'BTG/USD': True}
        for i in range(0, len(markets)):
            id = markets[i]['symbol']
            baseId, quoteId = id.split('_')
            baseIdUppercase = baseId.upper()
            quoteIdUppercase = quoteId.upper()
            base = self.common_currency_code(baseIdUppercase)
            quote = self.common_currency_code(quoteIdUppercase)
            symbol = base + '/' + quote
            precision = {'amount': markets[i]['maxSizeDigit'], 
               'price': markets[i]['maxPriceDigit']}
            lot = math.pow(10, -precision['amount'])
            minAmount = markets[i]['minTradeSize']
            minPrice = math.pow(10, -precision['price'])
            active = markets[i]['online'] != 0
            market = self.extend(self.fees['trading'], {'id': id, 
               'symbol': symbol, 
               'base': base, 
               'quote': quote, 
               'baseId': baseId, 
               'quoteId': quoteId, 
               'info': markets[i], 
               'type': 'spot', 
               'spot': True, 
               'future': False, 
               'lot': lot, 
               'active': active, 
               'precision': precision, 
               'limits': {'amount': {'min': minAmount, 
                                     'max': None}, 
                          'price': {'min': minPrice, 
                                    'max': None}, 
                          'cost': {'min': minAmount * minPrice, 
                                   'max': None}}})
            result.append(market)
            futureQuote = 'USD' if market['quote'] == 'USDT' else market['quote']
            futureSymbol = market['base'] + '/' + futureQuote
            if self.has['futures'] and futureSymbol in list(futureMarkets.keys()):
                result.append(self.extend(market, {'quote': 'USD', 
                   'symbol': market['base'] + '/USD', 
                   'id': market['id'].replace('usdt', 'usd'), 
                   'quoteId': market['quoteId'].replace('usdt', 'usd'), 
                   'type': 'future', 
                   'spot': False, 
                   'future': True}))

        return result

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        method = 'publicGet'
        request = {'symbol': market['id']}
        if limit is not None:
            request['size'] = limit
        if market['future']:
            method += 'Future'
            if not params.get('contract_type'):
                raise ExchangeError(self.id + ' futureOrderBook requires a contract_type parameter in params')
            request['contract_type'] = params.get('contract_type')
        method += 'Depth'
        orderbook = getattr(self, method)(self.extend(request, params))
        return self.parse_order_book(orderbook)

    def parse_ticker(self, ticker, market=None):
        timestamp = ticker['timestamp']
        symbol = None
        if not market:
            if 'symbol' in ticker:
                marketId = ticker['symbol']
                if marketId in self.markets_by_id:
                    market = self.markets_by_id[marketId]
        if market:
            symbol = market['symbol']
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

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        method = 'publicGet'
        request = {'symbol': market['id']}
        if market['future']:
            method += 'Future'
            if not params.get('contract_type'):
                raise ExchangeError(self.id + ' futureTicker requires a contract_type parameter in params')
            request['contract_type'] = params.get('contract_type')
        method += 'Ticker'
        response = getattr(self, method)(self.extend(request, params))
        ticker = self.safe_value(response, 'ticker')
        if ticker is None:
            raise ExchangeError(self.id + ' fetchTicker returned an empty response: ' + self.json(response))
        timestamp = self.safe_integer(response, 'date')
        if timestamp is not None:
            timestamp *= 1000
            ticker = self.extend(ticker, {'timestamp': timestamp})
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        symbol = None
        if market:
            symbol = market['symbol']
        return {'info': trade, 
           'timestamp': trade['date_ms'], 
           'datetime': self.iso8601(trade['date_ms']), 
           'symbol': symbol, 
           'id': str(trade['tid']), 
           'order': None, 
           'type': None, 
           'side': trade['type'], 
           'price': float(trade['price']), 
           'amount': float(trade['amount'])}

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        method = 'publicGet'
        request = {'symbol': market['id']}
        if market['future']:
            method += 'Future'
            if not params.get('contract_type'):
                raise ExchangeError(self.id + ' futureTrades requires a contract_type parameter in params')
            request['contract_type'] = params.get('contract_type')
        method += 'Trades'
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        method = 'publicGet'
        request = {'symbol': market['id'], 
           'type': self.timeframes[timeframe]}
        if market['future']:
            method += 'Future'
            if not params.get('contract_type'):
                raise ExchangeError(self.id + ' futureOhlcv requires a contract_type parameter in params')
            request['contract_type'] = params.get('contract_type')
        method += 'Kline'
        if limit is not None:
            if self.options['warnOnFetchOHLCVLimitArgument']:
                raise ExchangeError(self.id + ' fetchOHLCV counts "limit" candles from current time backwards, therefore the "limit" argument for ' + self.id + ' is disabled. Set ' + self.id + '.options["warnOnFetchOHLCVLimitArgument"] = False to suppress self warning message.')
            request['size'] = int(limit)
        if since is not None:
            request['since'] = since
        else:
            request['since'] = self.milliseconds() - 86400000
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostUserinfo()
        balances = response['info']['funds']
        result = {'info': response}
        ids = list(self.currencies_by_id.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            code = self.currencies_by_id[id]['code']
            account = self.account()
            account['free'] = self.safe_float(balances['free'], id, 0.0)
            account['used'] = self.safe_float(balances['freezed'], id, 0.0)
            account['total'] = self.sum(account['free'], account['used'])
            result[code] = account

        return self.parse_balance(result)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        method = 'privatePost'
        order = {'symbol': market['id'], 
           'type': side}
        if market['future']:
            method += 'Future'
            contract_type = params.get('contract_type')
            if not contract_type:
                raise ExchangeError(self.id + ' future orders requires a contract_type parameter in params')
            position_type = params.get('type')
            if not position_type:
                raise ExchangeError(self.id + ' future orders requires a position_type parameter in params')
            match_price = params.get('match_price', 0)
            if match_price == 0 and price is None:
                raise ExchangeError(self.id + ' future limit orders requires amount parameter')
            leverage_rate = params.get('leverage_rate')
            if leverage_rate:
                order = self.extend(order, {'lever_rate': leverage_rate})
            order = self.extend(order, {'contract_type': contract_type, 
               'match_price': match_price, 
               'price': price, 
               'amount': amount, 
               'type': position_type})
        elif type == 'limit':
            order['price'] = price
            order['amount'] = amount
        else:
            order['type'] += '_market'
            if side == 'buy':
                order['price'] = self.safe_float(params, 'cost')
                if not order['price']:
                    raise ExchangeError(self.id + ' market buy orders require an additional cost parameter, cost = price * amount')
            else:
                order['amount'] = amount
        params = self.omit(params, 'cost')
        method += 'Trade'
        response = getattr(self, method)(self.extend(order, params))
        timestamp = self.milliseconds()
        return {'info': response, 
           'id': str(response['order_id']), 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'lastTradeTimestamp': None, 
           'status': None, 
           'symbol': symbol, 
           'type': type, 
           'side': side, 
           'price': price, 
           'amount': amount, 
           'filled': None, 
           'remaining': None, 
           'cost': None, 
           'trades': None, 
           'fee': None}

    def cancel_order(self, id, symbol=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' cancelOrder() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {'symbol': market['id'], 
           'order_id': id}
        method = 'privatePost'
        if market['future']:
            method += 'FutureCancel'
            if not params.get('contract_type'):
                raise ExchangeError(self.id + ' futureCancelOrder requires a contract_type parameter in params')
            request['contract_type'] = params.get('contract_type')
        else:
            method += 'CancelOrder'
        response = getattr(self, method)(self.extend(request, params))
        return response

    def parse_order_status(self, status):
        if status == -1:
            return 'canceled'
        if status == 0:
            return 'open'
        if status == 1:
            return 'open'
        if status == 2:
            return 'closed'
        if status == 4:
            return 'canceled'
        return status

    def parse_order_side(self, side):
        if side == 1:
            return 'buy'
        if side == 2:
            return 'sell'
        if side == 3:
            return 'sell'
        if side == 4:
            return 'buy'
        return side

    def parse_order(self, order, market=None):
        side = None
        type = None
        if 'type' in order:
            if order['type'] == 'buy' or order['type'] == 'sell':
                side = order['type']
                type = 'limit'
            elif order['type'] == 'buy_market':
                side = 'buy'
                type = 'market'
            elif order['type'] == 'sell_market':
                side = 'sell'
                type = 'market'
            else:
                side = self.parse_order_side(order['type'])
                if 'contract_name' in list(order.keys()) or 'lever_rate' in list(order.keys()):
                    type = 'margin'
        status = self.parse_order_status(order['status'])
        symbol = None
        if not market:
            if 'symbol' in order:
                if order['symbol'] in self.markets_by_id:
                    market = self.markets_by_id[order['symbol']]
        if market:
            symbol = market['symbol']
        timestamp = None
        createDateField = self.get_create_date_field()
        if createDateField in order:
            timestamp = order[createDateField]
        amount = order['amount']
        filled = order['deal_amount']
        remaining = amount - filled
        average = self.safe_float(order, 'avg_price')
        average = self.safe_float(order, 'price_avg', average)
        cost = average * filled
        result = {'info': order, 
           'id': str(order['order_id']), 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'lastTradeTimestamp': None, 
           'symbol': symbol, 
           'type': type, 
           'side': side, 
           'price': order['price'], 
           'average': average, 
           'cost': cost, 
           'amount': amount, 
           'filled': filled, 
           'remaining': remaining, 
           'status': status, 
           'fee': None}
        return result

    def get_create_date_field(self):
        return 'create_date'

    def get_orders_field(self):
        return 'orders'

    def fetch_order(self, id, symbol=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchOrder requires a symbol parameter')
        self.load_markets()
        market = self.market(symbol)
        method = 'privatePost'
        request = {'order_id': id, 
           'symbol': market['id']}
        if market['future']:
            method += 'Future'
            if not params.get('contract_type'):
                raise ExchangeError(self.id + ' futureOrderInfo requires a contract_type parameter in params')
            request['contract_type'] = params.get('contract_type')
        method += 'OrderInfo'
        response = getattr(self, method)(self.extend(request, params))
        ordersField = self.get_orders_field()
        numOrders = len(response[ordersField])
        if numOrders > 0:
            return self.parse_order(response[ordersField][0])
        raise OrderNotFound(self.id + ' order ' + id + ' not found')

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchOrders requires a symbol parameter')
        self.load_markets()
        market = self.market(symbol)
        method = 'privatePost'
        request = {'symbol': market['id']}
        order_id_in_params = 'order_id' in list(params.keys())
        if market['future']:
            method += 'FutureOrdersInfo'
            if not params.get('contract_type'):
                raise ExchangeError(self.id + ' futureOrdersInfo requires a contract_type parameter in params')
            request['contract_type'] = params.get('contract_type')
            if not order_id_in_params:
                raise ExchangeError(self.id + ' fetchOrders() requires order_id param for futures market ' + symbol + '(a string of one or more order ids, comma-separated)')
        else:
            status = None
            if 'type' in params:
                status = params['type']
            elif 'status' in params:
                status = params['status']
            else:
                name = 'type' if order_id_in_params else 'status'
                raise ExchangeError(self.id + ' fetchOrders() requires ' + name + ' param for spot market ' + symbol + '(0 - for unfilled orders, 1 - for filled/canceled orders)')
            if order_id_in_params:
                method += 'OrdersInfo'
                request = self.extend(request, {'type': status, 
                   'order_id': params['order_id']})
            else:
                method += 'OrderHistory'
                request = self.extend(request, {'status': status, 
                   'current_page': 1, 
                   'page_length': 200})
            params = self.omit(params, ['type', 'status'])
        response = getattr(self, method)(self.extend(request, params))
        ordersField = self.get_orders_field()
        return self.parse_orders(response[ordersField], market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        open = 0
        return self.fetch_orders(symbol, since, limit, self.extend({'status': open}, params))

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        closed = 1
        orders = self.fetch_orders(symbol, since, limit, self.extend({'status': closed}, params))
        return orders

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        currencyId = currency['id'] + '_usd'
        request = {'symbol': currencyId, 
           'withdraw_address': address, 
           'withdraw_amount': amount, 
           'target': 'address'}
        query = params
        if 'chargefee' in query:
            request['chargefee'] = query['chargefee']
            query = self.omit(query, 'chargefee')
        else:
            raise ExchangeError(self.id + ' withdraw() requires a `chargefee` parameter')
        if self.password:
            request['trade_pwd'] = self.password
        elif 'password' in query:
            request['trade_pwd'] = query['password']
            query = self.omit(query, 'password')
        elif 'trade_pwd' in query:
            request['trade_pwd'] = query['trade_pwd']
            query = self.omit(query, 'trade_pwd')
        passwordInRequest = 'trade_pwd' in list(request.keys())
        if not passwordInRequest:
            raise ExchangeError(self.id + ' withdraw() requires self.password set on the exchange instance or a password / trade_pwd parameter')
        response = self.privatePostWithdraw(self.extend(request, query))
        return {'info': response, 
           'id': self.safe_string(response, 'withdraw_id')}

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = '/'
        if api != 'web':
            url += self.version + '/'
        url += path + self.extension
        if api == 'private':
            self.check_required_credentials()
            query = self.keysort(self.extend({'api_key': self.apiKey}, params))
            queryString = self.rawencode(query) + '&secret_key=' + self.secret
            query['sign'] = self.hash(self.encode(queryString)).upper()
            body = self.urlencode(query)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        elif params:
            url += '?' + self.urlencode(params)
        url = self.urls['api'][api] + url
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body):
        if len(body) < 2:
            return
        if body[0] == '{':
            response = json.loads(body)
            if 'error_code' in response:
                error = self.safe_string(response, 'error_code')
                message = self.id + ' ' + self.json(response)
                if error in self.exceptions:
                    ExceptionClass = self.exceptions[error]
                    raise ExceptionClass(message)
                else:
                    raise ExchangeError(message)
            if 'result' in response:
                if not response['result']:
                    raise ExchangeError(self.id + ' ' + self.json(response))

    def parse_position(self, position, market=None):
        symbol = None
        if len(position['holding']) == 0:
            return {}
        else:
            holding = position['holding'][0]
            if market:
                symbol = market['symbol']
            else:
                id = holding['symbol']
                if symbol in self.markets_by_id[id]:
                    market = self.markets_by_id[id]
                    symbol = market['symbol']
            datetime_value = None
            timestamp = None
            iso8601 = None
            if 'timestamp' in holding:
                datetime_value = holding['create_date']
            if datetime_value is not None:
                timestamp = self.parse8601(datetime_value)
                iso8601 = self.iso8601(timestamp)
            liquidation_price = self.safe_float(position, 'force_liqu_price')
            margin_call_price = liquidation_price
            leverage = self.safe_float(holding, 'lever_rate')
            open_buy_amount = holding['buy_amount']
            open_buy_cost = holding['buy_price_cost']
            open_sell_amount = holding['sell_amount']
            open_sell_cost = holding['sell_price_cost']
            result = {'info': position, 
               'timestamp': timestamp, 
               'datetime': iso8601, 
               'symbol': symbol, 
               'liquidation_price': liquidation_price, 
               'margin_call_price': margin_call_price, 
               'leverage': leverage, 
               'open_buy_amount': open_buy_amount, 
               'open_buy_cost': open_buy_cost, 
               'open_sell_amount': open_sell_amount, 
               'open_sell_cost': open_sell_cost}
            return result

    def create_position(self, symbol, type, side, amount, price=None, params={}):
        if params.get('contract_type') is None:
            raise ExchangeError(self.id + ' futurePosition requires a contract_type parameter in params')
        if type == 'market':
            params['match_price'] = 1
        else:
            params['match_price'] = 0
        if side == 'sell':
            params['type'] = 2
        else:
            params['type'] = 1
        return self.create_order(symbol, type, side, amount, price, params)

    def close_position(self, symbol, type=None, side=None, amount=None, price=None, params={}):
        if type == 'market':
            params['match_price'] = 1
        else:
            params['match_price'] = 0
        if side == 'sell':
            params['type'] = 3
        else:
            params['type'] = 4
        return self.create_order(symbol, type, side, amount, price, params)

    def fetch_future_position(self, symbol=None, params={}):
        if not params.get('contract_type'):
            raise ExchangeError(self.id + ' futurePosition requires a contract_type parameter in params')
        method = 'privatePostFuturePosition4fix'
        self.load_markets()
        request = {}
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_position(response)