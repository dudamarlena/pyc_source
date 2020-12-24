# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\bitstamp\wsclient.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 6497 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import datetime
from six.moves import queue
from pyalgotrade.websocket import pusher
from pyalgotrade.websocket import client
from pyalgotrade.bitstamp import common

def get_current_datetime():
    return datetime.datetime.now()


class Trade(pusher.Event):
    __doc__ = 'A trade event.'

    def __init__(self, dateTime, eventDict):
        super(Trade, self).__init__(eventDict, True)
        self._Trade__dateTime = dateTime

    def getDateTime(self):
        """Returns the :class:`datetime.datetime` when this event was received."""
        return self._Trade__dateTime

    def getId(self):
        """Returns the trade id."""
        return self.getData()['id']

    def getPrice(self):
        """Returns the trade price."""
        return self.getData()['price']

    def getAmount(self):
        """Returns the trade amount."""
        return self.getData()['amount']

    def isBuy(self):
        """Returns True if the trade was a buy."""
        return self.getData()['type'] == 0

    def isSell(self):
        """Returns True if the trade was a sell."""
        return self.getData()['type'] == 1


class OrderBookUpdate(pusher.Event):
    __doc__ = 'An order book update event.'

    def __init__(self, dateTime, eventDict):
        super(OrderBookUpdate, self).__init__(eventDict, True)
        self._OrderBookUpdate__dateTime = dateTime

    def getDateTime(self):
        """Returns the :class:`datetime.datetime` when this event was received."""
        return self._OrderBookUpdate__dateTime

    def getBidPrices(self):
        """Returns a list with the top 20 bid prices."""
        return [float(bid[0]) for bid in self.getData()['bids']]

    def getBidVolumes(self):
        """Returns a list with the top 20 bid volumes."""
        return [float(bid[1]) for bid in self.getData()['bids']]

    def getAskPrices(self):
        """Returns a list with the top 20 ask prices."""
        return [float(ask[0]) for ask in self.getData()['asks']]

    def getAskVolumes(self):
        """Returns a list with the top 20 ask volumes."""
        return [float(ask[1]) for ask in self.getData()['asks']]


class WebSocketClient(pusher.WebSocketClient):
    __doc__ = '\n    This websocket client class is designed to be running in a separate thread and for that reason\n    events are pushed into a queue.\n    '
    PUSHER_APP_KEY = 'de504dc5763aeef9ff52'

    class Event:
        TRADE = 1
        ORDER_BOOK_UPDATE = 2
        CONNECTED = 3
        DISCONNECTED = 4

    def __init__(self, queue):
        super(WebSocketClient, self).__init__(WebSocketClient.PUSHER_APP_KEY, 5)
        self._WebSocketClient__queue = queue

    def onMessage(self, msg):
        event = msg.get('event')
        if event == 'trade':
            self.onTrade(Trade(get_current_datetime(), msg))
        else:
            if event == 'data' and msg.get('channel') == 'order_book':
                self.onOrderBookUpdate(OrderBookUpdate(get_current_datetime(), msg))
            else:
                super(WebSocketClient, self).onMessage(msg)

    def onClosed(self, code, reason):
        common.logger.info('Closed. Code: %s. Reason: %s.' % (code, reason))
        self._WebSocketClient__queue.put((WebSocketClient.Event.DISCONNECTED, None))

    def onDisconnectionDetected(self):
        common.logger.warning('Disconnection detected.')
        try:
            self.stopClient()
        except Exception as e:
            try:
                common.logger.error('Error stopping websocket client: %s.' % str(e))
            finally:
                e = None
                del e

        self._WebSocketClient__queue.put((WebSocketClient.Event.DISCONNECTED, None))

    def onConnectionEstablished(self, event):
        common.logger.info('Connection established.')
        self._WebSocketClient__queue.put((WebSocketClient.Event.CONNECTED, None))
        channels = [
         'live_trades', 'order_book']
        common.logger.info('Subscribing to channels %s.' % channels)
        for channel in channels:
            self.subscribeChannel(channel)

    def onError(self, event):
        common.logger.error('Error: %s' % event)

    def onUnknownEvent(self, event):
        common.logger.warning('Unknown event: %s' % event)

    def onTrade(self, trade):
        self._WebSocketClient__queue.put((WebSocketClient.Event.TRADE, trade))

    def onOrderBookUpdate(self, orderBookUpdate):
        self._WebSocketClient__queue.put((WebSocketClient.Event.ORDER_BOOK_UPDATE, orderBookUpdate))


class WebSocketClientThread(client.WebSocketClientThreadBase):
    __doc__ = '\n    This thread class is responsible for running a WebSocketClient.\n    '

    def __init__(self):
        super(WebSocketClientThread, self).__init__()
        self._WebSocketClientThread__queue = queue.Queue()
        self._WebSocketClientThread__wsClient = None

    def getQueue(self):
        return self._WebSocketClientThread__queue

    def run(self):
        super(WebSocketClientThread, self).run()
        try:
            self._WebSocketClientThread__wsClient = WebSocketClient(self._WebSocketClientThread__queue)
            self._WebSocketClientThread__wsClient.connect()
            self._WebSocketClientThread__wsClient.startClient()
        except Exception:
            common.logger.exception('Failed to connect: %s')

    def stop(self):
        try:
            if self._WebSocketClientThread__wsClient is not None:
                common.logger.info('Stopping websocket client.')
                self._WebSocketClientThread__wsClient.stopClient()
        except Exception as e:
            try:
                common.logger.error('Error stopping websocket client: %s.' % str(e))
            finally:
                e = None
                del e