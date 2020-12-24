# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\websocket\client.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 6147 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import json, time, threading, six
from ws4py.client import tornadoclient
import tornado
if six.PY3:
    import asyncio, tornado.platform.asyncio
import pyalgotrade.logger
logger = pyalgotrade.logger.getLogger('websocket.client')

class KeepAliveMgr(object):

    def __init__(self, wsClient, maxInactivity, responseTimeout):
        assert maxInactivity > 0
        assert responseTimeout > 0
        self._KeepAliveMgr__callback = None
        self._KeepAliveMgr__wsClient = wsClient
        self._KeepAliveMgr__activityTimeout = maxInactivity
        self._KeepAliveMgr__responseTimeout = responseTimeout
        self._KeepAliveMgr__lastSeen = None
        self._KeepAliveMgr__kaSent = None

    def _keepAlive(self):
        if self._KeepAliveMgr__lastSeen is None:
            return
            inactivity = time.time() - self._KeepAliveMgr__lastSeen
            if inactivity <= self._KeepAliveMgr__activityTimeout:
                return
        else:
            try:
                if self._KeepAliveMgr__kaSent is None:
                    self.sendKeepAlive()
                    self._KeepAliveMgr__kaSent = time.time()
                else:
                    if time.time() - self._KeepAliveMgr__kaSent > self._KeepAliveMgr__responseTimeout:
                        self._KeepAliveMgr__wsClient.onDisconnectionDetected()
            except Exception:
                self._KeepAliveMgr__wsClient.onDisconnectionDetected()

    def getWSClient(self):
        return self._KeepAliveMgr__wsClient

    def setAlive(self):
        self._KeepAliveMgr__lastSeen = time.time()
        self._KeepAliveMgr__kaSent = None

    def start(self):
        self._KeepAliveMgr__callback = tornado.ioloop.PeriodicCallback(self._keepAlive, 1000)
        self._KeepAliveMgr__callback.start()

    def stop(self):
        if self._KeepAliveMgr__callback is not None:
            self._KeepAliveMgr__callback.stop()

    def sendKeepAlive(self):
        raise NotImplementedError()

    def handleResponse(self, msg):
        raise NotImplementedError()


class WebSocketClientBase(tornadoclient.TornadoWebSocketClient):

    def __init__(self, url):
        super(WebSocketClientBase, self).__init__(url)
        self._WebSocketClientBase__keepAliveMgr = None
        self._WebSocketClientBase__connected = False

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
        if self._WebSocketClientBase__keepAliveMgr is not None:
            raise Exception('KeepAliveMgr already set')
        self._WebSocketClientBase__keepAliveMgr = keepAliveMgr

    def received_message(self, message):
        try:
            msg = json.loads(message.data)
            if self._WebSocketClientBase__keepAliveMgr is not None:
                self._WebSocketClientBase__keepAliveMgr.setAlive()
                if self._WebSocketClientBase__keepAliveMgr.handleResponse(msg):
                    return
            self.onMessage(msg)
        except Exception as e:
            try:
                self.onUnhandledException(e)
            finally:
                e = None
                del e

    def opened(self):
        self._WebSocketClientBase__connected = True
        if self._WebSocketClientBase__keepAliveMgr is not None:
            self._WebSocketClientBase__keepAliveMgr.start()
            self._WebSocketClientBase__keepAliveMgr.setAlive()
        self.onOpened()

    def closed(self, code, reason=None):
        wasConnected = self._WebSocketClientBase__connected
        self._WebSocketClientBase__connected = False
        if self._WebSocketClientBase__keepAliveMgr:
            self._WebSocketClientBase__keepAliveMgr.stop()
            self._WebSocketClientBase__keepAliveMgr = None
        tornado.ioloop.IOLoop.instance().stop()
        if wasConnected:
            self.onClosed(code, reason)

    def isConnected(self):
        return self._WebSocketClientBase__connected

    def startClient(self):
        tornado.ioloop.IOLoop.instance().start()

    def stopClient(self):
        try:
            if self._WebSocketClientBase__connected:
                self.close()
            self.close_connection()
        except Exception as e:
            try:
                logger.warning('Failed to close connection: %s' % e)
            finally:
                e = None
                del e

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


class WebSocketClientThreadBase(threading.Thread):

    def run(self):
        if six.PY3:
            asyncio.set_event_loop_policy(tornado.platform.asyncio.AnyThreadEventLoopPolicy())