# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/webapptitude/application.py
# Compiled at: 2016-08-31 16:32:16
import os, webapp2, logging
from webapp2 import exc as exceptions
from handlers import patch_request, patch_response
from decorator import is_dev_server
try:
    from appengine_config import config as site_config
except ImportError:
    site_config = {}

logging.getLogger().setLevel(logging.INFO)

class SaneRouter(webapp2.Router):

    def dispatch(self, request, response):
        request = patch_request(request)
        response = patch_response(response)
        result = super(SaneRouter, self).dispatch(request, response)
        if isinstance(result, webapp2.Response):
            response = result
        return response


class WSGIApplication(webapp2.WSGIApplication, object):
    debug = False
    router_class = SaneRouter

    @webapp2.cached_property
    def dev_appserver(self):
        return is_dev_server()

    @webapp2.cached_property
    def logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(self.debug and logging.DEBUG or logging.INFO)
        logger.addHandler(logging.StreamHandler())
        return logger

    @classmethod
    def accept_http_method(cls, *methods):
        """Allow the request to handle additional HTTP methods."""
        cls.allowed_methods = cls.allowed_methods.union(methods)

    def __init__(self, *args, **kwargs):
        insert_static_route = os.environ.get('STATIC_ROUTE', None)
        config = {}
        config.update(site_config)
        config.update(kwargs.pop('config', {}))
        kwargs['config'] = config
        if 'debug' not in kwargs:
            kwargs['debug'] = self.dev_appserver
        self.debug = kwargs.get('debug', False)
        super(WSGIApplication, self).__init__(*args, **kwargs)
        if insert_static_route:
            self.router.add(webapp2.Route(insert_static_route, handler=webapp2.RequestHandler, name='static'))
        return

    def route(self, path_expr, *args, **options):
        """Construct and attach a new request handler, with route path."""

        def __handler(handler_cls):
            route = webapp2.Route(path_expr, handler_cls, *args, **options)
            self.router.add(route)
            return handler_cls

        if len(args) and issubclass(args[0], webapp2.RequestHandler):
            handler = args[0]
            args = args[1:]
            return __handler(handler)
        else:
            return __handler

    def build(self, request, name, args=[], kwargs={}):
        """Build a URL based on a named route."""
        assert isinstance(request, webapp2.Request)
        return self.router.build(request, name, args, kwargs)


WSGIApplication.accept_http_method('PATCH', 'HEAD', 'TRACE')