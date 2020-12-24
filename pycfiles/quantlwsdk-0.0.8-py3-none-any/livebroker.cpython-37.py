# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\bitstamp\livebroker.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 12032 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import threading, time
from six.moves import queue
from pyalgotrade import broker
from pyalgotrade.bitstamp import httpclient
from pyalgotrade.bitstamp import common

def build_order_from_open_order(openOrder, instrumentTraits):
    if openOrder.isBuy():
        action = broker.Order.Action.BUY
    else:
        if openOrder.isSell():
            action = broker.Order.Action.SELL
        else:
            raise Exception('Invalid order type')
    ret = broker.LimitOrder(action, common.btc_symbol, openOrder.getPrice(), openOrder.getAmount(), instrumentTraits)
    ret.setSubmitted(openOrder.getId(), openOrder.getDateTime())
    ret.setState(broker.Order.State.ACCEPTED)
    return ret


class TradeMonitor(threading.Thread):
    POLL_FREQUENCY = 2
    ON_USER_TRADE = 1

    def __init__(self, httpClient):
        super(TradeMonitor, self).__init__()
        self._TradeMonitor__lastTradeId = -1
        self._TradeMonitor__httpClient = httpClient
        self._TradeMonitor__queue = queue.Queue()
        self._TradeMonitor__stop = False

    def _getNewTrades(self):
        userTrades = self._TradeMonitor__httpClient.getUserTransactions(httpclient.HTTPClient.UserTransactionType.MARKET_TRADE)
        ret = [t for t in userTrades if t.getId() > self._TradeMonitor__lastTradeId]
        return sorted(ret, key=(lambda t: t.getId()))

    def getQueue(self):
        return self._TradeMonitor__queue

    def start(self):
        trades = self._getNewTrades()
        if len(trades):
            self._TradeMonitor__lastTradeId = trades[(-1)].getId()
            common.logger.info('Last trade found: %d' % self._TradeMonitor__lastTradeId)
        super(TradeMonitor, self).start()

    def run(self):
        while not self._TradeMonitor__stop:
            try:
                trades = self._getNewTrades()
                if len(trades):
                    self._TradeMonitor__lastTradeId = trades[(-1)].getId()
                    common.logger.info('%d new trade/s found' % len(trades))
                    self._TradeMonitor__queue.put((TradeMonitor.ON_USER_TRADE, trades))
            except Exception as e:
                try:
                    common.logger.critical('Error retrieving user transactions', exc_info=e)
                finally:
                    e = None
                    del e

            time.sleep(TradeMonitor.POLL_FREQUENCY)

    def stop(self):
        self._TradeMonitor__stop = True


class LiveBroker(broker.Broker):
    __doc__ = 'A Bitstamp live broker.\n\n    :param clientId: Client id.\n    :type clientId: string.\n    :param key: API key.\n    :type key: string.\n    :param secret: API secret.\n    :type secret: string.\n\n\n    .. note::\n        * Only limit orders are supported.\n        * Orders are automatically set as **goodTillCanceled=True** and  **allOrNone=False**.\n        * BUY_TO_COVER orders are mapped to BUY orders.\n        * SELL_SHORT orders are mapped to SELL orders.\n        * API access permissions should include:\n\n          * Account balance\n          * Open orders\n          * Buy limit order\n          * User transactions\n          * Cancel order\n          * Sell limit order\n    '
    QUEUE_TIMEOUT = 0.01

    def __init__(self, clientId, key, secret):
        super(LiveBroker, self).__init__()
        self._LiveBroker__stop = False
        self._LiveBroker__httpClient = self.buildHTTPClient(clientId, key, secret)
        self._LiveBroker__tradeMonitor = TradeMonitor(self._LiveBroker__httpClient)
        self._LiveBroker__cash = 0
        self._LiveBroker__shares = {}
        self._LiveBroker__activeOrders = {}

    def _registerOrder(self, order):
        assert order.getId() not in self._LiveBroker__activeOrders
        assert order.getId() is not None
        self._LiveBroker__activeOrders[order.getId()] = order

    def _unregisterOrder(self, order):
        assert order.getId() in self._LiveBroker__activeOrders
        assert order.getId() is not None
        del self._LiveBroker__activeOrders[order.getId()]

    def buildHTTPClient(self, clientId, key, secret):
        return httpclient.HTTPClient(clientId, key, secret)

    def refreshAccountBalance(self):
        """Refreshes cash and BTC balance."""
        self._LiveBroker__stop = True
        common.logger.info('Retrieving account balance.')
        balance = self._LiveBroker__httpClient.getAccountBalance()
        self._LiveBroker__cash = round(balance.getUSDAvailable(), 2)
        common.logger.info('%s USD' % self._LiveBroker__cash)
        btc = balance.getBTCAvailable()
        if btc:
            self._LiveBroker__shares = {common.btc_symbol: btc}
        else:
            self._LiveBroker__shares = {}
        common.logger.info('%s BTC' % btc)
        self._LiveBroker__stop = False

    def refreshOpenOrders(self):
        self._LiveBroker__stop = True
        common.logger.info('Retrieving open orders.')
        openOrders = self._LiveBroker__httpClient.getOpenOrders()
        for openOrder in openOrders:
            self._registerOrder(build_order_from_open_order(openOrder, self.getInstrumentTraits(common.btc_symbol)))

        common.logger.info('%d open order/s found' % len(openOrders))
        self._LiveBroker__stop = False

    def _startTradeMonitor(self):
        self._LiveBroker__stop = True
        common.logger.info('Initializing trade monitor.')
        self._LiveBroker__tradeMonitor.start()
        self._LiveBroker__stop = False

    def _onUserTrades(self, trades):
        for trade in trades:
            order = self._LiveBroker__activeOrders.get(trade.getOrderId())
            if order is not None:
                fee = trade.getFee()
                fillPrice = trade.getBTCUSD()
                btcAmount = trade.getBTC()
                dateTime = trade.getDateTime()
                self.refreshAccountBalance()
                orderExecutionInfo = broker.OrderExecutionInfo(fillPrice, abs(btcAmount), fee, dateTime)
                order.addExecutionInfo(orderExecutionInfo)
                if not order.isActive():
                    self._unregisterOrder(order)
                elif order.isFilled():
                    eventType = broker.OrderEvent.Type.FILLED
                else:
                    eventType = broker.OrderEvent.Type.PARTIALLY_FILLED
                self.notifyOrderEvent(broker.OrderEvent(order, eventType, orderExecutionInfo))
            else:
                common.logger.info('Trade %d refered to order %d that is not active' % (trade.getId(), trade.getOrderId()))

    def start(self):
        super(LiveBroker, self).start()
        self.refreshAccountBalance()
        self.refreshOpenOrders()
        self._startTradeMonitor()

    def stop(self):
        self._LiveBroker__stop = True
        common.logger.info('Shutting down trade monitor.')
        self._LiveBroker__tradeMonitor.stop()

    def join(self):
        if self._LiveBroker__tradeMonitor.isAlive():
            self._LiveBroker__tradeMonitor.join()

    def eof(self):
        return self._LiveBroker__stop

    def dispatch(self):
        ordersToProcess = list(self._LiveBroker__activeOrders.values())
        for order in ordersToProcess:
            if order.isSubmitted():
                order.switchState(broker.Order.State.ACCEPTED)
                self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.ACCEPTED, None))

        try:
            eventType, eventData = self._LiveBroker__tradeMonitor.getQueue().get(True, LiveBroker.QUEUE_TIMEOUT)
            if eventType == TradeMonitor.ON_USER_TRADE:
                self._onUserTrades(eventData)
            else:
                common.logger.error('Invalid event received to dispatch: %s - %s' % (eventType, eventData))
        except queue.Empty:
            pass

    def peekDateTime(self):
        pass

    def getCash(self, includeShort=True):
        return self._LiveBroker__cash

    def getInstrumentTraits(self, instrument):
        return common.BTCTraits()

    def getShares(self, instrument):
        return self._LiveBroker__shares.get(instrument, 0)

    def getPositions(self):
        return self._LiveBroker__shares

    def getActiveOrders(self, instrument=None):
        return list(self._LiveBroker__activeOrders.values())

    def submitOrder(self, order):
        if order.isInitial():
            order.setAllOrNone(False)
            order.setGoodTillCanceled(True)
            if order.isBuy():
                bitstampOrder = self._LiveBroker__httpClient.buyLimit(order.getLimitPrice(), order.getQuantity())
            else:
                bitstampOrder = self._LiveBroker__httpClient.sellLimit(order.getLimitPrice(), order.getQuantity())
            order.setSubmitted(bitstampOrder.getId(), bitstampOrder.getDateTime())
            self._registerOrder(order)
            order.switchState(broker.Order.State.SUBMITTED)
        else:
            raise Exception('The order was already processed')

    def createMarketOrder(self, action, instrument, quantity, onClose=False):
        raise Exception('Market orders are not supported')

    def createLimitOrder(self, action, instrument, limitPrice, quantity):
        if instrument != common.btc_symbol:
            raise Exception('Only BTC instrument is supported')
        elif action == broker.Order.Action.BUY_TO_COVER:
            action = broker.Order.Action.BUY
        else:
            if action == broker.Order.Action.SELL_SHORT:
                action = broker.Order.Action.SELL
        if action not in [broker.Order.Action.BUY, broker.Order.Action.SELL]:
            raise Exception('Only BUY/SELL orders are supported')
        instrumentTraits = self.getInstrumentTraits(instrument)
        limitPrice = round(limitPrice, 2)
        quantity = instrumentTraits.roundQuantity(quantity)
        return broker.LimitOrder(action, instrument, limitPrice, quantity, instrumentTraits)

    def createStopOrder(self, action, instrument, stopPrice, quantity):
        raise Exception('Stop orders are not supported')

    def createStopLimitOrder(self, action, instrument, stopPrice, limitPrice, quantity):
        raise Exception('Stop limit orders are not supported')

    def cancelOrder(self, order):
        activeOrder = self._LiveBroker__activeOrders.get(order.getId())
        if activeOrder is None:
            raise Exception('The order is not active anymore')
        if activeOrder.isFilled():
            raise Exception("Can't cancel order that has already been filled")
        self._LiveBroker__httpClient.cancelOrder(order.getId())
        self._unregisterOrder(order)
        order.switchState(broker.Order.State.CANCELED)
        self.refreshAccountBalance()
        self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.CANCELED, 'User requested cancellation'))