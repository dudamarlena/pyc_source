# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/resources/vacancy.py
# Compiled at: 2015-08-31 22:18:14
from ..apibits import *

class Vacancy(ApiResource):

    @classmethod
    def retrieve(cls, vacancy_id, params={}, headers={}):
        res = cls.default_client().vacancies().retrieve(vacancy_id, params, headers)
        return res

    def refresh(self, params={}, headers={}):
        res = self.get_client().vacancies().retrieve(self.id, params, headers)
        return self.refresh_from(res.json, res.api_method, res.client)

    def delete(self, params={}, headers={}):
        res = self.get_client().vacancies().delete(self.id, params, headers)
        return self.refresh_from(res.json, res.api_method, res.client)

    def bookings(self):
        from ..endpoints import VacancyBookingsEndpoint
        return VacancyBookingsEndpoint(self.client, self)

    def __init__(self, *args, **kwargs):
        super(Vacancy, self).__init__(*args, **kwargs)
        ApiResource.register_api_subclass(self, 'vacancy')

    _api_attributes = {'created_at': {}, 'created_at_rfc822': {}, 'end_at': {}, 'end_at_rfc822': {}, 'id': {}, 'object': {}, 'start_at': {}, 'start_at_rfc822': {}, 'updated_at': {}, 'updated_at_rfc822': {}}