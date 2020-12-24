# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robb/src/adapters-python/venv/lib/python3.4/site-packages/eaternet/lives_1_0/entities.py
# Compiled at: 2015-08-06 01:02:35
# Size of source mod 2**32: 1498 bytes
import datetime
from eaternet.lives_1_0.validated_object import ValidatedObject

class Business(ValidatedObject):
    __doc__ = '\n    A Lives 1.0 Business\n    Specified at http://www.yelp.com/healthscores#businesses\n    '

    def __init__(self, business_id, name, address, city=None, state=None, postal_code=None, latitude=None, longitude=None, phone_number=None):
        self.required(business_id, 'business_id', str).required(name, 'name', str).required(address, 'address', str).optional(latitude, 'latitude', float, minimum=-90, maximum=90).optional(longitude, 'longitude', float, minimum=-180, maximum=180).optional(phone_number, 'phone_number', str).optional(city, 'city', str).optional(state, 'state', str).optional(postal_code, 'postal_code', str)
        self.validate()


class Inspection(ValidatedObject):
    __doc__ = '\n    A Lives 1.0 Inspection\n    See http://www.yelp.com/healthscores#inspections\n    '

    def __init__(self, business_id, date, score=None, description=None, inspection_type=None):
        self.optional(inspection_type, 'inspection_type', str, inclusion_in=('initial',
                                                                             'routine',
                                                                             'followup',
                                                                             'complaint')).optional(score, 'score', int, minimum=0, maximum=100).optional(description, 'description', str).required(business_id, 'business_id', str).required(date, 'date', datetime.date)
        self.validate()