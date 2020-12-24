# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/berrymq/jsonrpc/server_common.py
# Compiled at: 2009-10-02 08:47:03
import sys, traceback, SocketServer, SimpleXMLRPCServer
try:
    import json
except ImportError:
    import simplejson as json

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