# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twswebrpc/resource.py
# Compiled at: 2014-06-10 08:45:22
from twisted.web.resource import Resource
from twisted.web import server
from twisted.internet import defer
from twisted.web.server import GzipEncoderFactory
from encoder import IEncoder, JSONEncoder, JellyEncoder
ERROR_CODE_INVALID_JSON_PARSE_TEXT = -32700
ERROR_CODE_INVALID_JSON_REQUEST_OBJECT = -32600
ERROR_CODE_METHOD_NOT_FOUND = -32601
ERROR_CODE_INVALID_PARAMETERS = -32602
ERROR_CODE_SERVER_ERROR = -32603

class JSONResource(Resource):
    protocolName = 'jsonrpc'
    protocolVersion = '2.0'
    protocolContentType = 'text/json'
    protocolErrorName = 'JSONRPCError'
    isLeaf = True

    def __init__(self, logger=None):
        Resource.__init__(self)
        self._methods = {}
        self._methods_with_requests = []
        self.logger = logger
        self.initMethods()
        self._gzipEncoderFactory = None
        self.encoder = self.get_encoder()
        assert IEncoder.providedBy(self.encoder), 'encoder does not provide IEncoder (no encoder available)'
        return

    def getCompressLevel(self):
        return self._gzipEncoderFactory.compressLevel

    def setCompressLevel(self, value):
        self._gzipEncoderFactory.compressLevel = value

    compressLevel = property(getCompressLevel, setCompressLevel)

    def getUseCompression(self):
        if self._gzipEncoderFactory:
            return True
        return False

    def setUseCompression(self, value):
        if value:
            self._gzipEncoderFactory = GzipEncoderFactory()
        else:
            self._gzipEncoderFactory = None
        return

    useCompression = property(getUseCompression, setUseCompression)

    def get_encoder(self):
        return JSONEncoder()

    def initMethods(self):
        """
        override this to auto register your methods
        make use of self.add_method(name,method)
        for example:
        self.add_method('echo',self.echo)
        """
        pass

    def add_method(self, name, method, with_request=False):
        """
        This can called to register class methods or external function to be called by rpc clients
        :param name string name that clients will call to reach this method
        :param method a method or function that will be called when clients call name method

        """
        self._methods[name] = method
        if with_request:
            if name not in self._methods_with_requests:
                self._methods_with_requests.append(name)
        elif name in self._methods_with_requests:
            self._methods_with_requests.remove(name)

    def remove_method(self, name):
        if name in self._methods:
            del self._methods[name]
        if name in self._methods_with_requests:
            self._methods_with_requests.remove(name)

    def list_methods(self):
        return list(self._methods)

    def has_method(self, name):
        return name in self._methods

    def get_method(self, name):
        if name in self._methods:
            return self._methods[name]
        else:
            return

    def requestAborted(self, err, deferred, request):
        """
        The client has disconnected while call is running if more cleanup needed,
        inherit this method
        """
        deferred.cancel()
        if self.logger:
            self.logger('call cancelled: %s:%s > %s ' % (
             request.client.host, request.client.port, err.getErrorMessage()))

    def response(self, callID, result, error=None, version=None):
        if version is None:
            version = self.protocolVersion
        if version == '2.0':
            message = dict(id=callID, result=result)
            message[self.protocolName] = version
            if error:
                message['error'] = error
        else:
            message = dict(version=self.protocolVersion, id=callID, result=result, error=error)
        return self.encoder.encode(message)

    def error(self, callID, code, message, data=None, version=None):
        if version is None:
            version = self.protocolVersion
        error_message = dict(code=code, message=message, data=data)
        return self.response(callID, None, error=error_message, version=version)

    def render(self, request):
        request.content.seek(0, 0)
        content = request.content.read()
        d = defer.maybeDeferred(self.process, content, request)
        request.notifyFinish().addErrback(self.requestAborted, d, request)
        d.addCallback(self.processSuccess, request)
        d.addErrback(self.processError, request)
        return server.NOT_DONE_YET

    def process(self, data, request):
        try:
            decodedData = self.encoder.decode(data)
        except Exception as exception:
            return self.error(0, ERROR_CODE_INVALID_JSON_PARSE_TEXT, 'invalid protocol %s:, %s' % (
             self.protocolContentType, str(exception)))

        if not isinstance(decodedData, dict):
            return self.error(0, ERROR_CODE_INVALID_JSON_PARSE_TEXT, "invalid protocol waiting <type 'dict'> received %s" % type(decodedData))
        else:
            if self.protocolName in decodedData:
                version = decodedData[self.protocolName]
            else:
                version = '1.0'
            callID = decodedData.get('id', 0)
            methodName = decodedData.get('method', None)
            params = decodedData.get('params', [])
            if not isinstance(params, (list, tuple)):
                return self.error(callID, ERROR_CODE_INVALID_PARAMETERS, 'protocol params must be list or tuple')
            method = self.get_method(methodName)
            if not method:
                return self.error(callID, ERROR_CODE_METHOD_NOT_FOUND, 'method "%s" does not exist' % methodName)
            if methodName in self._methods_with_requests:
                d = defer.maybeDeferred(method, request, *params)
            else:
                d = defer.maybeDeferred(method, *params)
            d.addCallback(self._execMethodSuccess, callID, version)
            d.addErrback(self._execMethodError, callID, version)
            return d

    def processSuccess(self, result, request):
        if not request._disconnected:
            request.setResponseCode(200)
            request.setHeader('content-type', self.protocolContentType)
            if self._gzipEncoderFactory:
                gzipEncoder = self._gzipEncoderFactory.encoderForRequest(request)
            else:
                gzipEncoder = None
            if gzipEncoder:
                request.write(gzipEncoder.encode(result))
                request.write(gzipEncoder.finish())
            else:
                request.setHeader('content-length', str(len(result)))
                request.write(result)
            request.finish()
        return

    def processError(self, failure, request):
        """
        in normal situations this errBack will never happen,
        in this situation i do know where the problem occurred
        """
        if not request._disconnected:
            result = self.error(None, ERROR_CODE_SERVER_ERROR, failure.getErrorMessage())
            request.setResponseCode(500)
            request.setHeader('content-type', self.protocolContentType)
            request.setHeader('content-length', str(len(result)))
            request.write(result)
            request.finish()
        return

    def _execMethodSuccess(self, result, callID, version):
        return self.response(callID, result, version=version)

    def _execMethodError(self, failure, callID, version):
        return self.error(callID, ERROR_CODE_SERVER_ERROR, failure.getErrorMessage(), version=version)


class JellyResource(JSONResource):
    protocolName = 'jellyrpc'
    protocolVersion = '2.0'
    protocolContentType = 'text/jelly'
    protocolErrorName = 'JELLYRPCError'

    def get_encoder(self):
        return JellyEncoder()