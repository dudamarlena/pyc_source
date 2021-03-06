# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/bxinth.py
# Compiled at: 2018-04-27 06:36:07
from anyex.base.exchange import Exchange
from anyex.base.errors import ExchangeError

class bxinth(Exchange):

    def describe(self):
        return self.deep_extend(super(bxinth, self).describe(), {'id': 'bxinth', 
           'name': 'BX.in.th', 
           'countries': 'TH', 
           'rateLimit': 1500, 
           'has': {'CORS': False, 
                   'fetchTickers': True, 
                   'fetchOpenOrders': True}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27766412-567b1eb4-5ed7-11e7-94a8-ff6a3884f6c5.jpg', 
                    'api': 'https://bx.in.th/api', 
                    'www': 'https://bx.in.th', 
                    'doc': 'https://bx.in.th/info/api'}, 
           'api': {'public': {'get': [
                                    '',
                                    'options',
                                    'optionbook',
                                    'orderbook',
                                    'pairing',
                                    'trade',
                                    'tradehistory']}, 
                   'private': {'post': [
                                      'balance',
                                      'biller',
                                      'billgroup',
                                      'billpay',
                                      'cancel',
                                      'deposit',
                                      'getorders',
                                      'history',
                                      'option-issue',
                                      'option-bid',
                                      'option-sell',
                                      'option-myissue',
                                      'option-mybid',
                                      'option-myoptions',
                                      'option-exercise',
                                      'option-cancel',
                                      'option-history',
                                      'order',
                                      'withdrawal',
                                      'withdrawal-history']}}, 
           'fees': {'trading': {'taker': 0.25 / 100, 
                                'maker': 0.25 / 100}}, 
           'commonCurrencies': {'DAS': 'DASH', 
                                'DOG': 'DOGE'}})

    def fetch_markets(self):
        markets = self.publicGetPairing()
        keys = list(markets.keys())
        result = []
        for p in range(0, len(keys)):
            market = markets[keys[p]]
            id = str(market['pairing_id'])
            base = market['secondary_currency']
            quote = market['primary_currency']
            base = self.common_currency_code(base)
            quote = self.common_currency_code(quote)
            symbol = base + '/' + quote
            result.append({'id': id, 
               'symbol': symbol, 
               'base': base, 
               'quote': quote, 
               'info': market})

        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostBalance()
        balance = response['balance']
        result = {'info': balance}
        currencies = list(balance.keys())
        for c in range(0, len(currencies)):
            currency = currencies[c]
            code = self.common_currency_code(currency)
            account = {'free': float(balance[currency]['available']), 
               'used': 0.0, 
               'total': float(balance[currency]['total'])}
            account['used'] = account['total'] - account['free']
            result[code] = account

        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        orderbook = self.publicGetOrderbook(self.extend({'pairing': self.market_id(symbol)}, params))
        return self.parse_order_book(orderbook)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market:
            symbol = market['symbol']
        last = float(ticker['last_price'])
        return {'symbol': symbol, 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'high': None, 
           'low': None, 
           'bid': float(ticker['orderbook']['bids']['highbid']), 
           'bidVolume': None, 
           'ask': float(ticker['orderbook']['asks']['highbid']), 
           'askVolume': None, 
           'vwap': None, 
           'open': None, 
           'close': last, 
           'last': last, 
           'previousClose': None, 
           'change': float(ticker['change']), 
           'percentage': None, 
           'average': None, 
           'baseVolume': float(ticker['volume_24hours']), 
           'quoteVolume': None, 
           'info': ticker}

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        tickers = self.publicGet(params)
        result = {}
        ids = list(tickers.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            ticker = tickers[id]
            market = self.markets_by_id[id]
            symbol = market['symbol']
            result[symbol] = self.parse_ticker(ticker, market)

        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        tickers = self.publicGet(self.extend({'pairing': market['id']}, params))
        id = str(market['id'])
        ticker = tickers[id]
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market):
        timestamp = self.parse8601(trade['trade_date'])
        return {'id': trade['trade_id'], 
           'info': trade, 
           'order': trade['order_id'], 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'symbol': market['symbol'], 
           'type': None, 
           'side': trade['trade_type'], 
           'price': float(trade['rate']), 
           'amount': float(trade['amount'])}

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetTrade(self.extend({'pairing': market['id']}, params))
        return self.parse_trades(response['trades'], market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        response = self.privatePostOrder(self.extend({'pairing': self.market_id(symbol), 
           'type': side, 
           'amount': amount, 
           'rate': price}, params))
        return {'info': response, 
           'id': str(response['order_id'])}

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        pairing = None
        return self.privatePostCancel({'order_id': id, 
           'pairing': pairing})

    def parse_order(self, order, market=None):
        side = self.safe_string(order, 'order_type')
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'pairing_id')
            if marketId is not None:
                if marketId in self.markets_by_id:
                    market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        timestamp = self.parse8601(order['date'])
        price = self.safe_float(order, 'rate')
        amount = self.safe_float(order, 'amount')
        return {'info': order, 
           'id': order['order_id'], 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'symbol': symbol, 
           'type': 'limit', 
           'side': side, 
           'price': price, 
           'amount': amount}

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['pairing'] = market['id']
        response = self.privatePostGetorders(self.extend(request, params))
        orders = self.parse_orders(response['orders'], market, since, limit)
        return self.filter_by_symbol(orders, symbol)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/'
        if path:
            url += path + '/'
        if params:
            url += '?' + self.urlencode(params)
        if api == 'private':
            self.check_required_credentials()
            nonce = self.nonce()
            auth = self.apiKey + str(nonce) + self.secret
            signature = self.hash(self.encode(auth), 'sha256')
            body = self.urlencode(self.extend({'key': self.apiKey, 
               'nonce': nonce, 
               'signature': signature}, params))
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if api == 'public':
            return response
        if 'success' in response:
            if response['success']:
                return response
        raise ExchangeError(self.id + ' ' + self.json(response))