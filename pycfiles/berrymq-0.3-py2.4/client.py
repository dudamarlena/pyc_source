# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/berrymq/jsonrpc/client.py
# Compiled at: 2009-09-13 11:47:26
import sys, select, threading, traceback, xmlrpclib
try:
    import fcntl
except ImportError:
    fcntl = None

try:
    import json
except ImportError:
    import simplejson as json

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
            if sys.version_info[:2] == (2, 4):
                if type == 'https':
                    transport = SafeTransport()
                else:
                    transport = Transport()
            elif type == 'https':
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
            raise Fault('JSON Error@%s' % self.__host, response['error'])
        return response['result']

    def __repr__(self):
        return '<ServerProxy for %s%s>' % (self.__host, self.__handler)

    __str__ = __repr__

    def __getattr__(self, name):
        return xmlrpclib._Method(self.__request, name)