# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/endpoints/bookings.py
# Compiled at: 2015-08-31 22:18:14
from ..apibits import *
from ..resources import *

class BookingsEndpoint(ApiEndpoint):

    def retrieve(self, booking_id, params={}, headers={}):
        params = ParamsBuilder.merge({'booking_id': booking_id}, params)
        method = ApiMethod('get', '/bookings/:booking_id', params, headers, self.parent)
        json = self.client.execute(method)
        return Booking(json, method, client=self.client)

    def delete(self, booking_id, params={}, headers={}):
        params = ParamsBuilder.merge({'booking_id': booking_id}, params)
        method = ApiMethod('delete', '/bookings/:booking_id', params, headers, self.parent)
        json = self.client.execute(method)
        return Booking(json, method, client=self.client)

    def update(self, booking_id, params={}, headers={}):
        params = ParamsBuilder.merge({'booking_id': booking_id}, params)
        method = ApiMethod('put', '/bookings/:booking_id', params, headers, self.parent)
        json = self.client.execute(method)
        return Booking(json, method, client=self.client)