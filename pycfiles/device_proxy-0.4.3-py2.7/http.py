# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/devproxy/utils/http.py
# Compiled at: 2013-09-27 03:39:58
from zope.interface import implements
from twisted.internet import defer
from twisted.internet.defer import succeed
from twisted.internet import reactor, protocol
from twisted.web.client import Agent, ResponseDone
from twisted.web.http_headers import Headers
from twisted.web.iweb import IBodyProducer
from twisted.web.http import PotentialDataLoss

def mkheaders(headers):
    """
    Turn a dict of HTTP headers into an instance of Headers.

    Twisted expects a list of values, not a single value. We should
    support both.
    """
    raw_headers = {}
    for k, v in headers.iteritems():
        if isinstance(v, basestring):
            v = [
             v]
        raw_headers[k] = v

    return Headers(raw_headers)


class StringProducer(object):
    """
    For various twisted.web mechanics we need a producer to produce
    content for HTTP requests, this is a helper class to quickly
    create a producer for a bit of content
    """
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


class SimplishReceiver(protocol.Protocol):

    def __init__(self, response):
        self.deferred = defer.Deferred()
        self.response = response
        self.response.delivered_body = ''
        if response.code == 204:
            self.deferred.callback(self.response)
        else:
            response.deliverBody(self)

    def dataReceived(self, data):
        self.response.delivered_body += data

    def connectionLost(self, reason):
        if reason.check(ResponseDone):
            self.deferred.callback(self.response)
        elif reason.check(PotentialDataLoss):
            self.deferred.callback(self.response)
        else:
            self.deferred.errback(reason)


def request(url, data=None, headers={}, method='POST'):
    agent = Agent(reactor)
    d = agent.request(method, url, mkheaders(headers), StringProducer(data) if data else None)

    def handle_response(response):
        return SimplishReceiver(response).deferred

    d.addCallback(handle_response)
    return d