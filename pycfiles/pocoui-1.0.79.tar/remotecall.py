# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/core/remotecall.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = '\n    pocoo.pkg.core.remotecall\n    ~~~~~~~~~~~~~~~~~~~~~~~~~\n\n    Pocoo remote call support.\n\n\n    Remote Call Implementation\n    ==========================\n\n    The Pocoo XMLRPC/JSONRPC interface works like this::\n\n        import time\n        from pocoo.pkg.core.remotecall import RemoteCallable, export\n\n        class MyClass(RemoteCallable):\n\n            @export("test.hello_world")\n            def say(self, req, name=\'World\'):\n                return \'Hello %s!\' % name\n\n            @export("test.get_servertime")\n            def servertime(self, req):\n                return time.time()\n\n    By now only jsonrpc is available. You can query the jsonrpc interface\n    under ``/!jsonrpc``. The exported names are ``packagename.<name>``.\n    So for the example above the method names are (assumed that the module\n    is in package ``core``)::\n\n        core.test.hello_world\n\n    and::\n\n        core.test.get_servertime\n\n\n    JavaScript Query\n    =================\n\n    You can query those functions using the following syntax::\n\n        var rpc = new pocoo.lib.async.RPC(\'!jsonrpc\');\n        var method = rpc.getMethod(\'methodname\');\n        method(arguments, kwarguments, callback);\n\n    The query for the example above would be::\n\n        var rpc = new pocoo.lib.async.RPC(\'!jsonrpc\');\n        var method = rpc.getMethod(\'core.test.hello_world\');\n        method(["Benjamin"], {}, function (result) {\n            alert(result);\n            // alerts "Hello Benjamin!"\n        });\n\n\n    :copyright: 2006 by Armin Ronacher.\n    :license: GNU GPL, see LICENSE for more details.\n'
import new
from types import FunctionType
from pocoo.http import DirectResponse
from pocoo.context import Component
from pocoo.application import RequestHandler
from pocoo.http import Response
from pocoo.utils import json

class _RemoteCallableMeta(type):
    __module__ = __name__

    def __new__(cls, name, bases, d):
        rpc_exports = {}
        result = type.__new__(cls, name, bases, d)
        for (name, ref) in d.iteritems():
            if isinstance(ref, FunctionType) and getattr(ref, 'rpc_exported', False):
                name = '%s.%s' % (ref.__module__.split('.')[2], ref.rpc_name)
                rpc_exports[name] = ref

        result.rpc_exports = rpc_exports
        return result


class RemoteCallable(Component):
    """
    Components inheriting from this base component can export methods
    for jsonrpc if they are decorated using `export`.

    Example::

        from pocoo.pkg.core.remotecall import RemoteCallable, export

        class MyExport(RemoteCallable):
    """
    __module__ = __name__
    __metaclass__ = _RemoteCallableMeta


class RemoteCallManager(RequestHandler):
    __module__ = __name__
    handler_regexes = [
     '!jsonrpc$']

    def __init__(self, ctx):
        super(RemoteCallManager, self).__init__(ctx)
        self._mapping = None
        return

    def handle_request(self, req):
        if self._mapping is None:
            self._mapping = {}
            for comp in self.ctx.get_components(RemoteCallable):
                for (name, ref) in comp.rpc_exports.iteritems():
                    handler = new.instancemethod(ref, comp, comp.__class__)
                    self._mapping[name] = handler

        id = None
        try:
            (method, args, kwargs, id) = json.parse_jsonrpc_request(req.data)
            handler = self._mapping[method]
            json_data = {'version': '1.1', 'result': handler(req, *args, **kwargs)}
            if id is not None:
                json_data['id'] = id
        except DirectResponse, e:
            return e.args[0]
        except Exception, e:
            error = {'msg': str(e), 'type': e.__class__.__name__}
            for (name, ref) in e.__dict__.iteritems():
                if not name.startswith('_') and isinstance(ref, (str, unicode, int, float, tuple, list, dict)):
                    error[name] = ref

            json_data = {'version': '1.1', 'error': {'name': 'JSONRPCError', 'code': 0, 'message': 'An error occurred parsing the request object.', 'error': error}}
            if id is not None:
                json_data['id'] = id

        return Response(json.dumps(json_data), [
         ('Content-Type', 'text/javascript')])


def export(name):
    """
    Exports a function in a RemoteCallable component.
    """

    def wrapped(f):
        f.rpc_exported = True
        f.rpc_name = name
        return f

    return wrapped