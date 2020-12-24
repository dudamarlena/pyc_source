# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/bitstamp/httpclient.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
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


class AccountBalance(object):

    def __init__(self, jsonDict):
        self.__jsonDict = jsonDict

    def getDict(self):
        return self.__jsonDict

    def getUSDAvailable(self):
        return float(self.__jsonDict['usd_available'])

    def getBTCAvailable(self):
        return float(self.__jsonDict['btc_available'])


class Order(object):

    def __init__(self, jsonDict):
        self.__jsonDict = jsonDict

    def getDict(self):
        return self.__jsonDict

    def getId(self):
        return int(self.__jsonDict['id'])

    def isBuy(self):
        return self.__jsonDict['type'] == 0

    def isSell(self):
        return self.__jsonDict['type'] == 1

    def getPrice(self):
        return float(self.__jsonDict['price'])

    def getAmount(self):
        return float(self.__jsonDict['amount'])

    def getDateTime(self):
        return parse_datetime(self.__jsonDict['datetime'])


class UserTransaction(object):

    def __init__(self, jsonDict):
        self.__jsonDict = jsonDict

    def getDict(self):
        return self.__jsonDict

    def getBTC(self):
        return float(self.__jsonDict['btc'])

    def getBTCUSD(self):
        return float(self.__jsonDict['btc_usd'])

    def getDateTime(self):
        return parse_datetime(self.__jsonDict['datetime'])

    def getFee(self):
        return float(self.__jsonDict['fee'])

    def getId(self):
        return int(self.__jsonDict['id'])

    def getOrderId(self):
        return int(self.__jsonDict['order_id'])

    def getUSD(self):
        return float(self.__jsonDict['usd'])


class HTTPClient(object):
    USER_AGENT = 'PyAlgoTrade'
    REQUEST_TIMEOUT = 30

    class UserTransactionType:
        MARKET_TRADE = 2

    def __init__(self, clientId, key, secret):
        self.__clientId = clientId
        self.__key = key
        self.__secret = secret
        self.__prevNonce = None
        self.__lock = threading.Lock()
        return

    def _getNonce(self):
        ret = int(time.time())
        if ret == self.__prevNonce:
            ret += 1
        self.__prevNonce = ret
        return ret

    def _buildQuery(self, params):
        nonce = self._getNonce()
        message = '%d%s%s' % (nonce, self.__clientId, self.__key)
        signature = hmac.new(self.__secret, msg=message, digestmod=hashlib.sha256).hexdigest().upper()
        headers = {}
        headers['User-Agent'] = HTTPClient.USER_AGENT
        data = {}
        data.update(params)
        data['key'] = self.__key
        data['signature'] = signature
        data['nonce'] = nonce
        return (
         data, headers)

    def _post(self, url, params):
        common.logger.debug('POST to %s with params %s' % (url, str(params)))
        with self.__lock:
            data, headers = self._buildQuery(params)
            response = requests.post(url, headers=headers, data=data, timeout=HTTPClient.REQUEST_TIMEOUT)
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
        return [ Order(json_open_order) for json_open_order in jsonResponse ]

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
        params = {'price': price, 
           'amount': amount}
        jsonResponse = self._post(url, params)
        return Order(jsonResponse)

    def sellLimit(self, limitPrice, quantity):
        url = 'https://www.bitstamp.net/api/sell/'
        price = round(limitPrice, 2)
        amount = round(quantity, 8)
        params = {'price': price, 
           'amount': amount}
        jsonResponse = self._post(url, params)
        return Order(jsonResponse)

    def getUserTransactions(self, transactionType=None):
        url = 'https://www.bitstamp.net/api/user_transactions/'
        jsonResponse = self._post(url, {})
        if transactionType is not None:
            jsonUserTransactions = filter(lambda jsonUserTransaction: jsonUserTransaction['type'] == transactionType, jsonResponse)
        else:
            jsonUserTransactions = jsonResponse
        return [ UserTransaction(jsonUserTransaction) for jsonUserTransaction in jsonUserTransactions ]