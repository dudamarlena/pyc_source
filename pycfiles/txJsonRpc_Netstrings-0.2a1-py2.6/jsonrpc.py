# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/txjsonrpc_netstrings/jsonrpc.py
# Compiled at: 2011-03-25 22:59:12
from twisted.protocols.basic import NetstringReceiver
from twisted.internet import defer, reactor
import jsonrpclib, json
from twisted.python import log
import logging

class Protocol(NetstringReceiver):
    requests = {}
    id = 1
    MAX_LENGTH = 10485760

    def __init__(self, onConnect=None, onDisconnect=None):
        """Overrid these instance variables to set callbacks on connect and disconnect"""
        self.onConnect = onConnect
        self.onDisconnect = onDisconnect
        if not hasattr(self, 'encoder'):
            self.encoder = jsonrpclib.JsonRpcEncoder

    def connectionMade(self):
        if self.onConnect:
            self.onConnect(self)

    def connectionLost(self, reason):
        if self.onDisconnect:
            self.onDisconnect(self)

    def stringReceived(self, string):
        message_id = None
        try:
            if len(string) > self.MAX_LENGTH:
                raise jsonrpclib.JsonRpcTooBigError()
            try:
                obj = jsonrpclib.load_string(string)
            except json.decoder.JSONDecodeError:
                raise jsonrpclib.JsonRpcParseError()

            if 'jsonrpc' not in obj or obj['jsonrpc'] != '2.0':
                raise jsonrpclib.JsonRpcInvalidRequestError()
            if 'id' in obj:
                message_id = obj['id']
            if 'method' in obj:
                method, params, message_id = obj['method'], obj['params'], obj['id']
                if hasattr(self, '_getFunction'):
                    f = self._getFunction(method)
                    d = f(params)
                    d.addCallback(self.responseReady, message_id)
                    d.addErrback(self.internalError, message_id)
                else:
                    logging.debug('** Client Got Request **')
                    logging.debug('%s - %s' % (method, params))
                    d = defer.Deferred()
                    d.addCallback(self.responseReady, message_id)
                    reactor.callLater(0, d.callback, 'ok')
            elif 'result' in obj:
                result, message_id = obj['result'], obj['id']
                if message_id in self.requests:
                    self.requests[message_id].callback(result)
        except Exception, error:
            log.err()
            if not isinstance(error, jsonrpclib.JsonRpcClientError):
                self.errorReady(error, message_id)

        if 'error' in obj and obj['error'] is not None:
            code, message = obj['error']['code'], obj['error']['message']
            if message_id in self.requests:
                exception = jsonrpclib.JsonRpcClientError()
                exception.message = message
                exception.code = code
                self.requests[message_id].errback(exception)
            else:
                logging.debug('****** NO ERRBACK ******')
        return

    def sendRequest(self, method, params={}):
        """This method is used as a client sending a request to a server"""
        req_id = str(self.id)
        self.id += 1
        if self.id > 65000:
            self.id = 1
        string = jsonrpclib.dump_request(method, params, req_id, encoder=self.encoder)
        if len(string) > self.MAX_LENGTH:
            raise jsonrpclib.JsonRpcTooBigError()
        packet = '%d:%s,' % (len(string), string)
        self.transport.write(packet)
        d = defer.Deferred()
        self.requests[req_id] = d
        return d

    def responseReady(self, result, req_id):
        """This is called when the server wants to respond to a request"""
        string = jsonrpclib.dump_response(result, req_id, encoder=self.encoder)
        if len(string) > self.MAX_LENGTH:
            self.errorReady(jsonrpclib.JsonRpcTooBigError(), req_id)
            return
        packet = '%d:%s,' % (len(string), string)
        logging.debug('Reply: %s...' % string)
        self.transport.write(packet)

    def errorReady(self, error, req_id):
        string = jsonrpclib.dump_error(error, req_id)
        packet = '%d:%s,' % (len(string), string)
        logging.debug('Error Reply: %s' % string)
        self.transport.write(packet)

    def internalError(self, failure, message_id):
        failure_message = failure.getErrorMessage()
        logging.error(failure.getTraceback())
        error = jsonrpclib.JsonRpcInternalError()
        error.message = failure_message
        self.errorReady(error, message_id)