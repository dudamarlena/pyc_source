# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jsonrpcdjango/__init__.py
# Compiled at: 2015-04-08 11:58:06
# Size of source mod 2**32: 945 bytes
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
try:
    from django.views.generic import View
except ImportError:
    pass
else:

    class RpcServerView(View):
        server_instance = None

        def __init__(self, *args, **kw):
            (super(RpcServerView, self).__init__)(*args, **kw)
            self._rpc_server = self.server_instance

        def post(self, request):
            result = self._rpc_server.handle_http_request(request)
            return HttpResponse(result)

        @method_decorator(csrf_exempt)
        def dispatch(self, *args, **kwargs):
            return (super(RpcServerView, self).dispatch)(*args, **kwargs)


def csrf_serve(request, service):
    result = service.handle_http_request(request)
    return HttpResponse(result)


@csrf_exempt
def serve(request, service):
    return csrf_serve(request, service)