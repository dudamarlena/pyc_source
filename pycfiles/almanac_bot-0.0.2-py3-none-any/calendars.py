# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/endpoints/calendars.py
# Compiled at: 2015-08-31 22:18:14
from ..apibits import *
from ..resources import *

class CalendarsEndpoint(ApiEndpoint):

    def all(self, params={}, headers={}):
        method = ApiMethod('get', '/calendars', params, headers, self.parent)
        json = self.client.execute(method)
        return ApiList(Calendar, json, method, client=self.client)

    def retrieve(self, calendar_id, params={}, headers={}):
        params = ParamsBuilder.merge({'calendar_id': calendar_id}, params)
        method = ApiMethod('get', '/calendars/:calendar_id', params, headers, self.parent)
        json = self.client.execute(method)
        return Calendar(json, method, client=self.client)

    def delete(self, calendar_id, params={}, headers={}):
        params = ParamsBuilder.merge({'calendar_id': calendar_id}, params)
        method = ApiMethod('delete', '/calendars/:calendar_id', params, headers, self.parent)
        json = self.client.execute(method)
        return Calendar(json, method, client=self.client)

    def update(self, calendar_id, params={}, headers={}):
        params = ParamsBuilder.merge({'calendar_id': calendar_id}, params)
        method = ApiMethod('put', '/calendars/:calendar_id', params, headers, self.parent)
        json = self.client.execute(method)
        return Calendar(json, method, client=self.client)

    def create(self, params={}, headers={}):
        method = ApiMethod('post', '/calendars', params, headers, self.parent)
        json = self.client.execute(method)
        return Calendar(json, method, client=self.client)