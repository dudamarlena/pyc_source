# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\bitstamp\livefeed.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 8589 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import datetime, time
from six.moves import queue
from pyalgotrade import bar
from pyalgotrade import barfeed
from pyalgotrade import observer
from pyalgotrade.bitstamp import common
from pyalgotrade.bitstamp import wsclient

class TradeBar(bar.Bar):
    __slots__ = ('__dateTime', '__tradeId', '__price', '__amount')

    def __init__(self, dateTime, trade):
        self._TradeBar__dateTime = dateTime
        self._TradeBar__tradeId = trade.getId()
        self._TradeBar__price = trade.getPrice()
        self._TradeBar__amount = trade.getAmount()
        self._TradeBar__buy = trade.isBuy()

    def __setstate__(self, state):
        self._TradeBar__dateTime, self._TradeBar__tradeId, self._TradeBar__price, self._TradeBar__amount = state

    def __getstate__(self):
        return (
         self._TradeBar__dateTime, self._TradeBar__tradeId, self._TradeBar__price, self._TradeBar__amount)

    def setUseAdjustedValue(self, useAdjusted):
        if useAdjusted:
            raise Exception('Adjusted close is not available')

    def getTradeId(self):
        return self._TradeBar__tradeId

    def getFrequency(self):
        return bar.Frequency.TRADE

    def getDateTime(self):
        return self._TradeBar__dateTime

    def getOpen(self, adjusted=False):
        return self._TradeBar__price

    def getHigh(self, adjusted=False):
        return self._TradeBar__price

    def getLow(self, adjusted=False):
        return self._TradeBar__price

    def getClose(self, adjusted=False):
        return self._TradeBar__price

    def getVolume(self):
        return self._TradeBar__amount

    def getAdjClose(self):
        pass

    def getTypicalPrice(self):
        return self._TradeBar__price

    def getPrice(self):
        return self._TradeBar__price

    def getUseAdjValue(self):
        return False

    def isBuy(self):
        return self._TradeBar__buy

    def isSell(self):
        return not self._TradeBar__buy


class LiveTradeFeed(barfeed.BaseBarFeed):
    __doc__ = 'A real-time BarFeed that builds bars from live trades.\n\n    :param maxLen: The maximum number of values that the :class:`pyalgotrade.dataseries.bards.BarDataSeries` will hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded\n        from the opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n\n    .. note::\n        Note that a Bar will be created for every trade, so open, high, low and close values will all be the same.\n    '
    QUEUE_TIMEOUT = 0.01

    def __init__(self, maxLen=None):
        super(LiveTradeFeed, self).__init__(bar.Frequency.TRADE, maxLen)
        self._LiveTradeFeed__barDicts = []
        self.registerInstrument(common.btc_symbol)
        self._LiveTradeFeed__prevTradeDateTime = None
        self._LiveTradeFeed__thread = None
        self._LiveTradeFeed__wsClientConnected = False
        self._LiveTradeFeed__enableReconnection = True
        self._LiveTradeFeed__stopped = False
        self._LiveTradeFeed__orderBookUpdateEvent = observer.Event()

    def buildWebSocketClientThread(self):
        return wsclient.WebSocketClientThread()

    def getCurrentDateTime(self):
        return wsclient.get_current_datetime()

    def enableReconection(self, enableReconnection):
        self._LiveTradeFeed__enableReconnection = enableReconnection

    def __initializeClient(self):
        common.logger.info('Initializing websocket client.')
        if not self._LiveTradeFeed__wsClientConnected is False:
            raise AssertionError('Websocket client already connected')
        else:
            try:
                self._LiveTradeFeed__thread = self.buildWebSocketClientThread()
                self._LiveTradeFeed__thread.start()
            except Exception as e:
                try:
                    common.logger.exception('Error connecting : %s' % str(e))
                finally:
                    e = None
                    del e

            while not self._LiveTradeFeed__wsClientConnected:
                if self._LiveTradeFeed__thread.is_alive():
                    self._LiveTradeFeed__dispatchImpl([wsclient.WebSocketClient.Event.CONNECTED])

            if self._LiveTradeFeed__wsClientConnected:
                common.logger.info('Initialization ok.')
            else:
                common.logger.error('Initialization failed.')
        return self._LiveTradeFeed__wsClientConnected

    def __onConnected(self):
        self._LiveTradeFeed__wsClientConnected = True

    def __onDisconnected(self):
        self._LiveTradeFeed__wsClientConnected = False
        if self._LiveTradeFeed__enableReconnection:
            initialized = False
            while not self._LiveTradeFeed__stopped:
                if not initialized:
                    common.logger.info('Reconnecting')
                    initialized = self._LiveTradeFeed__initializeClient()
                    initialized or time.sleep(5)

        else:
            self._LiveTradeFeed__stopped = True

    def __dispatchImpl(self, eventFilter):
        ret = False
        try:
            eventType, eventData = self._LiveTradeFeed__thread.getQueue().get(True, LiveTradeFeed.QUEUE_TIMEOUT)
            if eventFilter is not None:
                if eventType not in eventFilter:
                    return False
            else:
                ret = True
                if eventType == wsclient.WebSocketClient.Event.TRADE:
                    self._LiveTradeFeed__onTrade(eventData)
                else:
                    if eventType == wsclient.WebSocketClient.Event.ORDER_BOOK_UPDATE:
                        self._LiveTradeFeed__orderBookUpdateEvent.emit(eventData)
                    else:
                        if eventType == wsclient.WebSocketClient.Event.CONNECTED:
                            self._LiveTradeFeed__onConnected()
                        else:
                            if eventType == wsclient.WebSocketClient.Event.DISCONNECTED:
                                self._LiveTradeFeed__onDisconnected()
                            else:
                                ret = False
                                common.logger.error('Invalid event received to dispatch: %s - %s' % (eventType, eventData))
        except queue.Empty:
            pass

        return ret

    def __getTradeDateTime(self, trade):
        ret = trade.getDateTime()
        if ret == self._LiveTradeFeed__prevTradeDateTime:
            ret += datetime.timedelta(microseconds=1)
        self._LiveTradeFeed__prevTradeDateTime = ret
        return ret

    def __onTrade(self, trade):
        barDict = {common.btc_symbol: TradeBar(self._LiveTradeFeed__getTradeDateTime(trade), trade)}
        self._LiveTradeFeed__barDicts.append(barDict)

    def barsHaveAdjClose(self):
        return False

    def getNextBars(self):
        ret = None
        if len(self._LiveTradeFeed__barDicts):
            ret = bar.Bars(self._LiveTradeFeed__barDicts.pop(0))
        return ret

    def peekDateTime(self):
        pass

    def start(self):
        super(LiveTradeFeed, self).start()
        if self._LiveTradeFeed__thread is not None:
            raise Exception('Already running')
        else:
            if not self._LiveTradeFeed__initializeClient():
                self._LiveTradeFeed__stopped = True
                raise Exception('Initialization failed')

    def dispatch(self):
        ret = False
        if self._LiveTradeFeed__dispatchImpl(None):
            ret = True
        if super(LiveTradeFeed, self).dispatch():
            ret = True
        return ret

    def stop(self):
        try:
            self._LiveTradeFeed__stopped = True
            if self._LiveTradeFeed__thread is not None:
                if self._LiveTradeFeed__thread.is_alive():
                    common.logger.info('Shutting down websocket client.')
                    self._LiveTradeFeed__thread.stop()
        except Exception as e:
            try:
                common.logger.error('Error shutting down client: %s' % str(e))
            finally:
                e = None
                del e

    def join(self):
        if self._LiveTradeFeed__thread is not None:
            self._LiveTradeFeed__thread.join()

    def eof(self):
        return self._LiveTradeFeed__stopped

    def getOrderBookUpdateEvent(self):
        """
        Returns the event that will be emitted when the orderbook gets updated.

        Eventh handlers should receive one parameter:
         1. A :class:`pyalgotrade.bitstamp.wsclient.OrderBookUpdate` instance.

        :rtype: :class:`pyalgotrade.observer.Event`.
        """
        return self._LiveTradeFeed__orderBookUpdateEvent