# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnbackus/Dropbox/coding/blockscore/blockscore-python/blockscore/http_client/__init__.py
# Compiled at: 2015-03-04 21:31:22
import requests, copy
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from blockscore.error import BlockscoreError
from blockscore.http_client.auth_handler import AuthHandler
from blockscore.http_client.error_handler import ErrorHandler
from blockscore.http_client.request_handler import RequestHandler
from blockscore.http_client.response import Response
from blockscore.http_client.response_handler import ResponseHandler

class HttpClient:

    def __init__(self, auth, options):
        self.options = {'base': 'https://api.blockscore.com/', 
           'user_agent': 'blockscore-python/4.0.0 (https://github.com/BlockScore/blockscore-python)'}
        self.options.update(options)
        self.base = self.options['base']
        self.headers = {'Accept': 'application/vnd.blockscore+json;version=4', 
           'user-agent': self.options['user_agent']}
        if 'headers' in self.options:
            self.headers.update(self.dict_key_lower(self.options['headers']))
            del self.options['headers']
        self.auth = AuthHandler(auth)

    def get(self, path, params={}, options={}):
        options.update({'query': params})
        return self.request(path, None, 'get', options)

    def post(self, path, body={}, options={}):
        return self.request(path, body, 'post', options)

    def patch(self, path, body={}, options={}):
        return self.request(path, body, 'patch', options)

    def delete(self, path, body={}, options={}):
        return self.request(path, body, 'delete', options)

    def put(self, path, body={}, options={}):
        return self.request(path, body, 'put', options)

    def request(self, path, body, method, options):
        kwargs = copy.deepcopy(self.options)
        kwargs.update(options)
        kwargs['headers'] = copy.deepcopy(self.headers)
        if 'headers' in options:
            kwargs['headers'].update(self.dict_key_lower(options['headers']))
        kwargs['data'] = body
        kwargs['allow_redirects'] = True
        kwargs['params'] = kwargs['query'] if 'query' in kwargs else {}
        if 'query' in kwargs:
            del kwargs['query']
        if 'body' in kwargs:
            del kwargs['body']
        del kwargs['base']
        del kwargs['user_agent']
        kwargs['verify'] = True
        if method != 'get':
            kwargs = self.set_body(kwargs)
        kwargs['hooks'] = dict(response=ErrorHandler().check_error)
        kwargs = self.auth.set(kwargs)
        response = self.create_request(method, path, kwargs)
        return Response(self.get_body(response), response.status_code, response.headers)

    def create_request(self, method, path, options):
        version = '/' + options['api_version'] if 'api_version' in options else ''
        path = urlparse.urljoin(self.base, version + path)
        if 'api_version' in options:
            del options['api_version']
        if 'response_type' in options:
            del options['response_type']
        try:
            response = requests.request(method, path, **options)
        except BlockscoreError:
            raise

        return response

    def get_body(self, response):
        return ResponseHandler.get_body(response)

    def set_body(self, request):
        return RequestHandler.set_body(request)

    def dict_key_lower(self, dic):
        return dict(zip(map(self.key_lower, dic.keys()), dic.values()))

    def key_lower(self, key):
        return key.lower()