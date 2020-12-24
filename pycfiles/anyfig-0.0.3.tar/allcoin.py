# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/allcoin.py
# Compiled at: 2018-04-27 06:36:25
from anyex.okcoinusd import okcoinusd

class allcoin(okcoinusd):

    def describe(self):
        return self.deep_extend(super(allcoin, self).describe(), {'id': 'allcoin', 
           'name': 'Allcoin', 
           'countries': 'CA', 
           'has': {'CORS': False}, 
           'extension': '', 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/31561809-c316b37c-b061-11e7-8d5a-b547b4d730eb.jpg', 
                    'api': {'web': 'https://www.allcoin.com', 
                            'public': 'https://api.allcoin.com/api', 
                            'private': 'https://api.allcoin.com/api'}, 
                    'www': 'https://www.allcoin.com', 
                    'doc': 'https://www.allcoin.com/About/APIReference'}, 
           'api': {'web': {'get': [
                                 'Home/MarketOverViewDetail/']}, 
                   'public': {'get': [
                                    'depth',
                                    'kline',
                                    'ticker',
                                    'trades']}, 
                   'private': {'post': [
                                      'batch_trade',
                                      'cancel_order',
                                      'order_history',
                                      'order_info',
                                      'orders_info',
                                      'repayment',
                                      'trade',
                                      'trade_history',
                                      'userinfo']}}, 
           'markets': None})

    def fetch_markets(self):
        result = []
        response = self.webGetHomeMarketOverViewDetail()
        coins = response['marketCoins']
        for j in range(0, len(coins)):
            markets = coins[j]['Markets']
            for k in range(0, len(markets)):
                market = markets[k]['Market']
                base = market['Primary']
                quote = market['Secondary']
                baseId = base.lower()
                quoteId = quote.lower()
                id = baseId + '_' + quoteId
                symbol = base + '/' + quote
                active = market['TradeEnabled'] and market['BuyEnabled'] and market['SellEnabled']
                result.append({'id': id, 
                   'symbol': symbol, 
                   'base': base, 
                   'quote': quote, 
                   'baseId': baseId, 
                   'quoteId': quoteId, 
                   'active': active, 
                   'type': 'spot', 
                   'spot': True, 
                   'future': False, 
                   'maker': market['AskFeeRate'], 
                   'taker': market['AskFeeRate'], 
                   'precision': {'amount': market['PrimaryDigits'], 
                                 'price': market['SecondaryDigits']}, 
                   'limits': {'amount': {'min': market['MinTradeAmount'], 
                                         'max': market['MaxTradeAmount']}, 
                              'price': {'min': market['MinOrderPrice'], 
                                        'max': market['MaxOrderPrice']}, 
                              'cost': {'min': None, 
                                       'max': None}}, 
                   'info': market})

        return result

    def parse_order_status(self, status):
        if status == -1:
            return 'canceled'
        if status == 0:
            return 'open'
        if status == 1:
            return 'open'
        if status == 2:
            return 'closed'
        if status == 10:
            return 'canceled'
        return status

    def get_create_date_field(self):
        return 'create_data'

    def get_orders_field(self):
        return 'order'