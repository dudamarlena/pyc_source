# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/intellexer/core/request_handler.py
# Compiled at: 2019-04-16 12:33:47
# Size of source mod 2**32: 1801 bytes
"""
*docstring*
"""
import os, urllib, urllib3
from . import response_builders
from . import response_wrapper

class BaseRequest:
    __doc__ = '\n\t*docstring*\n\t'
    __slots__ = ('_api_key', '_server', '_builder')
    http = urllib3.PoolManager()

    def __init__(self, api_key=None, server=None):
        api_key = api_key or os.environ['INTELLEXER_API_KEY']
        server = server or os.getenv('INTELLEXER_SERVER', 'http://api.intellexer.com')
        self._api_key = api_key
        self._server = server.rstrip('/')
        builder_function = response_builders.builders[self.json]
        self._builder = builder_function(self.builder)

    def __url(self, path):
        return '/'.join((
         self._server,
         path))

    def __fields(self, fields):
        fields.update({'apikey': self._api_key})
        return fields

    @classmethod
    def from_raw(cls, raw_data):
        builder_function = response_builders.builders[cls.json]
        response_builder = builder_function(cls.builder)
        return response_wrapper.Response(response_builder=response_builder, response=raw_data)

    def __response_handler(self, response):
        return response_wrapper.Response(response_builder=self._builder, request_functin=response)

    def _get(self, path, fields, headers=None):
        response = lambda : self.http.request(method='GET', url=self._BaseRequest__url(path), fields=self._BaseRequest__fields(fields), preload_content=False, headers=headers)
        return self._BaseRequest__response_handler(response)

    def _post(self, path, fields, body, headers=None):
        url = self._BaseRequest__url(path)
        fields = self._BaseRequest__fields(fields)
        if fields:
            url += '?' + urllib.parse.urlencode(fields)
        response = lambda : self.http.request(method='POST', url=url, body=body, preload_content=False, headers=headers)
        return self._BaseRequest__response_handler(response)