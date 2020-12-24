# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pycrunchbase/resource/location.py
# Compiled at: 2017-01-13 23:45:16
import six
from .node import Node

@six.python_2_unicode_compatible
class Location(Node):
    """Represents a Location on CrunchBase"""
    KNOWN_PROPERTIES = [
     'web_path',
     'name',
     'location_type',
     'parent_location_uuid',
     'created_at',
     'updated_at']
    KNOWN_RELATIONSHIPS = [
     'parent_locations']

    def __str__(self):
        return ('{name} {location_type}').format(name=self.name, location_type=self.location_type)

    def __repr__(self):
        return self.__str__()