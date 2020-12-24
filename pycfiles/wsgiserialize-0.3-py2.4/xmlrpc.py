# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiserialize\xmlrpc.py
# Compiled at: 2006-12-06 22:56:10
from xmlrpclib import dumps
__all__ = [
 'WSGIXmlRpc', 'xmlrpc']

def xmlrpc(application, **kw):
    """Decorator for XML-RPC serialization."""
    return WsgiXmlRpc(application, **kw)


class WsgiXmlRpc(object):
    """WSGI middleware for serializing simple Python objects to XML-RPC."""
    __module__ = __name__

    def __init__(self, application, **kw):
        self.application = application
        self.response = kw.get('methodresponse')
        self.name = kw.get('methodname')
        self.encoding = kw.get('encoding')
        self.allownone = kw.get('allow_none', 0)

    def __call__(self, environ, start_response):
        return [
         dumps(tuple([self.application(environ, start_response)]), self.response, self.name, self.encoding, self.allownone)]