# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/bitstamp/livebroker.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import threading, time, Queue
from pyalgotrade import broker
from pyalgotrade.bitstamp import httpclient
from pyalgotrade.bitstamp import common

def build_order_from_open_order(openOrder, instrumentTraits):
    if openOrder.isBuy():
        action = broker.Order.Action.BUY
    elif openOrder.isSell():
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
        self.__lastTradeId = -1
        self.__httpClient = httpClient
        self.__queue = Queue.Queue()
        self.__stop = False

    def _getNewTrades(self):
        userTrades = self.__httpClient.getUserTransactions(httpclient.HTTPClient.UserTransactionType.MARKET_TRADE)
        ret = []
        for userTrade in userTrades:
            if userTrade.getId() > self.__lastTradeId:
                ret.append(userTrade)
            else:
                break

        ret.reverse()
        return ret

    def getQueue(self):
        return self.__queue

    def start(self):
        trades = self._getNewTrades()
        if len(trades):
            self.__lastTradeId = trades[(-1)].getId()
            common.logger.info('Last trade found: %d' % self.__lastTradeId)
        super(TradeMonitor, self).start()

    def run(self):
        while not self.__stop:
            try:
                trades = self._getNewTrades()
                if len(trades):
                    self.__lastTradeId = trades[(-1)].getId()
                    common.logger.info('%d new trade/s found' % len(trades))
                    self.__queue.put((TradeMonitor.ON_USER_TRADE, trades))
            except Exception as e:
                common.logger.critical('Error retrieving user transactions', exc_info=e)

            time.sleep(TradeMonitor.POLL_FREQUENCY)

    def stop(self):
        self.__stop = True


class LiveBroker(broker.Broker):
    """A Bitstamp live broker.

    :param clientId: Client id.
    :type clientId: string.
    :param key: API key.
    :type key: string.
    :param secret: API secret.
    :type secret: string.

    .. note::
        * Only limit orders are supported.
        * Orders are automatically set as **goodTillCanceled=True** and  **allOrNone=False**.
        * BUY_TO_COVER orders are mapped to BUY orders.
        * SELL_SHORT orders are mapped to SELL orders.
        * API access permissions should include:

          * Account balance
          * Open orders
          * Buy limit order
          * User transactions
          * Cancel order
          * Sell limit order
    """
    QUEUE_TIMEOUT = 0.01

    def __init__(self, clientId, key, secret):
        super(LiveBroker, self).__init__()
        self.__stop = False
        self.__httpClient = self.buildHTTPClient(clientId, key, secret)
        self.__tradeMonitor = TradeMonitor(self.__httpClient)
        self.__cash = 0
        self.__shares = {}
        self.__activeOrders = {}

    def _registerOrder(self, order):
        assert order.getId() not in self.__activeOrders
        assert order.getId() is not None
        self.__activeOrders[order.getId()] = order
        return

    def _unregisterOrder(self, order):
        assert order.getId() in self.__activeOrders
        assert order.getId() is not None
        del self.__activeOrders[order.getId()]
        return

    def buildHTTPClient(self, clientId, key, secret):
        return httpclient.HTTPClient(clientId, key, secret)

    def refreshAccountBalance(self):
        """Refreshes cash and BTC balance."""
        self.__stop = True
        common.logger.info('Retrieving account balance.')
        balance = self.__httpClient.getAccountBalance()
        self.__cash = round(balance.getUSDAvailable(), 2)
        common.logger.info('%s USD' % self.__cash)
        btc = balance.getBTCAvailable()
        if btc:
            self.__shares = {common.btc_symbol: btc}
        else:
            self.__shares = {}
        common.logger.info('%s BTC' % btc)
        self.__stop = False

    def refreshOpenOrders(self):
        self.__stop = True
        common.logger.info('Retrieving open orders.')
        openOrders = self.__httpClient.getOpenOrders()
        for openOrder in openOrders:
            self._registerOrder(build_order_from_open_order(openOrder, self.getInstrumentTraits(common.btc_symbol)))

        common.logger.info('%d open order/s found' % len(openOrders))
        self.__stop = False

    def _startTradeMonitor(self):
        self.__stop = True
        common.logger.info('Initializing trade monitor.')
        self.__tradeMonitor.start()
        self.__stop = False

    def _onUserTrades(self, trades):
        for trade in trades:
            order = self.__activeOrders.get(trade.getOrderId())
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
                if order.isFilled():
                    eventType = broker.OrderEvent.Type.FILLED
                else:
                    eventType = broker.OrderEvent.Type.PARTIALLY_FILLED
                self.notifyOrderEvent(broker.OrderEvent(order, eventType, orderExecutionInfo))
            else:
                common.logger.info('Trade %d refered to order %d that is not active' % (trade.getId(), trade.getOrderId()))

        return

    def start(self):
        super(LiveBroker, self).start()
        self.refreshAccountBalance()
        self.refreshOpenOrders()
        self._startTradeMonitor()

    def stop(self):
        self.__stop = True
        common.logger.info('Shutting down trade monitor.')
        self.__tradeMonitor.stop()

    def join(self):
        if self.__tradeMonitor.isAlive():
            self.__tradeMonitor.join()

    def eof(self):
        return self.__stop

    def dispatch(self):
        ordersToProcess = self.__activeOrders.values()
        for order in ordersToProcess:
            if order.isSubmitted():
                order.switchState(broker.Order.State.ACCEPTED)
                self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.ACCEPTED, None))

        try:
            eventType, eventData = self.__tradeMonitor.getQueue().get(True, LiveBroker.QUEUE_TIMEOUT)
            if eventType == TradeMonitor.ON_USER_TRADE:
                self._onUserTrades(eventData)
            else:
                common.logger.error('Invalid event received to dispatch: %s - %s' % (eventType, eventData))
        except Queue.Empty:
            pass

        return

    def peekDateTime(self):
        return

    def getCash(self, includeShort=True):
        return self.__cash

    def getInstrumentTraits(self, instrument):
        return common.BTCTraits()

    def getShares(self, instrument):
        return self.__shares.get(instrument, 0)

    def getPositions(self):
        return self.__shares

    def getActiveOrders(self, instrument=None):
        return self.__activeOrders.values()

    def submitOrder(self, order):
        if order.isInitial():
            order.setAllOrNone(False)
            order.setGoodTillCanceled(True)
            if order.isBuy():
                bitstampOrder = self.__httpClient.buyLimit(order.getLimitPrice(), order.getQuantity())
            else:
                bitstampOrder = self.__httpClient.sellLimit(order.getLimitPrice(), order.getQuantity())
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
        if action == broker.Order.Action.BUY_TO_COVER:
            action = broker.Order.Action.BUY
        elif action == broker.Order.Action.SELL_SHORT:
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
        activeOrder = self.__activeOrders.get(order.getId())
        if activeOrder is None:
            raise Exception('The order is not active anymore')
        if activeOrder.isFilled():
            raise Exception("Can't cancel order that has already been filled")
        self.__httpClient.cancelOrder(order.getId())
        self._unregisterOrder(order)
        order.switchState(broker.Order.State.CANCELED)
        self.refreshAccountBalance()
        self.notifyOrderEvent(broker.OrderEvent(order, broker.OrderEvent.Type.CANCELED, 'User requested cancellation'))
        return