# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/testee.py
# Compiled at: 2018-12-17 11:51:20
__all__ = [
 'startClient', 'startServer']
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File
import autobahn
from autobahn.twisted.websocket import connectWS, listenWS
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.websocket.compress import *

class TesteeServerProtocol(WebSocketServerProtocol):

    def onMessage(self, payload, isBinary):
        self.sendMessage(payload, isBinary)


class StreamingTesteeServerProtocol(WebSocketServerProtocol):

    def onMessageBegin(self, isBinary):
        WebSocketServerProtocol.onMessageBegin(self, isBinary)
        self.beginMessage(isBinary=isBinary)

    def onMessageFrameBegin(self, length):
        WebSocketServerProtocol.onMessageFrameBegin(self, length)
        self.beginMessageFrame(length)

    def onMessageFrameData(self, data):
        self.sendMessageFrameData(data)

    def onMessageFrameEnd(self):
        pass

    def onMessageEnd(self):
        self.endMessage()


class TesteeServerFactory(WebSocketServerFactory):
    protocol = TesteeServerProtocol

    def __init__(self, url, debug=False, ident=None):
        if ident is not None:
            server = ident
        else:
            server = 'AutobahnPython/%s' % autobahn.version
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debug, server=server)
        self.setProtocolOptions(failByDrop=False)

        def accept(offers):
            for offer in offers:
                if isinstance(offer, PerMessageDeflateOffer):
                    return PerMessageDeflateOfferAccept(offer)
                if isinstance(offer, PerMessageBzip2Offer):
                    return PerMessageBzip2OfferAccept(offer)
                if isinstance(offer, PerMessageSnappyOffer):
                    return PerMessageSnappyOfferAccept(offer)

        self.setProtocolOptions(perMessageCompressionAccept=accept)
        return


class TesteeClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        if self.factory.endCaseId is None:
            print 'Getting case count ..'
        elif self.factory.currentCaseId <= self.factory.endCaseId:
            print 'Running test case %d/%d as user agent %s on peer %s' % (self.factory.currentCaseId, self.factory.endCaseId, self.factory.agent, self.peer)
        return

    def onMessage(self, msg, binary):
        if self.factory.endCaseId is None:
            self.factory.endCaseId = int(msg)
            print 'Ok, will run %d cases' % self.factory.endCaseId
        else:
            self.sendMessage(msg, binary)
        return


class TesteeClientFactory(WebSocketClientFactory):
    protocol = TesteeClientProtocol

    def __init__(self, url, debug=False, ident=None):
        WebSocketClientFactory.__init__(self, url, useragent=ident, debug=debug, debugCodePaths=debug)
        self.setProtocolOptions(failByDrop=False)
        offers = [
         PerMessageDeflateOffer()]
        self.setProtocolOptions(perMessageCompressionOffers=offers)

        def accept(response):
            if isinstance(response, PerMessageDeflateResponse):
                return PerMessageDeflateResponseAccept(response)
            if isinstance(response, PerMessageBzip2Response):
                return PerMessageBzip2ResponseAccept(response)
            if isinstance(response, PerMessageSnappyResponse):
                return PerMessageSnappyResponseAccept(response)

        self.setProtocolOptions(perMessageCompressionAccept=accept)
        self.endCaseId = None
        self.currentCaseId = 0
        self.updateReports = True
        if ident is not None:
            self.agent = ident
        else:
            self.agent = 'AutobahnPython/%s' % autobahn.version
        self.resource = '/getCaseCount'
        return

    def clientConnectionLost(self, connector, reason):
        self.currentCaseId += 1
        if self.currentCaseId <= self.endCaseId:
            self.resource = '/runCase?case=%d&agent=%s' % (self.currentCaseId, self.agent)
            connector.connect()
        elif self.updateReports:
            self.resource = '/updateReports?agent=%s' % self.agent
            self.updateReports = False
            connector.connect()
        else:
            reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print 'Connection to %s failed (%s)' % (self.url, reason.getErrorMessage())
        reactor.stop()


def startClient(wsuri, ident=None, debug=False):
    factory = TesteeClientFactory(wsuri, ident=ident, debug=debug)
    connectWS(factory)
    return True


def startServer(wsuri, webport=None, sslKey=None, sslCert=None, debug=False):
    factory = TesteeServerFactory(wsuri, debug)
    if sslKey and sslCert:
        sslContext = ssl.DefaultOpenSSLContextFactory(sslKey, sslCert)
    else:
        sslContext = None
    listenWS(factory, sslContext)
    if webport:
        webdir = File(pkg_resources.resource_filename('autobahntestsuite', 'web/echoserver'))
        web = Site(webdir)
        reactor.listenTCP(webport, web)
    return True