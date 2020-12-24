# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pycrunchbase/resource/address.py
# Compiled at: 2017-01-13 23:45:16
import six
from .node import Node

@six.python_2_unicode_compatible
class Address(Node):
    """Represents a Address on CrunchBase"""
    KNOWN_PROPERTIES = [
     'name',
     'street_1',
     'street_2',
     'postal_code',
     'city',
     'city_path',
     'city_web_path',
     'region',
     'region_path',
     'region_web_path',
     'country',
     'country_path',
     'country_web_path',
     'latitude',
     'longitude',
     'created_at',
     'updated_at']

    def _coerce_values(self):
        for attr in ['latitude', 'longitude']:
            if getattr(self, attr, None):
                setattr(self, attr, float(getattr(self, attr)))

        return

    def __str__(self):
        return ('{name} {street_1}').format(name=self.name, street_1=self.street_1)

    def __repr__(self):
        return self.__str__()