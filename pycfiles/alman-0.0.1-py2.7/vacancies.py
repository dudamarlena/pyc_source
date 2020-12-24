# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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