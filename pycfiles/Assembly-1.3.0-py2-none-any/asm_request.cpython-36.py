# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Flasik/assembly/asm_request.py
# Compiled at: 2019-10-27 19:58:13
# Size of source mod 2**32: 3972 bytes
import inspect
from flask import request as f_request
from .core import _bind_route_rule_cache, extends
import flask_seasurf
csrf = flask_seasurf.SeaSurf()
extends(csrf.init_app)

class RequestProxy(object):
    __doc__ = '\n    A request proxy, that attaches some special attributes to the request object\n    '
    csrf_exempt = csrf.exempt

    @property
    def IS_GET(self):
        return f_request.method == 'GET'

    @property
    def IS_POST(cls):
        return f_request.method == 'POST'

    @property
    def IS_PUT(self):
        return f_request.method == 'PUT'

    @property
    def IS_DELETE(self):
        return f_request.method == 'DELETE'

    @classmethod
    def _accept_method(cls, methods, f):
        kw = {'append_method':True, 
         'methods':methods}
        _bind_route_rule_cache(f, rule=None, **kw)
        return f

    @classmethod
    def get(cls, f):
        """ decorator to accept GET method """
        return cls._accept_method(['GET'], f)

    @classmethod
    def post(cls, f):
        """ decorator to accept POST method """
        return cls._accept_method(['POST'], f)

    @classmethod
    def post_get(cls, f):
        """ decorator to accept POST & GET method """
        return cls._accept_method(['POST', 'GET'], f)

    @classmethod
    def delete(cls, f):
        """ decorator to accept DELETE method """
        return cls._accept_method(['DELETE'], f)

    @classmethod
    def put(cls, f):
        """ decorator to accept PUT method """
        return cls._accept_method(['PUT'], f)

    @classmethod
    def all(cls, f):
        """ decorator to accept ALL methods """
        return cls._accept_method(['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS', 'UPDATE'], f)

    @classmethod
    def options(cls, f):
        """ decorator to accept OPTIONS methods """
        return cls._accept_method(['OPTIONS'], f)

    @classmethod
    def route(cls, rule=None, **kwargs):
        """
        This decorator defines custom route for both class and methods in the view.
        It behaves the same way as Flask's @app.route
        on class:
            It takes the following args
                - rule: the root route of the endpoint
                - decorators: a list of decorators to run on each method
        on methods:
            along with the rule, it takes kwargs
                - endpoint
                - defaults
                - ...
        :param rule:
        :param kwargs:
        :return:
        """
        _restricted_keys = [
         'route', 'decorators']

        def decorator(f):
            if inspect.isclass(f):
                kwargs.setdefault('route', rule)
                kwargs['decorators'] = kwargs.get('decorators', []) + f.decorators
                setattr(f, '_route_extends__', kwargs)
                setattr(f, 'base_route', kwargs.get('route'))
                setattr(f, 'decorators', kwargs.get('decorators', []))
            else:
                if not rule:
                    raise ValueError("'rule' is missing in @route ")
                for k in _restricted_keys:
                    if k in kwargs:
                        del kwargs[k]

                _bind_route_rule_cache(f, rule=rule, **kwargs)
            return f

        return decorator

    def __getattr__(self, item):
        return getattr(f_request, item)

    @classmethod
    def get_auth_bearer(cls):
        """
        Return the authorization bearer
        :return: string
        """
        if 'Authorization' not in f_request.headers:
            raise ValueError('Missing Authorization Bearer in headers')
        data = f_request.headers['Authorization'].encode('ascii', 'ignore')
        return str.replace(str(data), 'Bearer ', '').strip()