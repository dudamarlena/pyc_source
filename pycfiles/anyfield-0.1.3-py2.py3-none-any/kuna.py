# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/kuna.py
# Compiled at: 2018-04-27 06:35:42
from anyex.acx import acx
from anyex.base.errors import ExchangeError

class kuna(acx):

    def describe(self):
        return self.deep_extend(super(kuna, self).describe(), {'id': 'kuna', 
           'name': 'Kuna', 
           'countries': 'UA', 
           'rateLimit': 1000, 
           'version': 'v2', 
           'has': {'CORS': False, 
                   'fetchTickers': True, 
                   'fetchOpenOrders': True, 
                   'fetchMyTrades': True, 
                   'withdraw': False}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/31697638-912824fa-b3c1-11e7-8c36-cf9606eb94ac.jpg', 
                    'api': 'https://kuna.io', 
                    'www': 'https://kuna.io', 
                    'doc': 'https://kuna.io/documents/api', 
                    'fees': 'https://kuna.io/documents/api'}, 
           'fees': {'trading': {'taker': 0.25 / 100, 
                                'maker': 0.25 / 100}, 
                    'funding': {'withdraw': {'UAH': '1%', 
                                             'BTC': 0.001, 
                                             'BCH': 0.001, 
                                             'ETH': 0.01, 
                                             'WAVES': 0.01, 
                                             'GOL': 0.0, 
                                             'GBG': 0.0}, 
                                'deposit': {}}}})

    def fetch_markets(self):
        predefinedMarkets = [{'id': 'btcuah', 'symbol': 'BTC/UAH', 'base': 'BTC', 'quote': 'UAH', 'baseId': 'btc', 'quoteId': 'uah', 'precision': {'amount': 6, 'price': 0}, 'lot': 1e-06, 'limits': {'amount': {'min': 1e-06, 'max': None}, 'price': {'min': 1, 'max': None}, 'cost': {'min': 1e-06, 'max': None}}}, {'id': 'ethuah', 'symbol': 'ETH/UAH', 'base': 'ETH', 'quote': 'UAH', 'baseId': 'eth', 'quoteId': 'uah', 'precision': {'amount': 6, 'price': 0}, 'lot': 1e-06, 'limits': {'amount': {'min': 1e-06, 'max': None}, 'price': {'min': 1, 'max': None}, 'cost': {'min': 1e-06, 'max': None}}}, {'id': 'gbguah', 'symbol': 'GBG/UAH', 'base': 'GBG', 'quote': 'UAH', 'baseId': 'gbg', 'quoteId': 'uah', 'precision': {'amount': 3, 'price': 2}, 'lot': 0.001, 'limits': {'amount': {'min': 1e-06, 'max': None}, 'price': {'min': 0.01, 'max': None}, 'cost': {'min': 1e-06, 'max': None}}}, {'id': 'kunbtc', 'symbol': 'KUN/BTC', 'base': 'KUN', 'quote': 'BTC', 'baseId': 'kun', 'quoteId': 'btc', 'precision': {'amount': 6, 'price': 6}, 'lot': 1e-06, 'limits': {'amount': {'min': 1e-06, 'max': None}, 'price': {'min': 1e-06, 'max': None}, 'cost': {'min': 1e-06, 'max': None}}}, {'id': 'bchbtc', 'symbol': 'BCH/BTC', 'base': 'BCH', 'quote': 'BTC', 'baseId': 'bch', 'quoteId': 'btc', 'precision': {'amount': 6, 'price': 6}, 'lot': 1e-06, 'limits': {'amount': {'min': 1e-06, 'max': None}, 'price': {'min': 1e-06, 'max': None}, 'cost': {'min': 1e-06, 'max': None}}}, {'id': 'bchuah', 'symbol': 'BCH/UAH', 'base': 'BCH', 'quote': 'UAH', 'baseId': 'bch', 'quoteId': 'uah', 'precision': {'amount': 6, 'price': 0}, 'lot': 1e-06, 'limits': {'amount': {'min': 1e-06, 'max': None}, 'price': {'min': 1, 'max': None}, 'cost': {'min': 1e-06, 'max': None}}}, {'id': 'wavesuah', 'symbol': 'WAVES/UAH', 'base': 'WAVES', 'quote': 'UAH', 'baseId': 'waves', 'quoteId': 'uah', 'precision': {'amount': 6, 'price': 0}, 'lot': 1e-06, 'limits': {'amount': {'min': 1e-06, 'max': None}, 'price': {'min': 1, 'max': None}, 'cost': {'min': 1e-06, 'max': None}}}, {'id': 'arnbtc', 'symbol': 'ARN/BTC', 'base': 'ARN', 'quote': 'BTC', 'baseId': 'arn', 'quoteId': 'btc'}, {'id': 'b2bbtc', 'symbol': 'B2B/BTC', 'base': 'B2B', 'quote': 'BTC', 'baseId': 'b2b', 'quoteId': 'btc'}, {'id': 'evrbtc', 'symbol': 'EVR/BTC', 'base': 'EVR', 'quote': 'BTC', 'baseId': 'evr', 'quoteId': 'btc'}, {'id': 'golgbg', 'symbol': 'GOL/GBG', 'base': 'GOL', 'quote': 'GBG', 'baseId': 'gol', 'quoteId': 'gbg'}, {'id': 'rbtc', 'symbol': 'R/BTC', 'base': 'R', 'quote': 'BTC', 'baseId': 'r', 'quoteId': 'btc'}, {'id': 'rmcbtc', 'symbol': 'RMC/BTC', 'base': 'RMC', 'quote': 'BTC', 'baseId': 'rmc', 'quoteId': 'btc'}]
        markets = []
        tickers = self.publicGetTickers()
        for i in range(0, len(predefinedMarkets)):
            market = predefinedMarkets[i]
            if market['id'] in tickers:
                markets.append(market)

        marketsById = self.index_by(markets, 'id')
        ids = list(tickers.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            if id not in list(marketsById.keys()):
                baseId = id.replace('btc', '')
                baseId = baseId.replace('uah', '')
                baseId = baseId.replace('gbg', '')
                if len(baseId) > 0:
                    baseIdLength = len(baseId) - 0
                    quoteId = id[baseIdLength:]
                    base = baseId.upper()
                    quote = quoteId.upper()
                    base = self.common_currency_code(base)
                    quote = self.common_currency_code(quote)
                    symbol = base + '/' + quote
                    markets.append({'id': id, 
                       'symbol': symbol, 
                       'base': base, 
                       'quote': quote, 
                       'baseId': baseId, 
                       'quoteId': quoteId})

        return markets

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        orderBook = self.publicGetOrderBook(self.extend({'market': market['id']}, params))
        return self.parse_order_book(orderBook, None, 'bids', 'asks', 'price', 'remaining_volume')

    def fetch_l3_order_book(self, symbol, limit=None, params={}):
        return self.fetch_order_book(symbol, limit, params)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchOpenOrders requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        orders = self.privateGetOrders(self.extend({'market': market['id']}, params))
        return self.parse_orders(orders, market, since, limit)

    def parse_trade(self, trade, market=None):
        timestamp = self.parse8601(trade['created_at'])
        symbol = None
        if market:
            symbol = market['symbol']
        return {'id': str(trade['id']), 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'symbol': symbol, 
           'type': None, 
           'side': None, 
           'price': float(trade['price']), 
           'amount': float(trade['volume']), 
           'info': trade}

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetTrades(self.extend({'market': market['id']}, params))
        return self.parse_trades(response, market, since, limit)

    def parse_my_trade(self, trade, market):
        timestamp = self.parse8601(trade['created_at'])
        symbol = None
        if market:
            symbol = market['symbol']
        return {'id': trade['id'], 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'price': trade['price'], 
           'amount': trade['volume'], 
           'cost': trade['funds'], 
           'symbol': symbol, 
           'side': trade['side'], 
           'order': trade['order_id']}

    def parse_my_trades(self, trades, market=None):
        parsedTrades = []
        for i in range(0, len(trades)):
            trade = trades[i]
            parsedTrade = self.parse_my_trade(trade, market)
            parsedTrades.append(parsedTrade)

        return parsedTrades

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        if not symbol:
            raise ExchangeError(self.id + ' fetchOpenOrders requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        response = self.privateGetTradesMy({'market': market['id']})
        return self.parse_my_trades(response, market)