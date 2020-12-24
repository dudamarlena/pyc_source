# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/endpoints/calendar_vacancies.py
# Compiled at: 2015-08-31 22:18:14
from ..apibits import *
from ..resources import *

class CalendarVacanciesEndpoint(ApiEndpoint):

    def all(self, params={}, headers={}):
        method = ApiMethod('get', '/calendars/:id/vacancies', params, headers, self.parent)
        json = self.client.execute(method)
        return ApiList(Vacancy, json, method, client=self.client)

    def all_within(self, params={}, headers={}):
        method = ApiMethod('get', '/calendars/:id/vacancies/within', params, headers, self.parent)
        json = self.client.execute(method)
        return ApiList(Vacancy, json, method, client=self.client)

    def create(self, params={}, headers={}):
        method = ApiMethod('post', '/calendars/:id/vacancies', params, headers, self.parent)
        json = self.client.execute(method)
        return Vacancy(json, method, client=self.client)

    def create_range(self, params={}, headers={}):
        method = ApiMethod('post', '/calendars/:id/vacancies/range', params, headers, self.parent)
        json = self.client.execute(method)
        return ApiList(Vacancy, json, method, client=self.client)

    def delete_overlap(self, params={}, headers={}):
        method = ApiMethod('delete', '/calendars/:id/vacancies/overlap', params, headers, self.parent)
        json = self.client.execute(method)
        return ApiList(Vacancy, json, method, client=self.client)