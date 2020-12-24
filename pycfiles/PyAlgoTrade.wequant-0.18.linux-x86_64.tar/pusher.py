# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/websocket/pusher.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import json, urllib, pyalgotrade
from pyalgotrade.websocket import client
import pyalgotrade.logger
logger = pyalgotrade.logger.getLogger('pusher')

class Event(object):

    def __init__(self, eventDict, dataIsJSON):
        self.__eventDict = eventDict
        self.__data = eventDict.get('data')
        if self.__data is not None and dataIsJSON:
            self.__data = json.loads(self.__data)
        return

    def __str__(self):
        return str(self.__eventDict)

    def getDict(self):
        return self.__eventDict

    def getData(self):
        return self.__data

    def getType(self):
        return self.__eventDict.get('event')


class PingKeepAliveMgr(client.KeepAliveMgr):

    def __init__(self, wsClient, maxInactivity, responseTimeout):
        super(PingKeepAliveMgr, self).__init__(wsClient, maxInactivity, responseTimeout)

    def sendKeepAlive(self):
        logger.debug('Sending pusher:ping.')
        self.getWSClient().sendPing()

    def handleResponse(self, msg):
        ret = msg.get('event') == 'pusher:pong'
        if ret:
            logger.debug('Received pusher:pong.')
        return ret


class WebSocketClient(client.WebSocketClientBase):

    def __init__(self, appKey, protocol=5, maxInactivity=120, responseTimeout=30):
        params = {'protocol': protocol, 
           'client': 'Python-PyAlgoTrade', 
           'version': pyalgotrade.__version__}
        url = 'ws://ws.pusherapp.com/app/%s?%s' % (appKey, urllib.urlencode(params))
        super(WebSocketClient, self).__init__(url)
        self.setKeepAliveMgr(PingKeepAliveMgr(self, maxInactivity, responseTimeout))

    def sendEvent(self, eventType, eventData):
        msgDict = {'event': eventType}
        if eventData:
            msgDict['data'] = eventData
        msg = json.dumps(msgDict)
        self.send(msg, False)

    def subscribeChannel(self, channel):
        self.sendEvent('pusher:subscribe', {'channel': channel})

    def sendPing(self):
        self.sendEvent('pusher:ping', None)
        return

    def sendPong(self):
        self.sendEvent('pusher:pong', None)
        return

    def onMessage(self, msg):
        eventType = msg.get('event')
        if eventType == 'pusher:error':
            self.onError(Event(msg, False))
        elif eventType == 'pusher:ping':
            self.sendPong()
        elif eventType == 'pusher:connection_established':
            self.onConnectionEstablished(Event(msg, True))
        elif eventType == 'pusher_internal:subscription_succeeded':
            self.onSubscriptionSucceeded(Event(msg, True))
        else:
            self.onUnknownEvent(Event(msg, False))

    def onConnectionEstablished(self, event):
        pass

    def onSubscriptionSucceeded(self, event):
        pass

    def onError(self, event):
        raise NotImplementedError()

    def onUnknownEvent(self, event):
        raise NotImplementedError()