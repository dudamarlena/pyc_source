# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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