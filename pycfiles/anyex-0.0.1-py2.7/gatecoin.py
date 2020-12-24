# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/gatecoin.py
# Compiled at: 2018-04-27 06:35:52
from anyex.base.exchange import Exchange
import hashlib, math
from anyex.base.errors import ExchangeError
from anyex.base.errors import AuthenticationError
from anyex.base.errors import InvalidAddress

class gatecoin(Exchange):

    def describe(self):
        return self.deep_extend(super(gatecoin, self).describe(), {'id': 'gatecoin', 
           'name': 'Gatecoin', 
           'rateLimit': 2000, 
           'countries': 'HK', 
           'comment': 'a regulated/licensed exchange', 
           'has': {'CORS': False, 
                   'createDepositAddress': True, 
                   'fetchDepositAddress': True, 
                   'fetchOHLCV': True, 
                   'fetchOpenOrders': True, 
                   'fetchOrder': True, 
                   'fetchTickers': True, 
                   'withdraw': True}, 
           'timeframes': {'1m': '1m', 
                          '15m': '15m', 
                          '1h': '1h', 
                          '6h': '6h', 
                          '1d': '24h'}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/28646817-508457f2-726c-11e7-9eeb-3528d2413a58.jpg', 
                    'api': 'https://api.gatecoin.com', 
                    'www': 'https://gatecoin.com', 
                    'doc': [
                          'https://gatecoin.com/api',
                          'https://github.com/Gatecoin/RESTful-API-Implementation',
                          'https://api.gatecoin.com/swagger-ui/index.html']}, 
           'api': {'public': {'get': [
                                    'Public/ExchangeRate',
                                    'Public/LiveTicker',
                                    'Public/LiveTicker/{CurrencyPair}',
                                    'Public/LiveTickers',
                                    'Public/MarketDepth/{CurrencyPair}',
                                    'Public/NetworkStatistics/{DigiCurrency}',
                                    'Public/StatisticHistory/{DigiCurrency}/{Typeofdata}',
                                    'Public/TickerHistory/{CurrencyPair}/{Timeframe}',
                                    'Public/Transactions/{CurrencyPair}',
                                    'Public/TransactionsHistory/{CurrencyPair}',
                                    'Reference/BusinessNatureList',
                                    'Reference/Countries',
                                    'Reference/Currencies',
                                    'Reference/CurrencyPairs',
                                    'Reference/CurrentStatusList',
                                    'Reference/IdentydocumentTypes',
                                    'Reference/IncomeRangeList',
                                    'Reference/IncomeSourceList',
                                    'Reference/VerificationLevelList',
                                    'Stream/PublicChannel'], 
                              'post': [
                                     'Export/Transactions',
                                     'Ping',
                                     'Public/Unsubscribe/{EmailCode}',
                                     'RegisterUser']}, 
                   'private': {'get': [
                                     'Account/CorporateData',
                                     'Account/DocumentAddress',
                                     'Account/DocumentCorporation',
                                     'Account/DocumentID',
                                     'Account/DocumentInformation',
                                     'Account/Email',
                                     'Account/FeeRate',
                                     'Account/Level',
                                     'Account/PersonalInformation',
                                     'Account/Phone',
                                     'Account/Profile',
                                     'Account/Questionnaire',
                                     'Account/Referral',
                                     'Account/ReferralCode',
                                     'Account/ReferralNames',
                                     'Account/ReferralReward',
                                     'Account/ReferredCode',
                                     'Account/ResidentInformation',
                                     'Account/SecuritySettings',
                                     'Account/User',
                                     'APIKey/APIKey',
                                     'Auth/ConnectionHistory',
                                     'Balance/Balances',
                                     'Balance/Balances/{Currency}',
                                     'Balance/Deposits',
                                     'Balance/Withdrawals',
                                     'Bank/Accounts/{Currency}/{Location}',
                                     'Bank/Transactions',
                                     'Bank/UserAccounts',
                                     'Bank/UserAccounts/{Currency}',
                                     'ElectronicWallet/DepositWallets',
                                     'ElectronicWallet/DepositWallets/{DigiCurrency}',
                                     'ElectronicWallet/Transactions',
                                     'ElectronicWallet/Transactions/{DigiCurrency}',
                                     'ElectronicWallet/UserWallets',
                                     'ElectronicWallet/UserWallets/{DigiCurrency}',
                                     'Info/ReferenceCurrency',
                                     'Info/ReferenceLanguage',
                                     'Notification/Messages',
                                     'Trade/Orders',
                                     'Trade/Orders/{OrderID}',
                                     'Trade/StopOrders',
                                     'Trade/StopOrdersHistory',
                                     'Trade/Trades',
                                     'Trade/UserTrades'], 
                               'post': [
                                      'Account/DocumentAddress',
                                      'Account/DocumentCorporation',
                                      'Account/DocumentID',
                                      'Account/Email/RequestVerify',
                                      'Account/Email/Verify',
                                      'Account/GoogleAuth',
                                      'Account/Level',
                                      'Account/Questionnaire',
                                      'Account/Referral',
                                      'APIKey/APIKey',
                                      'Auth/ChangePassword',
                                      'Auth/ForgotPassword',
                                      'Auth/ForgotUserID',
                                      'Auth/Login',
                                      'Auth/Logout',
                                      'Auth/LogoutOtherSessions',
                                      'Auth/ResetPassword',
                                      'Bank/Transactions',
                                      'Bank/UserAccounts',
                                      'ElectronicWallet/DepositWallets/{DigiCurrency}',
                                      'ElectronicWallet/Transactions/Deposits/{DigiCurrency}',
                                      'ElectronicWallet/Transactions/Withdrawals/{DigiCurrency}',
                                      'ElectronicWallet/UserWallets/{DigiCurrency}',
                                      'ElectronicWallet/Withdrawals/{DigiCurrency}',
                                      'Notification/Messages',
                                      'Notification/Messages/{ID}',
                                      'Trade/Orders',
                                      'Trade/StopOrders'], 
                               'put': [
                                     'Account/CorporateData',
                                     'Account/DocumentID',
                                     'Account/DocumentInformation',
                                     'Account/Email',
                                     'Account/PersonalInformation',
                                     'Account/Phone',
                                     'Account/Questionnaire',
                                     'Account/ReferredCode',
                                     'Account/ResidentInformation',
                                     'Account/SecuritySettings',
                                     'Account/User',
                                     'Bank/UserAccounts',
                                     'ElectronicWallet/DepositWallets/{DigiCurrency}/{AddressName}',
                                     'ElectronicWallet/UserWallets/{DigiCurrency}',
                                     'Info/ReferenceCurrency',
                                     'Info/ReferenceLanguage'], 
                               'delete': [
                                        'APIKey/APIKey/{PublicKey}',
                                        'Bank/Transactions/{RequestID}',
                                        'Bank/UserAccounts/{Currency}/{Label}',
                                        'ElectronicWallet/DepositWallets/{DigiCurrency}/{AddressName}',
                                        'ElectronicWallet/UserWallets/{DigiCurrency}/{AddressName}',
                                        'Trade/Orders',
                                        'Trade/Orders/{OrderID}',
                                        'Trade/StopOrders',
                                        'Trade/StopOrders/{ID}']}}, 
           'fees': {'trading': {'maker': 0.0025, 
                                'taker': 0.0035}}, 
           'commonCurrencies': {'MAN': 'MANA'}})

    def fetch_markets(self):
        response = self.publicGetReferenceCurrencyPairs()
        markets = response['currencyPairs']
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = market['tradingCode']
            baseId = market['baseCurrency']
            quoteId = market['quoteCurrency']
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {'amount': 8, 
               'price': market['priceDecimalPlaces']}
            limits = {'amount': {'min': math.pow(10, -precision['amount']), 
                          'max': None}, 
               'price': {'min': math.pow(10, -precision['amount']), 
                         'max': None}, 
               'cost': {'min': None, 
                        'max': None}}
            result.append({'id': id, 
               'symbol': symbol, 
               'base': base, 
               'quote': quote, 
               'baseId': baseId, 
               'quoteId': quoteId, 
               'active': True, 
               'precision': precision, 
               'limits': limits, 
               'info': market})

        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetBalanceBalances()
        balances = response['balances']
        result = {'info': balances}
        for b in range(0, len(balances)):
            balance = balances[b]
            currencyId = balance['currency']
            code = currencyId
            if currencyId in self.currencies_by_id:
                code = self.currencies_by_id[currencyId]['code']
            account = {'free': balance['availableBalance'], 'used': self.sum(balance['pendingIncoming'], balance['pendingOutgoing'], balance['openOrder']), 
               'total': balance['balance']}
            result[code] = account

        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        orderbook = self.publicGetPublicMarketDepthCurrencyPair(self.extend({'CurrencyPair': market['id']}, params))
        return self.parse_order_book(orderbook, None, 'bids', 'asks', 'price', 'volume')

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        response = self.privateGetTradeOrdersOrderID(self.extend({'OrderID': id}, params))
        return self.parse_order(response.order)

    def parse_ticker(self, ticker, market=None):
        timestamp = int(ticker['createDateTime']) * 1000
        symbol = None
        if market:
            symbol = market['symbol']
        baseVolume = float(ticker['volume'])
        vwap = float(ticker['vwap'])
        quoteVolume = baseVolume * vwap
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
           'vwap': vwap, 
           'open': float(ticker['open']), 
           'close': last, 
           'last': last, 
           'previousClose': None, 
           'change': None, 
           'percentage': None, 
           'average': None, 
           'baseVolume': baseVolume, 
           'quoteVolume': quoteVolume, 
           'info': ticker}

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetPublicLiveTickers(params)
        tickers = response['tickers']
        result = {}
        for t in range(0, len(tickers)):
            ticker = tickers[t]
            id = ticker['currencyPair']
            market = self.markets_by_id[id]
            symbol = market['symbol']
            result[symbol] = self.parse_ticker(ticker, market)

        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetPublicLiveTickerCurrencyPair(self.extend({'CurrencyPair': market['id']}, params))
        ticker = response['ticker']
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        side = None
        orderId = None
        if 'way' in trade:
            side = 'buy' if trade['way'] == 'bid' else 'sell'
            orderIdField = trade['way'] + 'OrderId'
            orderId = self.safe_string(trade, orderIdField)
        timestamp = int(trade['transactionTime']) * 1000
        if market is None:
            marketId = self.safe_string(trade, 'currencyPair')
            if marketId is not None:
                market = self.find_market(marketId)
        fee = None
        feeCost = self.safe_float(trade, 'feeAmount')
        price = trade['price']
        amount = trade['quantity']
        cost = price * amount
        feeCurrency = None
        symbol = None
        if market is not None:
            symbol = market['symbol']
            feeCurrency = market['quote']
        if feeCost is not None:
            fee = {'cost': feeCost, 'currency': feeCurrency, 
               'rate': self.safe_float(trade, 'feeRate')}
        return {'info': trade, 
           'id': self.safe_string(trade, 'transactionId'), 
           'order': orderId, 
           'timestamp': timestamp, 
           'datetime': self.iso8601(timestamp), 
           'symbol': symbol, 
           'type': None, 
           'side': side, 
           'price': price, 
           'amount': amount, 
           'cost': cost, 
           'fee': fee}

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetPublicTransactionsCurrencyPair(self.extend({'CurrencyPair': market['id']}, params))
        return self.parse_trades(response['transactions'], market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
         int(ohlcv['createDateTime']) * 1000,
         ohlcv['open'],
         ohlcv['high'],
         ohlcv['low'],
         None,
         ohlcv['volume']]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {'CurrencyPair': market['id'], 
           'Timeframe': self.timeframes[timeframe]}
        if limit is not None:
            request['Count'] = limit
        request = self.extend(request, params)
        response = self.publicGetPublicTickerHistoryCurrencyPairTimeframe(request)
        ohlcvs = self.parse_ohlcvs(response['tickers'], market, timeframe, since, limit)
        return self.sort_by(ohlcvs, 0)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        order = {'Code': self.market_id(symbol), 
           'Way': 'Bid' if side == 'buy' else 'Ask', 
           'Amount': amount}
        if type == 'limit':
            order['Price'] = price
        if self.twofa:
            if 'ValidationCode' in params:
                order['ValidationCode'] = params['ValidationCode']
            else:
                raise AuthenticationError(self.id + ' two-factor authentication requires a missing ValidationCode parameter')
        response = self.privatePostTradeOrders(self.extend(order, params))
        return {'info': response, 
           'id': response['clOrderId']}

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        return self.privateDeleteTradeOrdersOrderID({'OrderID': id})

    def parse_order_status(self, status):
        statuses = {'6': 'closed'}
        if status in statuses:
            return statuses[status]
        return status

    def parse_order(self, order, market=None):
        side = 'buy' if order['side'] == 0 else 'sell'
        type = 'limit' if order['type'] == 0 else 'market'
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'code')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        timestamp = int(order['date']) * 1000
        amount = order['initialQuantity']
        remaining = order['remainingQuantity']
        filled = amount - remaining
        price = order['price']
        cost = price * filled
        id = order['clOrderId']
        status = self.parse_order_status(self.safe_string(order, 'status'))
        trades = None
        fee = None
        if status == 'closed':
            tradesFilled = None
            tradesCost = None
            trades = []
            transactions = self.safe_value(order, 'trades')
            feeCost = None
            feeCurrency = None
            feeRate = None
            if transactions is not None:
                if isinstance(transactions, list):
                    for i in range(0, len(transactions)):
                        trade = self.parse_trade(transactions[i])
                        if tradesFilled is None:
                            tradesFilled = 0.0
                        if tradesCost is None:
                            tradesCost = 0.0
                        tradesFilled += trade['amount']
                        tradesCost += trade['amount'] * trade['price']
                        if 'fee' in trade:
                            if trade['fee']['cost'] is not None:
                                if feeCost is None:
                                    feeCost = 0.0
                                feeCost += trade['fee']['cost']
                            feeCurrency = trade['fee']['currency']
                            if trade['fee']['rate'] is not None:
                                if feeRate is None:
                                    feeRate = 0.0
                                feeRate += trade['fee']['rate']
                        trades.append(trade)

                    if tradesFilled is not None and tradesFilled > 0:
                        price = tradesCost / tradesFilled
                    if feeRate is not None:
                        numTrades = len(trades)
                        if numTrades > 0:
                            feeRate = feeRate / numTrades
                    if feeCost is not None:
                        fee = {'cost': feeCost, 'currency': feeCurrency, 
                           'rate': feeRate}
        result = {'id': id, 
           'datetime': self.iso8601(timestamp), 
           'timestamp': timestamp, 
           'lastTradeTimestamp': None, 
           'status': status, 
           'symbol': symbol, 
           'type': type, 
           'side': side, 
           'price': price, 
           'amount': amount, 
           'filled': filled, 
           'remaining': remaining, 
           'cost': cost, 
           'trades': trades, 
           'fee': fee, 
           'info': order}
        return result

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        response = self.privateGetTradeOrders()
        orders = self.parse_orders(response['orders'], None, since, limit)
        if symbol is not None:
            return self.filter_by_symbol(orders, symbol)
        else:
            return orders

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            nonceString = str(nonce)
            contentType = '' if method == 'GET' else 'application/json'
            auth = method + url + contentType + nonceString
            auth = auth.lower()
            signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha256, 'base64')
            headers = {'API_PUBLIC_KEY': self.apiKey, 
               'API_REQUEST_SIGNATURE': self.decode(signature), 
               'API_REQUEST_DATE': nonceString}
            if method != 'GET':
                headers['Content-Type'] = contentType
                body = self.json(self.extend({'nonce': nonce}, params))
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if 'responseStatus' in response:
            if 'message' in response['responseStatus']:
                if response['responseStatus']['message'] == 'OK':
                    return response
        raise ExchangeError(self.id + ' ' + self.json(response))

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        request = {'DigiCurrency': currency['id'], 
           'Address': address, 
           'Amount': amount}
        response = self.privatePostElectronicWalletWithdrawalsDigiCurrency(self.extend(request, params))
        return {'info': response, 
           'id': self.safe_string(response, 'id')}

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        request = {'DigiCurrency': currency['id']}
        response = self.privateGetElectronicWalletDepositWalletsDigiCurrency(self.extend(request, params))
        result = response['addresses']
        numResults = len(result)
        if numResults < 1:
            raise InvalidAddress(self.id + ' privateGetElectronicWalletDepositWalletsDigiCurrency() returned no addresses')
        address = self.safe_string(result[0], 'address')
        self.check_address(address)
        return {'currency': code, 
           'address': address, 
           'status': 'ok', 
           'info': response}

    def create_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        request = {'DigiCurrency': currency['id']}
        response = self.privatePostElectronicWalletDepositWalletsDigiCurrency(self.extend(request, params))
        result = response['addresses']
        numResults = len(result)
        if numResults < 1:
            raise InvalidAddress(self.id + ' privatePostElectronicWalletDepositWalletsDigiCurrency() returned no addresses')
        address = self.safe_string(result[0], 'address')
        self.check_address(address)
        return {'currency': code, 
           'address': address, 
           'status': 'ok', 
           'info': response}