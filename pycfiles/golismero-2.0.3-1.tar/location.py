# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/geopy/location.py
# Compiled at: 2013-10-14 11:27:57
from geopy.point import Point

class Location(object):

    def __init__(self, name='', point=None, attributes=None, **kwargs):
        self.name = name
        if point is not None:
            self.point = Point(point)
        if attributes is None:
            attributes = {}
        self.attributes = dict(attributes, **kwargs)
        return

    def __getitem__(self, index):
        """Backwards compatibility with geopy 0.93 tuples."""
        return (
         self.name, self.point)[index]

    def __repr__(self):
        return 'Location(%r, %r)' % (self.name, self.point)

    def __iter__(self):
        return iter((self.name, self.point))

    def __eq__(self, other):
        return (
         self.name, self.point) == (other.name, other.point)

    def __ne__(self, other):
        return (
         self.name, self.point) != (other.name, other.point)