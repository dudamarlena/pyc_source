# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/PyJSONService.py
# Compiled at: 2008-09-03 13:55:14
"""
  PyJSONRPCService.py is an over-simplified JSON RPC proxy client.
  It uses urllib.urlopen() and therefore does not provide crucial
  asynchronous functionality.  See JSONService.py for proper
  asynchronous JSON RPC client functionality, using DOM XMLHttpRequest.

"""
import urllib
from jsonrpc.json import dumps, loads, JSONDecodeException

class JSONRequestInfo:

    def __init__(self, id, method, handler):
        self.id = id
        self.method = method
        self.handler = handler


class JSONRPCException(Exception):

    def __init__(self, rpcError):
        Exception.__init__(self)
        self.error = rpcError


class ServiceProxy(object):

    def __init__(self, serviceURL, serviceName=None):
        self.__serviceURL = serviceURL
        self.__serviceName = serviceName

    def __getattr__(self, name):
        if self.__serviceName != None:
            name = '%s.%s' % (self.__serviceName, name)
        return ServiceProxy(self.__serviceURL, name)

    def __call__(self, *args):
        postdata = dumps({'method': self.__serviceName, 'params': args[:-1], 'id': 'jsonrpc'})
        respdata = urllib.urlopen(self.__serviceURL, postdata).read()
        try:
            resp = loads(respdata)
        except JSONDecodeException:
            args[(-1)].onRemoteError(0, 'decode failure', None)
            return -1

        resp_info = JSONRequestInfo(resp['id'], self.__serviceName, args[(-1)])
        print 'resp', resp
        if not resp:
            args[(-1)].onRemoteError(0, 'decode failure', None)
            return -1
        if not resp.has_key('error') or resp['error'] == None:
            args[(-1)].onRemoteResponse(resp['result'], resp_info)
            return resp['id']
        else:
            args[(-1)].onRemoteError(resp.get('code'), resp['error'], resp_info)
            return -1
        return


class JSONProxy(ServiceProxy):

    def __init__(self, location, fns):
        ServiceProxy.__init__(self, 'http://127.0.0.1/%s' % location)


class EchoServicePython(JSONProxy):
    """ example service (see examples/jsonrpc/JSONRPCExample.py)
    """

    def __init__(self):
        JSONProxy.__init__(self, '/cgi-bin/EchoService.py', ['echo', 'reverse', 'uppercase', 'lowercase'])


if __name__ == '__main__':

    class test:

        def __init__(self):
            self.s = EchoServicePython()
            self.s.echo('hello', self)
            self.s.reverse('reverse', self)
            self.s.sodyou('reverse', self)

        def onRemoteError(self, code, message, resp_info):
            print code, message, resp_info

        def onRemoteResponse(self, response, resp_info):
            if resp_info.method == 'echo':
                print 'echo', response
            if resp_info.method == 'echo':
                print 'reverse', response


    test()