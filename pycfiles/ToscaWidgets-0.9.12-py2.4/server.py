# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tw\core\server.py
# Compiled at: 2010-07-25 06:35:38
from inspect import isclass
from textwrap import dedent
import webob, tw
from tw.core.resources import registry

def authorize_callback(callback, request):
    widget = callback.im_self
    if widget.callback_authorization is not None:
        return widget.callback_authorization(callback, request)
    return tw.framework.middleware.callback_security_default(callback, request)


def serverside_callback(method):
    method.is_callback = True
    method.authorization = authorize_callback
    return method


resource_prefix = registry.prefix.lstrip('/')

class ServerSideCallbackMixin(object):
    __module__ = __name__
    params = dict(callback_authorization=dedent('\n    The WSGI-app that is used to check if\n    the current request is authorized to proceed to\n    the actual callback.\n\n    The wsgi-app has to have the signature\n\n      (callback, `webob.Request`) -> `webob.Response`\n\n    The callback is passed in to enable a different response\n    based on the callback in question.\n    '))
    callback_authorization = None

    def post_init(self, *args, **kwargs):
        for (name, value) in self.__class__.__dict__.iteritems():
            try:
                value.is_callback
            except AttributeError:
                pass
            else:
                registry.register_callback(getattr(self, value.func_name))

    def url_for_callback(self, callback):
        prefix = tw.framework.middleware.prefix
        script_name = tw.framework.script_name
        return ('/').join([script_name + prefix, resource_prefix, registry.path_for_callback(callback)])


def always_deny(callback, request):
    response = webob.Response()
    response.status = 403
    return response


def always_allow(callback, request):
    response = webob.Response()
    response.status = 200
    return response