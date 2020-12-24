# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/echo.py
# Compiled at: 2018-12-17 11:51:20
__all__ = [
 'startClient', 'startServer']
from autobahn.twisted.websocket import connectWS, listenWS, WebSocketClientFactory, WebSocketClientProtocol, WebSocketServerFactory, WebSocketServerProtocol

class EchoServerProtocol(WebSocketServerProtocol):

    def onMessage(self, payload, isBinary):
        self.sendMessage(payload, isBinary)


class EchoServerFactory(WebSocketServerFactory):
    protocol = EchoServerProtocol

    def __init__(self, url, debug=False):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debug)


class EchoClientProtocol(WebSocketClientProtocol):

    def onMessage(self, payload, isBinary):
        self.sendMessage(payload, isBinary)


class EchoClientFactory(WebSocketClientFactory):
    protocol = EchoClientProtocol

    def __init__(self, url, debug=False):
        WebSocketClientFactory.__init__(self, url, debug=debug, debugCodePaths=debug)


def startClient(wsuri, debug=False):
    factory = EchoClientFactory(wsuri, debug)
    connectWS(factory)
    return True


def startServer(wsuri, sslKey=None, sslCert=None, debug=False):
    factory = EchoServerFactory(wsuri, debug)
    if sslKey and sslCert:
        sslContext = ssl.DefaultOpenSSLContextFactory(sslKey, sslCert)
    else:
        sslContext = None
    listenWS(factory, sslContext)
    return True