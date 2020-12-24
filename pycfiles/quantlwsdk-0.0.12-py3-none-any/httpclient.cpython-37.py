# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\bitstamp\httpclient.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 6942 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import time, datetime, hmac, hashlib, requests, threading
from pyalgotrade.utils import dt
from pyalgotrade.bitstamp import common
import logging
logging.getLogger('requests').setLevel(logging.ERROR)

def parse_datetime(dateTime):
    try:
        ret = datetime.datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        ret = datetime.datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S.%f')

    return dt.as_utc(ret)


class NonceGenerator(object):

    def __init__(self):
        self._NonceGenerator__prev = None

    def getNext(self):
        ret = int(time.time())
        if self._NonceGenerator__prev is not None:
            if ret <= self._NonceGenerator__prev:
                ret = self._NonceGenerator__prev + 1
        self._NonceGenerator__prev = ret
        return ret


class AccountBalance(object):

    def __init__(self, jsonDict):
        self._AccountBalance__jsonDict = jsonDict

    def getDict(self):
        return self._AccountBalance__jsonDict

    def getUSDAvailable(self):
        return float(self._AccountBalance__jsonDict['usd_available'])

    def getBTCAvailable(self):
        return float(self._AccountBalance__jsonDict['btc_available'])


class Order(object):

    def __init__(self, jsonDict):
        self._Order__jsonDict = jsonDict

    def getDict(self):
        return self._Order__jsonDict

    def getId(self):
        return int(self._Order__jsonDict['id'])

    def isBuy(self):
        return self._Order__jsonDict['type'] == 0

    def isSell(self):
        return self._Order__jsonDict['type'] == 1

    def getPrice(self):
        return float(self._Order__jsonDict['price'])

    def getAmount(self):
        return float(self._Order__jsonDict['amount'])

    def getDateTime(self):
        return parse_datetime(self._Order__jsonDict['datetime'])


class UserTransaction(object):

    def __init__(self, jsonDict):
        self._UserTransaction__jsonDict = jsonDict

    def getDict(self):
        return self._UserTransaction__jsonDict

    def getBTC(self):
        return float(self._UserTransaction__jsonDict['btc'])

    def getBTCUSD(self):
        return float(self._UserTransaction__jsonDict['btc_usd'])

    def getDateTime(self):
        return parse_datetime(self._UserTransaction__jsonDict['datetime'])

    def getFee(self):
        return float(self._UserTransaction__jsonDict['fee'])

    def getId(self):
        return int(self._UserTransaction__jsonDict['id'])

    def getOrderId(self):
        return int(self._UserTransaction__jsonDict['order_id'])

    def getUSD(self):
        return float(self._UserTransaction__jsonDict['usd'])


class HTTPClient(object):
    USER_AGENT = 'PyAlgoTrade'
    REQUEST_TIMEOUT = 30

    class UserTransactionType:
        MARKET_TRADE = 2

    def __init__(self, clientId, key, secret):
        self._HTTPClient__clientId = clientId
        self._HTTPClient__key = key
        self._HTTPClient__secret = secret
        self._HTTPClient__nonce = NonceGenerator()
        self._HTTPClient__lock = threading.Lock()

    def _buildQuery(self, params):
        nonce = self._HTTPClient__nonce.getNext()
        message = '%d%s%s' % (nonce, self._HTTPClient__clientId, self._HTTPClient__key)
        signature = hmac.new((self._HTTPClient__secret), msg=message, digestmod=(hashlib.sha256)).hexdigest().upper()
        headers = {}
        headers['User-Agent'] = HTTPClient.USER_AGENT
        data = {}
        data.update(params)
        data['key'] = self._HTTPClient__key
        data['signature'] = signature
        data['nonce'] = nonce
        return (
         data, headers)

    def _post(self, url, params):
        common.logger.debug('POST to %s with params %s' % (url, str(params)))
        with self._HTTPClient__lock:
            data, headers = self._buildQuery(params)
            response = requests.post(url, headers=headers, data=data, timeout=(HTTPClient.REQUEST_TIMEOUT))
            response.raise_for_status()
        jsonResponse = response.json()
        if isinstance(jsonResponse, dict):
            error = jsonResponse.get('error')
            if error is not None:
                raise Exception(error)
        return jsonResponse

    def getAccountBalance(self):
        url = 'https://www.bitstamp.net/api/balance/'
        jsonResponse = self._post(url, {})
        return AccountBalance(jsonResponse)

    def getOpenOrders(self):
        url = 'https://www.bitstamp.net/api/open_orders/'
        jsonResponse = self._post(url, {})
        return [Order(json_open_order) for json_open_order in jsonResponse]

    def cancelOrder(self, orderId):
        url = 'https://www.bitstamp.net/api/cancel_order/'
        params = {'id': orderId}
        jsonResponse = self._post(url, params)
        if jsonResponse != True:
            raise Exception('Failed to cancel order')

    def buyLimit(self, limitPrice, quantity):
        url = 'https://www.bitstamp.net/api/buy/'
        price = round(limitPrice, 2)
        amount = round(quantity, 8)
        params = {'price':price, 
         'amount':amount}
        jsonResponse = self._post(url, params)
        return Order(jsonResponse)

    def sellLimit(self, limitPrice, quantity):
        url = 'https://www.bitstamp.net/api/sell/'
        price = round(limitPrice, 2)
        amount = round(quantity, 8)
        params = {'price':price, 
         'amount':amount}
        jsonResponse = self._post(url, params)
        return Order(jsonResponse)

    def getUserTransactions(self, transactionType=None):
        url = 'https://www.bitstamp.net/api/user_transactions/'
        jsonResponse = self._post(url, {})
        if transactionType is not None:
            jsonUserTransactions = filter(lambda jsonUserTransaction: jsonUserTransaction['type'] == transactionType, jsonResponse)
        else:
            jsonUserTransactions = jsonResponse
        return [UserTransaction(jsonUserTransaction) for jsonUserTransaction in jsonUserTransactions]