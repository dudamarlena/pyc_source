# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/resources/booking.py
# Compiled at: 2015-08-31 22:18:14
from ..apibits import *

class Booking(ApiResource):

    @classmethod
    def all(cls, params={}, headers={}):
        res = cls.default_client().bookings().all(params, headers)
        return res

    @classmethod
    def retrieve(cls, booking_id, params={}, headers={}):
        res = cls.default_client().bookings().retrieve(booking_id, params, headers)
        return res

    @classmethod
    def update(cls, booking_id, params={}, headers={}):
        res = cls.default_client().bookings().update(booking_id, params, headers)
        return res

    def refresh(self, params={}, headers={}):
        res = self.get_client().bookings().retrieve(self.id, params, headers)
        return self.refresh_from(res.json, res.api_method, res.client)

    def delete(self, params={}, headers={}):
        res = self.get_client().bookings().delete(self.id, params, headers)
        return self.refresh_from(res.json, res.api_method, res.client)

    def __init__(self, *args, **kwargs):
        super(Booking, self).__init__(*args, **kwargs)
        ApiResource.register_api_subclass(self, 'booking')

    _api_attributes = {'created_at': {}, 'created_at_rfc822': {}, 'end_at': {}, 'end_at_rfc822': {}, 'id': {}, 'meta': {}, 'object': {}, 'start_at': {}, 'start_at_rfc822': {}, 'updated_at': {}, 'updated_at_rfc822': {}}