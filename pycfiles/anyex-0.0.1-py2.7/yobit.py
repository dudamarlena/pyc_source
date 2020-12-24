# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/anyex/yobit.py
# Compiled at: 2018-04-27 06:35:15
from anyex.liqui import liqui
from anyex.base.errors import ExchangeError
from anyex.base.errors import InsufficientFunds
from anyex.base.errors import DDoSProtection

class yobit(liqui):

    def describe(self):
        return self.deep_extend(super(yobit, self).describe(), {'id': 'yobit', 
           'name': 'YoBit', 
           'countries': 'RU', 
           'rateLimit': 3000, 
           'version': '3', 
           'has': {'createDepositAddress': True, 
                   'fetchDepositAddress': True, 
                   'CORS': False, 
                   'withdraw': True}, 
           'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27766910-cdcbfdae-5eea-11e7-9859-03fea873272d.jpg', 
                    'api': {'public': 'https://yobit.net/api', 
                            'private': 'https://yobit.net/tapi'}, 
                    'www': 'https://www.yobit.net', 
                    'doc': 'https://www.yobit.net/en/api/', 
                    'fees': 'https://www.yobit.net/en/fees/'}, 
           'api': {'public': {'get': [
                                    'depth/{pair}',
                                    'info',
                                    'ticker/{pair}',
                                    'trades/{pair}']}, 
                   'private': {'post': [
                                      'ActiveOrders',
                                      'CancelOrder',
                                      'GetDepositAddress',
                                      'getInfo',
                                      'OrderInfo',
                                      'Trade',
                                      'TradeHistory',
                                      'WithdrawCoinsToAddress']}}, 
           'fees': {'trading': {'maker': 0.002, 
                                'taker': 0.002}, 
                    'funding': {'withdraw': {}}}, 
           'commonCurrencies': {'AIR': 'AirCoin', 
                                'ANI': 'ANICoin', 
                                'ANT': 'AntsCoin', 
                                'AST': 'Astral', 
                                'ATM': 'Autumncoin', 
                                'BCC': 'BCH', 
                                'BCS': 'BitcoinStake', 
                                'BLN': 'Bulleon', 
                                'BTS': 'Bitshares2', 
                                'CAT': 'BitClave', 
                                'COV': 'Coven Coin', 
                                'CPC': 'Capricoin', 
                                'CS': 'CryptoSpots', 
                                'DCT': 'Discount', 
                                'DGD': 'DarkGoldCoin', 
                                'DROP': 'FaucetCoin', 
                                'ERT': 'Eristica Token', 
                                'ICN': 'iCoin', 
                                'KNC': 'KingN Coin', 
                                'LIZI': 'LiZi', 
                                'LOC': 'LocoCoin', 
                                'LOCX': 'LOC', 
                                'LUN': 'LunarCoin', 
                                'MDT': 'Midnight', 
                                'NAV': 'NavajoCoin', 
                                'OMG': 'OMGame', 
                                'STK': 'StakeCoin', 
                                'PAY': 'EPAY', 
                                'PLC': 'Platin Coin', 
                                'REP': 'Republicoin', 
                                'RUR': 'RUB', 
                                'XIN': 'XINCoin'}, 
           'options': {'fetchOrdersRequiresSymbol': True}})

    def parse_order_status(self, status):
        statuses = {'0': 'open', 
           '1': 'closed', 
           '2': 'canceled', 
           '3': 'open'}
        if status in statuses:
            return statuses[status]
        return status

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostGetInfo()
        balances = response['return']
        result = {'info': balances}
        sides = {'free': 'funds', 'total': 'funds_incl_orders'}
        keys = list(sides.keys())
        for i in range(0, len(keys)):
            key = keys[i]
            side = sides[key]
            if side in balances:
                currencies = list(balances[side].keys())
                for j in range(0, len(currencies)):
                    lowercase = currencies[j]
                    uppercase = lowercase.upper()
                    currency = self.common_currency_code(uppercase)
                    account = None
                    if currency in result:
                        account = result[currency]
                    else:
                        account = self.account()
                    account[key] = balances[side][lowercase]
                    if account['total'] and account['free']:
                        account['used'] = account['total'] - account['free']
                    result[currency] = account

        return self.parse_balance(result)

    def create_deposit_address(self, code, params={}):
        response = self.fetch_deposit_address(code, self.extend({'need_new': 1}, params))
        address = self.safe_string(response, 'address')
        self.check_address(address)
        return {'currency': code, 
           'address': address, 
           'status': 'ok', 
           'info': response['info']}

    def fetch_deposit_address(self, code, params={}):
        currency = self.currency(code)
        request = {'coinName': currency['id'], 
           'need_new': 0}
        response = self.privatePostGetDepositAddress(self.extend(request, params))
        address = self.safe_string(response['return'], 'address')
        self.check_address(address)
        return {'currency': code, 
           'address': address, 
           'status': 'ok', 
           'info': response}

    def withdraw(self, currency, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        response = self.privatePostWithdrawCoinsToAddress(self.extend({'coinName': currency, 
           'amount': amount, 
           'address': address}, params))
        return {'info': response, 
           'id': None}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if 'success' in response:
            if not response['success']:
                if response['error'].find('Insufficient funds') >= 0:
                    raise InsufficientFunds(self.id + ' ' + self.json(response))
                elif response['error'] == 'Requests too often':
                    raise DDoSProtection(self.id + ' ' + self.json(response))
                elif response['error'] == 'not available' or response['error'] == 'external service unavailable':
                    raise DDoSProtection(self.id + ' ' + self.json(response))
                else:
                    raise ExchangeError(self.id + ' ' + self.json(response))
        return response