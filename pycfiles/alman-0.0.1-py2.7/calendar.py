# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/resources/calendar.py
# Compiled at: 2015-08-31 22:18:14
from ..apibits import *

class Calendar(ApiResource):

    @classmethod
    def all(cls, params={}, headers={}):
        res = cls.default_client().calendars().all(params, headers)
        return res

    @classmethod
    def retrieve(cls, calendar_id, params={}, headers={}):
        res = cls.default_client().calendars().retrieve(calendar_id, params, headers)
        return res

    @classmethod
    def update(cls, calendar_id, params={}, headers={}):
        res = cls.default_client().calendars().update(calendar_id, params, headers)
        return res

    @classmethod
    def create(cls, params={}, headers={}):
        res = cls.default_client().calendars().create(params, headers)
        return res

    def refresh(self, params={}, headers={}):
        res = self.get_client().calendars().retrieve(self.id, params, headers)
        return self.refresh_from(res.json, res.api_method, res.client)

    def delete(self, params={}, headers={}):
        res = self.get_client().calendars().delete(self.id, params, headers)
        return self.refresh_from(res.json, res.api_method, res.client)

    def vacancies(self):
        from ..endpoints import CalendarVacanciesEndpoint
        return CalendarVacanciesEndpoint(self.client, self)

    def __init__(self, *args, **kwargs):
        super(Calendar, self).__init__(*args, **kwargs)
        ApiResource.register_api_subclass(self, 'calendar')

    _api_attributes = {'created_at': {}, 'created_at_rfc822': {}, 'details': {}, 'id': {}, 'name': {}, 'object': {}, 'updated_at': {}, 'updated_at_rfc822': {}}