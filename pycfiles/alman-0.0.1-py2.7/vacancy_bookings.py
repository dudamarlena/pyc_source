# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/endpoints/vacancy_bookings.py
# Compiled at: 2015-08-31 22:18:14
from ..apibits import *
from ..resources import *

class VacancyBookingsEndpoint(ApiEndpoint):

    def create(self, params={}, headers={}):
        method = ApiMethod('post', '/vacancies/:id/bookings', params, headers, self.parent)
        json = self.client.execute(method)
        return Booking(json, method, client=self.client)