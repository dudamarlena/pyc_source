# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/das-g/hsr/dev/osmaxx/drf-utm-zone-info/utm_zone_info/coordinate_reference_system.py
# Compiled at: 2017-01-12 05:40:31
# Size of source mod 2**32: 3721 bytes
from django.contrib.gis.geos.collections import MultiPolygon
from django.contrib.gis.geos.polygon import Polygon
WGS_84 = 4326
MIN_LONGITUDE_DEGREES = -180
MAX_LONGITUDE_DEGREES = 180

class UTMZone(object):
    __doc__ = '\n    Universal Transverse Mercator (UTM) zone\n    '
    HEMISPHERE_PREFIXES = dict(north=326, south=327)
    NUMBER_OF_ZONES_PER_HEMISPHERE = 60
    VALID_ZONE_NUMBERS = range(1, NUMBER_OF_ZONES_PER_HEMISPHERE + 1)
    ZONE_WIDTH_DEGREES = 360 / NUMBER_OF_ZONES_PER_HEMISPHERE
    MAX_LONGITUDE_OFFSET = 89.9999999999999

    def __init__(self, hemisphere, utm_zone_number):
        assert hemisphere in self.HEMISPHERE_PREFIXES
        assert utm_zone_number in self.VALID_ZONE_NUMBERS
        self.hemisphere = hemisphere
        self.utm_zone_number = utm_zone_number
        self._prepared_domain = None

    def can_represent(self, geom):
        return self.domain.covers(geom.transform(WGS_84, clone=True))

    @property
    def domain(self):
        if self._prepared_domain is None:
            self._prepared_domain = self._computed_domain.prepared
        return self._prepared_domain

    @property
    def _computed_domain(self):
        xmin, ymin, xmax, ymax = (
         wrap_longitude_degrees(self.central_meridian_longitude_degrees - self.MAX_LONGITUDE_OFFSET),
         -90,
         wrap_longitude_degrees(self.central_meridian_longitude_degrees + self.MAX_LONGITUDE_OFFSET),
         90)
        if xmin <= xmax:
            domain = Polygon.from_bbox((xmin, ymin, xmax, ymax))
            domain.srid = WGS_84
            return domain
        else:
            return MultiPolygon(Polygon.from_bbox((xmin, ymin, MAX_LONGITUDE_DEGREES, ymax)), Polygon.from_bbox((MIN_LONGITUDE_DEGREES, ymin, xmax, ymax)), srid=WGS_84)

    @property
    def srid(self):
        return self.HEMISPHERE_PREFIXES[self.hemisphere] * 100 + self.utm_zone_number

    @property
    def central_meridian_longitude_degrees(self):
        return MIN_LONGITUDE_DEGREES + (self.utm_zone_number - 0.5) * self.ZONE_WIDTH_DEGREES

    def __eq__(self, other):
        return (
         self.hemisphere, self.utm_zone_number == other.hemisphere, other.utm_zone_number)

    def __hash__(self):
        return hash((self.hemisphere, self.utm_zone_number))

    def __str__(self):
        return 'UTM Zone {zone_number}, {hemisphere}ern hemisphere'.format(zone_number=self.utm_zone_number, hemisphere=self.hemisphere)

    def __repr__(self):
        return '{cls}({hemisphere}, {zone_number})'.format(cls=type(self).__name__, zone_number=self.utm_zone_number, hemisphere=repr(self.hemisphere))


UTM_ZONE_NUMBERS = UTMZone.VALID_ZONE_NUMBERS
ALL_UTM_ZONES = frozenset(UTMZone(hs, nr) for hs in UTMZone.HEMISPHERE_PREFIXES for nr in UTM_ZONE_NUMBERS)

def utm_zones_for_representing(geom):
    return frozenset(zone for zone in ALL_UTM_ZONES if zone.can_represent(geom))


def wrap_longitude_degrees(longitude_degrees):
    return confine(longitude_degrees, MIN_LONGITUDE_DEGREES, MAX_LONGITUDE_DEGREES)


def confine(value, lower_bound, upper_bound):
    modulus = upper_bound - lower_bound
    result = (value - lower_bound) % modulus + lower_bound
    assert lower_bound <= result <= upper_bound
    return result