# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted_goodies/webfetch/http.py
# Compiled at: 2007-07-25 20:13:09
from twisted.web2.client import http

class HTTPClientChannelRequest(http.HTTPClientChannelRequest):
    """
    """
    __module__ = __name__

    def submit(self):
        l = []
        request = self.request
        if request.method == 'HEAD':
            self.length = 0
        l.append('%s %s %s\r\n' % (request.method, request.uri, self.outgoing_version))
        if request.headers is not None:
            for (name, valuelist) in request.headers.getAllRawHeaders():
                for value in valuelist:
                    l.append('%s: %s\r\n' % (name, value))

        if request.stream is not None:
            if request.stream.length is not None:
                l.append('%s: %s\r\n' % ('Content-Length', request.stream.length))
            else:
                l.append('%s: %s\r\n' % ('Transfer-Encoding', 'chunked'))
                self.chunkedOut = True
        l.append('\r\n')
        self.transport.writeSequence(l)
        d = http.stream_mod.StreamProducer(request.stream).beginProducing(self)
        d.addCallback(self._finish).addErrback(self._error)
        return

    def createRequest(self):
        print '\ncreateRequest'
        self.stream = http.stream_mod.ProducerStream()
        self.response = http.http.Response(self.code, self.inHeaders, self.stream)
        self.stream.registerProducer(self, True)
        del self.inHeaders

    def processRequest(self):
        print '\nprocessRequest'
        self.responseDefer.callback(self.response)


class HTTPClientProtocol(http.HTTPClientProtocol):
    """
    """
    __module__ = __name__

    def lineReceived(self, line):
        print '\nlineReceived', line
        if not self.inRequests:
            self.transport.loseConnection()
            return
        if self.inRequests[0] is not self.outRequest:
            self.setTimeout(self.inputTimeOut)
        if self.firstLine:
            self.firstLine = 0
            self.inRequests[0].gotInitialLine(line)
        else:
            self.inRequests[0].lineReceived(line)

    def rawDataReceived(self, data):
        print '\nrawDataReceived', data
        if not self.inRequests:
            print 'Extra raw data!'
            self.transport.loseConnection()
            return
        if self.inRequests[0] is not self.outRequest:
            self.setTimeout(self.inputTimeOut)
        self.inRequests[0].rawDataReceived(data)

    def submitRequest(self, request, closeAfter=True):
        """
        @param request: The request to send to a remote server.
        @type request: L{ClientRequest}

        @param closeAfter: If True the 'Connection: close' header will be sent,
            otherwise 'Connection: keep-alive'
        @type closeAfter: C{bool}

        @return: L{twisted.internet.defer.Deferred} 
        @callback: L{twisted.web2.http.Response} from the server.
        """
        print '\nsubmitRequest', request, closeAfter
        assert self.outRequest is None
        assert self.readPersistent is http.PERSIST_NO_PIPELINE and not self.inRequests or self.readPersistent is http.PERSIST_PIPELINE
        self.manager.clientBusy(self)
        if closeAfter:
            self.readPersistent = False
        self.outRequest = chanRequest = HTTPClientChannelRequest(self, request, closeAfter)
        self.inRequests.append(chanRequest)
        chanRequest.submit()
        return chanRequest.responseDefer

    def requestWriteFinished(self, request):
        assert request is self.outRequest
        self.outRequest = None
        self.setTimeout(self.inputTimeOut)
        if self.readPersistent is http.PERSIST_PIPELINE:
            self.manager.clientPipelining(self)
        return

    def requestReadFinished(self, request):
        assert self.inRequests[0] is request
        del self.inRequests[0]
        self.firstLine = True
        if not self.inRequests:
            if self.readPersistent:
                self.setTimeout(None)
                self.manager.clientIdle(self)
            else:
                self.transport.loseConnection()
        return

    def setReadPersistent(self, persist):
        self.readPersistent = persist
        if not persist:
            for request in self.inRequests[1:]:
                request.connectionLost(None)

            del self.inRequests[1:]
        return

    def connectionLost(self, reason):
        self.readPersistent = False
        self.setTimeout(None)
        self.manager.clientGone(self)
        for request in self.inRequests:
            if request is not None:
                request.connectionLost(reason)

        return