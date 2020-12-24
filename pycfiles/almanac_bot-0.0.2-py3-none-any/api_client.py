# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/apibits/api_client.py
# Compiled at: 2015-08-31 22:18:13
from .params_builder import ParamsBuilder

class ApiClient(object):
    headers = {}
    params = {}

    def execute(self, api_method):
        api_method.headers = ParamsBuilder.merge(api_method.headers, self.headers)
        api_method.params = ParamsBuilder.merge(api_method.params, self.params)
        return api_method.execute()

    def refresh_from(self, headers, params):
        self.headers = headers
        self.params = params
        return self

    def __init__(self, headers, params):
        self.refresh_from(headers, params)