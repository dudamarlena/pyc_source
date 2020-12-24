# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/jsonrpc_server.py
# Compiled at: 2015-02-12 15:25:14
from __future__ import print_function
from twisted.internet import ssl
import traceback
from twisted.internet import reactor
from twisted.web import server, iweb
from twisted.web.resource import EncodingResourceWrapper
from jsonrpc.server import ServerEvents, JSON_RPC
import bayesdb.engine as engine_module
engine_methods = engine_module.get_method_names()
from bayesdb.engine import Engine
engine = Engine()

class ExampleServer(ServerEvents):

    def log(self, responses, txrequest, error):
        print(txrequest.code, end=' ')
        if isinstance(responses, list):
            for response in responses:
                msg = self._get_msg(response)
                print(txrequest, msg)

        else:
            msg = self._get_msg(responses)
            print(txrequest, msg)

    def findmethod(self, method, args=None, kwargs=None):
        if method in self.methods:
            return getattr(engine, method)
        else:
            return
            return

    methods = set(engine_methods)

    def _get_msg(self, response):
        ret_str = 'No id response: %s' % str(response)
        if hasattr(response, 'id'):
            ret_str = str(response.id)
            if response.result:
                ret_str += '; result: %s' % str(response.result)
            else:
                ret_str += '; error: %s' % str(response.error)
                for at in dir(response):
                    if not at.startswith('__'):
                        print(at + ': ' + str(getattr(response, at)))

                print('response:\n' + str(dir(response)))
        return ret_str


class CorsEncoderFactory(object):

    def encoderForRequest(self, request):
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'PUT, GET')
        return _CorsEncoder(request)


class _CorsEncoder(object):
    """
      @ivar _request: A reference to the originating request.
      
      @since: 12.3
      """

    def __init__(self, request):
        self._request = request

    def encode(self, data):
        return data

    def finish(self):
        return ''


root = JSON_RPC().customize(ExampleServer)
wrapped = EncodingResourceWrapper(root, [CorsEncoderFactory()])
site = server.Site(wrapped)
PORT = 8008
print('Listening on port %d...' % PORT)
reactor.listenTCP(PORT, site)
reactor.run()