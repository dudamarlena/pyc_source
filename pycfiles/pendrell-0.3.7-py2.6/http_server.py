# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pendrell/cases/http_server.py
# Compiled at: 2010-09-03 02:22:19
from twisted.internet import reactor
from twisted.internet.defer import Deferred, DeferredList, succeed, inlineCallbacks, returnValue
from twisted.web import http, server
from pendrell import log
NOT_DONE_YET = server.NOT_DONE_YET

class LoggingTransport(object):

    def __init__(self, transport):
        self.transport = transport

    def write(self, data):
        log.debug('Writing %r' % data)
        return self.transport.write(data)

    def writeSequence(self, seq):
        log.debug('Writing %r' % str().join(seq))
        return self.transport.writeSequence(seq)

    def __getattr__(self, attr):
        return getattr(self.transport, attr)


class JournalingRequest(server.Request):
    """Ensures that requests on a channel are not processed concurrently.
    Otherwise generating large data can fill memory.
    """

    def __init__(self, *args, **kw):
        self._queued = None
        self.__transport = None
        self.journal = kw.pop('journal', [])
        server.Request.__init__(self, *args, **kw)
        self.transport = LoggingTransport(self.transport)
        return

    @inlineCallbacks
    def process(self):
        yield self._waitToProcess()
        log.debug('Rendering: %r' % self)
        server.Request.process(self)

    def _waitToProcess(self):
        """Wait for noLongerQueued() to be called."""
        assert self._queued is None
        if self.queued:
            log.debug('%r: Waiting to render' % self)
            self._queued = d = Deferred()
        else:
            log.debug('%r: Rendering immediately' % self)
            d = succeed(self)
        return d

    def noLongerQueued(self):
        assert self._queued
        server.Request.noLongerQueued(self)
        q, self._queued = self._queued, None
        q.callback(self)
        return

    def write(self, data):
        log.debug('%r writing %r' % (self, data))
        return server.Request.write(self, data)

    def requestReceived(self, *req):
        server.Request.requestReceived(self, *req)
        self.journal.append(req)


class Site(server.Site):

    def __init__(self, resource):
        server.Site.__init__(self, resource)
        self.journal = []

    def requestFactory(self, *args, **kw):
        kw.setdefault('journal', self.journal)
        return JournalingRequest(*args, **kw)