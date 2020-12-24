# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/websocket/client.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import json, time
from ws4py.client import tornadoclient
import tornado, pyalgotrade.logger
logger = pyalgotrade.logger.getLogger('websocket.client')

class KeepAliveMgr(object):

    def __init__(self, wsClient, maxInactivity, responseTimeout):
        assert maxInactivity > 0
        assert responseTimeout > 0
        self.__callback = None
        self.__wsClient = wsClient
        self.__activityTimeout = maxInactivity
        self.__responseTimeout = responseTimeout
        self.__lastSeen = None
        self.__kaSent = None
        return

    def _keepAlive(self):
        if self.__lastSeen is None:
            return
        else:
            inactivity = time.time() - self.__lastSeen
            if inactivity <= self.__activityTimeout:
                return
            try:
                if self.__kaSent is None:
                    self.sendKeepAlive()
                    self.__kaSent = time.time()
                elif time.time() - self.__kaSent > self.__responseTimeout:
                    self.__wsClient.onDisconnectionDetected()
            except Exception:
                self.__wsClient.onDisconnectionDetected()

            return

    def getWSClient(self):
        return self.__wsClient

    def setAlive(self):
        self.__lastSeen = time.time()
        self.__kaSent = None
        return

    def start(self):
        self.__callback = tornado.ioloop.PeriodicCallback(self._keepAlive, 1000, self.__wsClient.getIOLoop())
        self.__callback.start()

    def stop(self):
        if self.__callback is not None:
            self.__callback.stop()
        return

    def sendKeepAlive(self):
        raise NotImplementedError()

    def handleResponse(self, msg):
        raise NotImplementedError()


class WebSocketClientBase(tornadoclient.TornadoWebSocketClient):

    def __init__(self, url):
        super(WebSocketClientBase, self).__init__(url)
        self.__keepAliveMgr = None
        self.__connected = False
        return

    def _cleanup(self):
        ret = None
        try:
            ret = super(WebSocketClientBase, self)._cleanup()
        except Exception:
            pass

        return ret

    def getIOLoop(self):
        return tornado.ioloop.IOLoop.instance()

    def setKeepAliveMgr(self, keepAliveMgr):
        if self.__keepAliveMgr is not None:
            raise Exception('KeepAliveMgr already set')
        self.__keepAliveMgr = keepAliveMgr
        return

    def received_message(self, message):
        try:
            msg = json.loads(message.data)
            if self.__keepAliveMgr is not None:
                self.__keepAliveMgr.setAlive()
                if self.__keepAliveMgr.handleResponse(msg):
                    return
            self.onMessage(msg)
        except Exception as e:
            self.onUnhandledException(e)

        return

    def opened(self):
        self.__connected = True
        if self.__keepAliveMgr is not None:
            self.__keepAliveMgr.start()
            self.__keepAliveMgr.setAlive()
        self.onOpened()
        return

    def closed(self, code, reason=None):
        wasConnected = self.__connected
        self.__connected = False
        if self.__keepAliveMgr:
            self.__keepAliveMgr.stop()
            self.__keepAliveMgr = None
        tornado.ioloop.IOLoop.instance().stop()
        if wasConnected:
            self.onClosed(code, reason)
        return

    def isConnected(self):
        return self.__connected

    def startClient(self):
        tornado.ioloop.IOLoop.instance().start()

    def stopClient(self):
        try:
            if self.__connected:
                self.close()
            self.close_connection()
        except Exception as e:
            logger.warning('Failed to close connection: %s' % e)

    def onUnhandledException(self, exception):
        logger.critical('Unhandled exception', exc_info=exception)
        raise

    def onOpened(self):
        pass

    def onMessage(self, msg):
        raise NotImplementedError()

    def onClosed(self, code, reason):
        pass

    def onDisconnectionDetected(self):
        pass