# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/foxbit.py
# Compiled at: 2018-04-27 06:35:54
from anyex.base.exchange import Exchange
from anyex.base.errors import ExchangeError

class foxbit(Exchange):

    def describe(self):
        return self.deep_extend(super(foxbit, self).describe(), {'id': 'foxbit', 
           'name': 'FoxBit', 
           'countries': 'BR', 
           'has': {'CORS': False, 
                   'createMarketOrder': False}, 
           'rateLimit': 1000, 
           'version': 'v1', 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27991413-11b40d42-647f-11e7-91ee-78ced874dd09.jpg', 
                    'api': {'public': 'https://api.blinktrade.com/api', 
                            'private': 'https://api.blinktrade.com/tapi'}, 
                    'www': 'https://foxbit.exchange', 
                    'doc': 'https://blinktrade.com/docs'}, 
           'comment': 'Blinktrade API', 
           'api': {'public': {'get': [
                                    '{currency}/ticker',
                                    '{currency}/orderbook',
                                    '{currency}/trades']}, 
                   'private': {'post': [
                                      'D',
                                      'F',
                                      'U2',
                                      'U4',
                                      'U6',
                                      'U18',
                                      'U24',
                                      'U26',
                                      'U30',
                                      'U34',
                                      'U70']}}, 
           'markets': {'BTC/VEF': {'id': 'BTCVEF', 'symbol': 'BTC/VEF', 'base': 'BTC', 'quote': 'VEF', 'brokerId': 1, 'broker': 'SurBitcoin'}, 'BTC/VND': {'id': 'BTCVND', 'symbol': 'BTC/VND', 'base': 'BTC', 'quote': 'VND', 'brokerId': 3, 'broker': 'VBTC'}, 'BTC/BRL': {'id': 'BTCBRL', 'symbol': 'BTC/BRL', 'base': 'BTC', 'quote': 'BRL', 'brokerId': 4, 'broker': 'FoxBit'}, 'BTC/PKR': {'id': 'BTCPKR', 'symbol': 'BTC/PKR', 'base': 'BTC', 'quote': 'PKR', 'brokerId': 8, 'broker': 'UrduBit'}, 'BTC/CLP': {'id': 'BTCCLP', 'symbol': 'BTC/CLP', 'base': 'BTC', 'quote': 'CLP', 'brokerId': 9, 'broker': 'ChileBit'}}, 'options': {'brokerId': '4'}})

    def fetch_balance(self, params={}):
        response = self.privatePostU2({'BalanceReqID': self.nonce()})
        balances = self.safe_value(response['Responses'], self.options['brokerId'])
        result = {'info': response}
        if balances is not None:
            currencyIds = list(self.currencies_by_id.keys())
            for i in range(0, len(currencyIds)):
                currencyId = currencyIds[i]
                currency = self.currencies_by_id[currencyId]
                code = currency['code']
                if currencyId in balances:
                    account = self.account()
                    account['used'] = float(balances[(currencyId + '_locked')]) * 1e-08
                    account['total'] = float(balances[currencyId]) * 1e-08
                    account['free'] = account['total'] - account['used']
                    result[code] = account

        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        market = self.market(symbol)
        orderbook = self.publicGetCurrencyOrderbook(self.extend({'currency': market['quote'], 
           'crypto_currency': market['base']}, params))
        return self.parse_order_book(orderbook)

    def fetch_ticker(self, symbol, params={}):
        market = self.market(symbol)
        ticker = self.publicGetCurrencyTicker(self.extend({'currency': market['quote'], 
           'crypto_currency': market['base']}, params))
        timestamp = self.milliseconds()
        lowercaseQuote = market['quote'].lower()
        quoteVolume = 'vol_' + lowercaseQuote
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
           'quoteVolume': float(ticker[quoteVolume]), 
           'info': ticker}

    def parse_trade(self, trade, market):
        timestamp = trade['date'] * 1000
        return {'id': self.safe_string(trade, 'tid'), 
           'info': trade, 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'symbol': market['symbol'], 
           'type': None, 
           'side': trade['side'], 
           'price': trade['price'], 
           'amount': trade['amount']}

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        market = self.market(symbol)
        response = self.publicGetCurrencyTrades(self.extend({'currency': market['quote'], 
           'crypto_currency': market['base']}, params))
        return self.parse_trades(response, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type == 'market':
            raise ExchangeError(self.id + ' allows limit orders only')
        market = self.market(symbol)
        orderSide = '1' if side == 'buy' else '2'
        order = {'ClOrdID': self.nonce(), 
           'Symbol': market['id'], 
           'Side': orderSide, 
           'OrdType': '2', 
           'Price': price, 
           'OrderQty': amount, 
           'BrokerID': market['brokerId']}
        response = self.privatePostD(self.extend(order, params))
        indexed = self.index_by(response['Responses'], 'MsgType')
        execution = indexed['8']
        return {'info': response, 
           'id': execution['OrderID']}

    def cancel_order(self, id, symbol=None, params={}):
        return self.privatePostF(self.extend({'ClOrdID': id}, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            request = self.extend({'MsgType': path}, query)
            body = self.json(request)
            headers = {'APIKey': self.apiKey, 
               'Nonce': nonce, 
               'Signature': self.hmac(self.encode(nonce), self.encode(self.secret)), 
               'Content-Type': 'application/json'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if 'Status' in response:
            if response['Status'] != 200:
                raise ExchangeError(self.id + ' ' + self.json(response))
        return response