# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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