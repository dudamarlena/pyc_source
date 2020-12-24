# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/endpoints/vacancies.py
# Compiled at: 2015-08-31 22:18:14
from ..apibits import *
from ..resources import *

class VacanciesEndpoint(ApiEndpoint):

    def retrieve(self, vacancy_id, params={}, headers={}):
        params = ParamsBuilder.merge({'vacancy_id': vacancy_id}, params)
        method = ApiMethod('get', '/vacancies/:vacancy_id', params, headers, self.parent)
        json = self.client.execute(method)
        return Vacancy(json, method, client=self.client)

    def delete(self, vacancy_id, params={}, headers={}):
        params = ParamsBuilder.merge({'vacancy_id': vacancy_id}, params)
        method = ApiMethod('delete', '/vacancies/:vacancy_id', params, headers, self.parent)
        json = self.client.execute(method)
        return Vacancy(json, method, client=self.client)