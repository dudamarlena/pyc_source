# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/bitstamp/wsclient.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
import datetime, threading, Queue
from pyalgotrade.websocket import pusher
from pyalgotrade.bitstamp import common

def get_current_datetime():
    return datetime.datetime.now()


class Trade(pusher.Event):
    """A trade event."""

    def __init__(self, dateTime, eventDict):
        super(Trade, self).__init__(eventDict, True)
        self.__dateTime = dateTime

    def getDateTime(self):
        """Returns the :class:`datetime.datetime` when this event was received."""
        return self.__dateTime

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
    """An order book update event."""

    def __init__(self, dateTime, eventDict):
        super(OrderBookUpdate, self).__init__(eventDict, True)
        self.__dateTime = dateTime

    def getDateTime(self):
        """Returns the :class:`datetime.datetime` when this event was received."""
        return self.__dateTime

    def getBidPrices(self):
        """Returns a list with the top 20 bid prices."""
        return [ float(bid[0]) for bid in self.getData()['bids'] ]

    def getBidVolumes(self):
        """Returns a list with the top 20 bid volumes."""
        return [ float(bid[1]) for bid in self.getData()['bids'] ]

    def getAskPrices(self):
        """Returns a list with the top 20 ask prices."""
        return [ float(ask[0]) for ask in self.getData()['asks'] ]

    def getAskVolumes(self):
        """Returns a list with the top 20 ask volumes."""
        return [ float(ask[1]) for ask in self.getData()['asks'] ]


class WebSocketClient(pusher.WebSocketClient):
    PUSHER_APP_KEY = 'de504dc5763aeef9ff52'
    ON_TRADE = 1
    ON_ORDER_BOOK_UPDATE = 2
    ON_CONNECTED = 3
    ON_DISCONNECTED = 4

    def __init__(self):
        super(WebSocketClient, self).__init__(WebSocketClient.PUSHER_APP_KEY, 5)
        self.__queue = Queue.Queue()

    def getQueue(self):
        return self.__queue

    def onMessage(self, msg):
        event = msg.get('event')
        if event == 'trade':
            self.onTrade(Trade(get_current_datetime(), msg))
        elif event == 'data' and msg.get('channel') == 'order_book':
            self.onOrderBookUpdate(OrderBookUpdate(get_current_datetime(), msg))
        else:
            super(WebSocketClient, self).onMessage(msg)

    def onOpened(self):
        pass

    def onClosed(self, code, reason):
        common.logger.info('Closed. Code: %s. Reason: %s.' % (code, reason))
        self.__queue.put((WebSocketClient.ON_DISCONNECTED, None))
        return

    def onDisconnectionDetected(self):
        common.logger.warning('Disconnection detected.')
        try:
            self.stopClient()
        except Exception as e:
            common.logger.error('Error stopping websocket client: %s.' % str(e))

        self.__queue.put((WebSocketClient.ON_DISCONNECTED, None))
        return

    def onConnectionEstablished(self, event):
        common.logger.info('Connection established.')
        self.subscribeChannel('live_trades')
        self.subscribeChannel('order_book')
        self.__queue.put((WebSocketClient.ON_CONNECTED, None))
        return

    def onError(self, event):
        common.logger.error('Error: %s' % event)

    def onUnknownEvent(self, event):
        common.logger.warning('Unknown event: %s' % event)

    def onTrade(self, trade):
        self.__queue.put((WebSocketClient.ON_TRADE, trade))

    def onOrderBookUpdate(self, orderBookUpdate):
        self.__queue.put((WebSocketClient.ON_ORDER_BOOK_UPDATE, orderBookUpdate))


class WebSocketClientThread(threading.Thread):

    def __init__(self):
        super(WebSocketClientThread, self).__init__()
        self.__wsClient = WebSocketClient()

    def getQueue(self):
        return self.__wsClient.getQueue()

    def start(self):
        self.__wsClient.connect()
        super(WebSocketClientThread, self).start()

    def run(self):
        self.__wsClient.startClient()

    def stop(self):
        try:
            common.logger.info('Stopping websocket client.')
            self.__wsClient.stopClient()
        except Exception as e:
            common.logger.error('Error stopping websocket client: %s.' % str(e))