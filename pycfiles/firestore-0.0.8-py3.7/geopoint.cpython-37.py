# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/firestore/datatypes/geopoint.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 1402 bytes
from firestore.datatypes.base import Base
MAX_LATITUDE = 90.0
MIN_LATITUDE = -90.0
MAX_LONGITUDE = MAX_LATITUDE * 2
MIN_LONGITUDE = MIN_LATITUDE * 2

class Geopoint(Base):
    __doc__ = '\n    Geographic coordinates\n\n    Organised by latitude, then longitude\n    '

    def __init__(self, *args, **kwargs):
        default = kwargs.get('default')
        self.py_type = tuple
        if default:
            self.validate(default)
        (super(Geopoint, self).__init__)(*args, **kwargs)

    def validate(self, value, instance=None):
        if not isinstance(value, (list, tuple)):
            raise ValueError('Unsupported value assigned to Geopoint - only list, tuple supported')
        if len(value) != 2:
            raise ValueError('Geopoint requires exactly two values for latitude and longitude')
        latitude, longitude = value
        if not isinstance(latitude, (int, float)) or latitude < MIN_LATITUDE or latitude > MAX_LATITUDE:
            raise ValueError(f"Invalid latitude value {latitude} detected")
        if not isinstance(longitude, (int, float)) or longitude < MIN_LONGITUDE or longitude > MAX_LONGITUDE:
            raise ValueError('Invalid longitude value detected')
        self.latitude, self.longitude = value