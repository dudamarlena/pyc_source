# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/tomchristie/GitHub/api-star/api_star/frameworks/flask/app.py
# Compiled at: 2016-04-13 15:50:03
# Size of source mod 2**32: 4496 bytes
from __future__ import unicode_literals
from flask import request, Flask
from api_star.core import check_permissions
from api_star.exceptions import APIException
from api_star.frameworks.flask.request import APIRequest
from api_star.frameworks.flask.response import APIResponse
from api_star.schema import get_link
from werkzeug.exceptions import HTTPException
from werkzeug.routing import parse_rule
import coreapi

def _rule_to_url(rule):
    """
    Given a werkzeug rule, return a URITemplate URL.
    """
    url = ''
    for converter, arguments, variable in parse_rule(rule):
        if converter is None:
            url += variable
        else:
            url += '{' + variable + '}'

    return url


class App(Flask):
    request_class = APIRequest
    response_class = APIResponse

    def __init__(self, module=None, **kwargs):
        self.links = {}
        self.title = kwargs.pop('title', None)
        self.parsers = kwargs.pop('parsers', None)
        self.renderers = kwargs.pop('renderers', None)
        self.authenticators = kwargs.pop('authenticators', None)
        self.permissions = kwargs.pop('permissions', None)
        super(App, self).__init__(module, **kwargs)

    def dispatch_request(self):
        try:
            return super(App, self).dispatch_request()
        finally:
            request.renderer

    def handle_user_exception(self, e):
        if isinstance(e, APIException):
            return self.handle_http_exception(e)
        return super(App, self).handle_user_exception(e)

    def handle_http_exception(self, e):
        ret = super(App, self).handle_http_exception(e)
        if isinstance(ret, (HTTPException, APIException)):
            return APIResponse({'message': e.description}, status=e.code)
        return ret

    def get(self, url, **options):
        return self.api_route(url, 'GET', **options)

    def post(self, url, **options):
        return self.api_route(url, 'POST', **options)

    def put(self, url, **options):
        return self.api_route(url, 'PUT', **options)

    def patch(self, url, **options):
        return self.api_route(url, 'PATCH', **options)

    def delete(self, url, **options):
        return self.api_route(url, 'DELETE', **options)

    def api_route(self, rule, method, **options):
        tag = options.pop('tag', None)
        exclude_from_schema = options.pop('exclude_from_schema', False)
        renderers = options.pop('renderers', self.renderers)
        parsers = options.pop('parsers', self.parsers)
        authenticators = options.pop('authenticators', self.authenticators)
        permissions = options.pop('permissions', self.permissions)

        def decorator(func):
            endpoint = options.pop('endpoint', func.__name__)
            url = _rule_to_url(rule)
            func.link = get_link(url, method, func)
            if not exclude_from_schema:
                if tag:
                    if tag not in self.links:
                        self.links[tag] = {}
                    self.links[tag][endpoint] = func.link
                else:
                    self.links[endpoint] = func.link
                self.schema = coreapi.Document(title=self.title, content=self.links)

            def wrapper(**params):
                for field in func.link.fields:
                    if field.location == 'form':
                        if field.name in request.data:
                            params[field.name] = request.data[field.name]
                    elif field.location == 'query':
                        if field.name in request.args:
                            params[field.name] = request.args[field.name]
                    elif field.location == 'body':
                        params[field.name] = request.data
                        continue

                if renderers is not None:
                    request.renderers = renderers
                if parsers is not None:
                    request.parsers = parsers
                if authenticators is not None:
                    request.authenticators = authenticators
                if permissions is not None:
                    check_permissions(request, permissions)
                return func(**params)

            self.add_url_rule(rule, endpoint, wrapper, methods=[method], **options)
            return func

        return decorator