# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twswebrpc/client.py
# Compiled at: 2014-06-10 08:51:37
from zope.interface import implementer
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, connectionDone
from twisted.internet.defer import Deferred, maybeDeferred, succeed
from twisted.python.failure import Failure
from twisted.web.client import Agent, HTTPConnectionPool, ContentDecoderAgent, GzipDecoder, ResponseDone
from twisted.web.http_headers import Headers
from twisted.web.iweb import IBodyProducer
from encoder import JSONEncoder, JellyEncoder, IEncoder

class StdError(Exception):
    """standard  error"""

    def __str__(self):
        s = self.__doc__
        if self.args:
            s = '%s: %s' % (s, (' ').join(self.args))
        s = '%s.' % s
        return s


class UnknownProtocol(StdError):
    """Unknown transfer protocol"""
    pass


class ServerError(StdError):
    """server Error"""
    pass


class WrongServerData(StdError):
    """Wrong server data"""
    pass


class WrongEncoding(StdError):
    """Wrong client data"""
    pass


class DataReceiver(Protocol):

    def __init__(self, finished, encoder):
        self.finished = finished
        self.encoder = encoder
        self.dataBytes = None
        return

    def dataReceived(self, dataBytes):
        if self.dataBytes:
            self.dataBytes += dataBytes
        else:
            self.dataBytes = dataBytes

    def connectionLost(self, reason=connectionDone):
        if reason.check(ResponseDone):
            try:
                response = self.encoder.decode(self.dataBytes)
            except Exception as exception:
                self.finished.errback(Failure(UnknownProtocol('error when decoding the server response: %s' % str(exception))))
            else:
                if isinstance(response, dict) and 'id' in response and 'result' in response:
                    errorData = response.get('error', None)
                    if errorData:
                        if isinstance(errorData, dict):
                            errorMessage = '%s :  %s' % (errorData.get('code', None),
                             errorData.get('message', None))
                            self.finished.errback(Failure(ServerError(errorMessage)))
                        else:
                            self.finished.errback(Failure(WrongServerData('error occurred but can not read from transferred response')))
                    else:
                        self.finished.callback(response['result'])
                else:
                    self.finished.errback(Failure(WrongServerData('the server data received is not conform')))
        else:
            self.finished.errback(reason)
        return


@implementer(IBodyProducer)
class StringProducer(object):

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def stopProducing(self):
        pass


class JSONClient(object):
    protocolName = 'jsonrpc'
    protocolVersion = '2.0'
    protocolContentType = 'text/json'
    userAgentName = 'twswebrpc'

    def __init__(self, url, callID=0, maxPersistentPerHost=2, useCompression=False):
        self.url = url
        self.encoder = self.get_encoder()
        assert IEncoder.providedBy(self.encoder), 'no encoder available or encoder does not provide IEncoder'
        assert isinstance(callID, (int, long)), "callID must be <type 'int'> or <type 'long'>"
        self.__callID = callID
        self.__callsCounter = 0
        if maxPersistentPerHost > 0:
            self.pool = HTTPConnectionPool(reactor, persistent=True)
            self.pool.maxPersistentPerHost = maxPersistentPerHost
        else:
            self.pool = None
        agent = Agent(reactor, pool=self.pool)
        if useCompression:
            self.agent = ContentDecoderAgent(agent, [('gzip', GzipDecoder)])
        else:
            self.agent = agent
        return

    def get_encoder(self):
        return JSONEncoder()

    @property
    def callID(self):
        return self.__callID

    def __callsCounterInc(self):
        self.__callsCounter += 1

    def __callsCounterDec(self):
        self.__callsCounter -= 1

    @property
    def callsCounter(self):
        return self.__callsCounter

    def callRemote(self, function, *params):
        self.__callID += 1
        data = dict(id=self.__callID, method=function, params=params)
        data[self.protocolName] = self.protocolVersion
        encodedData = self.encoder.encode(data)
        deferred = maybeDeferred(self.agent.request, 'POST', self.url, Headers({'User-Agent': [self.userAgentName], 'content-type': [
                          self.protocolContentType], 
           'content-length': [
                            str(len(encodedData))]}), StringProducer(encodedData))
        deferred.addCallback(self._onCallSuccess)
        deferred.addErrback(self._onCallError)
        self.__callsCounterInc()
        return deferred

    def _onCallSuccess(self, response):
        if response.code != 200:
            return Failure(ServerError('%s - %s' % (response.code, response.phrase)))
        finished = Deferred()
        finished.addCallback(self._onCallSuccessFinish)
        response.deliverBody(DataReceiver(finished, self.encoder))
        return finished

    def _onCallSuccessFinish(self, response):
        self.__callsCounterDec()
        return response

    def _onCallError(self, response):
        self.__callsCounterDec()
        return response

    def closeCachedConnections(self, callBack=None):
        if self.pool:
            deferred = self.pool.closeCachedConnections()
            if callBack:
                assert callable(callBack)
                return deferred.addCallback(callBack)
            return deferred
        return


class JellyClient(JSONClient):
    protocolName = 'jellyrpc'
    protocolVersion = '1.0'
    protocolContentType = 'text/jelly'

    def get_encoder(self):
        return JellyEncoder()