# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/coincheck.py
# Compiled at: 2018-04-27 06:36:04
from anyex.base.exchange import Exchange
from anyex.base.errors import ExchangeError
from anyex.base.errors import NotSupported

class coincheck(Exchange):

    def describe(self):
        return self.deep_extend(super(coincheck, self).describe(), {'id': 'coincheck', 
           'name': 'coincheck', 
           'countries': [
                       'JP', 'ID'], 
           'rateLimit': 1500, 
           'has': {'CORS': False}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27766464-3b5c3c74-5ed9-11e7-840e-31b32968e1da.jpg', 
                    'api': 'https://coincheck.com/api', 
                    'www': 'https://coincheck.com', 
                    'doc': 'https://coincheck.com/documents/exchange/api'}, 
           'api': {'public': {'get': [
                                    'exchange/orders/rate',
                                    'order_books',
                                    'rate/{pair}',
                                    'ticker',
                                    'trades']}, 
                   'private': {'get': [
                                     'accounts',
                                     'accounts/balance',
                                     'accounts/leverage_balance',
                                     'bank_accounts',
                                     'deposit_money',
                                     'exchange/orders/opens',
                                     'exchange/orders/transactions',
                                     'exchange/orders/transactions_pagination',
                                     'exchange/leverage/positions',
                                     'lending/borrows/matches',
                                     'send_money',
                                     'withdraws'], 
                               'post': [
                                      'bank_accounts',
                                      'deposit_money/{id}/fast',
                                      'exchange/orders',
                                      'exchange/transfers/to_leverage',
                                      'exchange/transfers/from_leverage',
                                      'lending/borrows',
                                      'lending/borrows/{id}/repay',
                                      'send_money',
                                      'withdraws'], 
                               'delete': [
                                        'bank_accounts/{id}',
                                        'exchange/orders/{id}',
                                        'withdraws/{id}']}}, 
           'markets': {'BTC/JPY': {'id': 'btc_jpy', 'symbol': 'BTC/JPY', 'base': 'BTC', 'quote': 'JPY'}}})

    def fetch_balance(self, params={}):
        balances = self.privateGetAccountsBalance()
        result = {'info': balances}
        currencies = list(self.currencies.keys())
        for i in range(0, len(currencies)):
            currency = currencies[i]
            lowercase = currency.lower()
            account = self.account()
            if lowercase in balances:
                account['free'] = float(balances[lowercase])
            reserved = lowercase + '_reserved'
            if reserved in balances:
                account['used'] = float(balances[reserved])
            account['total'] = self.sum(account['free'], account['used'])
            result[currency] = account

        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        if symbol != 'BTC/JPY':
            raise NotSupported(self.id + ' fetchOrderBook() supports BTC/JPY only')
        orderbook = self.publicGetOrderBooks(params)
        return self.parse_order_book(orderbook)

    def fetch_ticker(self, symbol, params={}):
        if symbol != 'BTC/JPY':
            raise NotSupported(self.id + ' fetchTicker() supports BTC/JPY only')
        ticker = self.publicGetTicker(params)
        timestamp = ticker['timestamp'] * 1000
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
           'open': None, 
           'close': last, 
           'last': last, 
           'previousClose': None, 
           'change': None, 
           'percentage': None, 
           'average': None, 
           'baseVolume': float(ticker['volume']), 
           'quoteVolume': None, 
           'info': ticker}

    def parse_trade(self, trade, market):
        timestamp = self.parse8601(trade['created_at'])
        return {'id': str(trade['id']), 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'symbol': market['symbol'], 
           'type': None, 
           'side': trade['order_type'], 
           'price': float(trade['rate']), 
           'amount': float(trade['amount']), 
           'info': trade}

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        if symbol != 'BTC/JPY':
            raise NotSupported(self.id + ' fetchTrades() supports BTC/JPY only')
        market = self.market(symbol)
        response = self.publicGetTrades(self.extend({'pair': market['id']}, params))
        if 'success' in response:
            if response['success']:
                if response['data'] is not None:
                    return self.parse_trades(response['data'], market, since, limit)
        raise ExchangeError(self.id + ' ' + self.json(response))
        return

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        order = {'pair': self.market_id(symbol)}
        if type == 'market':
            order_type = type + '_' + side
            order['order_type'] = order_type
            prefix = order_type + '_' if side == 'buy' else ''
            order[prefix + 'amount'] = amount
        else:
            order['order_type'] = side
            order['rate'] = price
            order['amount'] = amount
        response = self.privatePostExchangeOrders(self.extend(order, params))
        return {'info': response, 
           'id': str(response['id'])}

    def cancel_order(self, id, symbol=None, params={}):
        return self.privateDeleteExchangeOrdersId({'id': id})

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            queryString = ''
            if method == 'GET':
                if query:
                    url += '?' + self.urlencode(self.keysort(query))
            elif query:
                body = self.urlencode(self.keysort(query))
                queryString = body
            auth = nonce + url + queryString
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 
               'ACCESS-KEY': self.apiKey, 
               'ACCESS-NONCE': nonce, 
               'ACCESS-SIGNATURE': self.hmac(self.encode(auth), self.encode(self.secret))}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if api == 'public':
            return response
        if 'success' in response:
            if response['success']:
                return response
        raise ExchangeError(self.id + ' ' + self.json(response))