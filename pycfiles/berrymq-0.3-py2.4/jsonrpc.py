# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/berrymq/jsonrpc/jsonrpc.py
# Compiled at: 2009-07-31 12:40:50
import sys, json, select, threading, traceback, xmlrpclib, SocketServer, SimpleXMLRPCServer

class ResponseError(xmlrpclib.ResponseError):
    __module__ = __name__


class Fault(xmlrpclib.ResponseError):
    __module__ = __name__


def _get_response(file, sock):
    data = ''
    while 1:
        if sock:
            response = sock.recv(1024)
        else:
            response = file.read(1024)
        if not response:
            break
        data += response

    file.close()
    return data


class Transport(xmlrpclib.Transport):
    __module__ = __name__

    def _parse_response(self, file, sock):
        return _get_response(file, sock)


class SafeTransport(xmlrpclib.SafeTransport):
    __module__ = __name__

    def _parse_response(self, file, sock):
        return _get_response(file, sock)


class ServerProxy:
    __module__ = __name__

    def __init__(self, uri, id=None, transport=None, use_datetime=0):
        import urllib
        (type, uri) = urllib.splittype(uri)
        if type not in ('http', 'https'):
            raise IOError, 'unsupported JSON-RPC protocol'
        (self.__host, self.__handler) = urllib.splithost(uri)
        if not self.__handler:
            self.__handler = '/JSON'
        if transport is None:
            if type == 'https':
                transport = SafeTransport(use_datetime=use_datetime)
            else:
                transport = Transport(use_datetime=use_datetime)
        self.__transport = transport
        self.__id = id
        return

    def __request(self, methodname, params):
        request = json.dumps(dict(id=self.__id, method=methodname, params=params))
        data = self.__transport.request(self.__host, self.__handler, request, verbose=False)
        response = json.loads(data)
        if response['id'] != self.__id:
            raise ResponseError('Invalid request id (is: %s, expected: %s)' % (response['id'], self.__id))
        if response['error'] is not None:
            raise Fault('JSON Error', response['error'])
        return response['result']

    def __repr__(self):
        return '<ServerProxy for %s%s>' % (self.__host, self.__handler)

    __str__ = __repr__

    def __getattr__(self, name):
        return xmlrpclib._Method(self.__request, name)


class SimpleJSONRPCDispatcher(SimpleXMLRPCServer.SimpleXMLRPCDispatcher):
    __module__ = __name__

    def _marshaled_dispatch(self, data, dispatch_method=None):
        id = None
        try:
            req = json.loads(data)
            method = req['method']
            params = req['params']
            id = req['id']
            if dispatch_method is not None:
                result = dispatch_method(method, params)
            else:
                result = self._dispatch(method, params)
            response = dict(id=id, result=result, error=None)
        except:
            (extpe, exv, extrc) = sys.exc_info()
            err = dict(type=str(extpe), message=str(exv), traceback=('').join(traceback.format_tb(extrc)))
            response = dict(id=id, result=None, error=err)

        try:
            return json.dumps(response)
        except:
            (extpe, exv, extrc) = sys.exc_info()
            err = dict(type=str(extpe), message=str(exv), traceback=('').join(traceback.format_tb(extrc)))
            response = dict(id=id, result=None, error=err)
            return json.dumps(response)

        return


class SimpleJSONRPCRequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    __module__ = __name__
    rpc_paths = ('/', '/JSON')


class SimpleJSONRPCServer(SocketServer.TCPServer, SimpleJSONRPCDispatcher):
    __module__ = __name__
    allow_reuse_address = True

    def __init__(self, addr, requestHandler=SimpleJSONRPCRequestHandler, logRequests=True):
        self.logRequests = logRequests
        SimpleJSONRPCDispatcher.__init__(self, allow_none=True, encoding=None)
        SocketServer.TCPServer.__init__(self, addr, requestHandler)
        self.__thread = None
        return

    def serve_forever(self, in_thread=False, poll_interval=0.5):

        def serve_thread(server, poll_interval):
            server.serve_forever(poll_interval=poll_interval)

        if in_thread:
            args = [
             self, poll_interval]
            self.__thread = threading.Thread(target=serve_thread, args=args)
            self.__thread.start()
        else:
            SocketServer.TCPServer.serve_forever(self, poll_interval)

    def shutdown(self):
        SocketServer.TCPServer.shutdown(self)
        if self.__thread:
            self.__thread.join()
            self.__thread = None
        return