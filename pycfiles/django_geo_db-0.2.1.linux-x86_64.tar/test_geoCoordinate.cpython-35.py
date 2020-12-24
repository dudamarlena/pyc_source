# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/tests/test_geoCoordinate.py
# Compiled at: 2018-02-04 15:10:23
# Size of source mod 2**32: 5917 bytes
from unittest import TestCase
from django_geo_db.models import GeoCoordinate

class TestGeoCoordinate(TestCase):

    def test_split_lat_coordinate_1(self):
        value = '12.34567'
        n, a, b, c, d, e, f, g = GeoCoordinate.split_lat_coordinate(value)
        self.assertEqual(n, False)
        self.assertEqual(a, 1)
        self.assertEqual(b, 2)
        self.assertEqual(c, 3)
        self.assertEqual(d, 4)
        self.assertEqual(e, 5)
        self.assertEqual(f, 6)
        self.assertEqual(g, 7)

    def test_split_lat_coordinate_2(self):
        value = '-12.34567'
        n, a, b, c, d, e, f, g = GeoCoordinate.split_lat_coordinate(value)
        self.assertEqual(n, True)
        self.assertEqual(a, 1)
        self.assertEqual(b, 2)
        self.assertEqual(c, 3)
        self.assertEqual(d, 4)
        self.assertEqual(e, 5)
        self.assertEqual(f, 6)
        self.assertEqual(g, 7)

    def test_split_lat_coordinate_3(self):
        value = '-2.34567'
        n, a, b, c, d, e, f, g = GeoCoordinate.split_lat_coordinate(value)
        self.assertEqual(n, True)
        self.assertEqual(a, 0)
        self.assertEqual(b, 2)
        self.assertEqual(c, 3)
        self.assertEqual(d, 4)
        self.assertEqual(e, 5)
        self.assertEqual(f, 6)
        self.assertEqual(g, 7)

    def test_split_lat_coordinate_4(self):
        value = '2.34567'
        n, a, b, c, d, e, f, g = GeoCoordinate.split_lat_coordinate(value)
        self.assertEqual(n, False)
        self.assertEqual(a, 0)
        self.assertEqual(b, 2)
        self.assertEqual(c, 3)
        self.assertEqual(d, 4)
        self.assertEqual(e, 5)
        self.assertEqual(f, 6)
        self.assertEqual(g, 7)

    def test_split_lat_coordinate_5(self):
        value = '-0.34567'
        n, a, b, c, d, e, f, g = GeoCoordinate.split_lat_coordinate(value)
        self.assertEqual(n, True)
        self.assertEqual(a, 0)
        self.assertEqual(b, 0)
        self.assertEqual(c, 3)
        self.assertEqual(d, 4)
        self.assertEqual(e, 5)
        self.assertEqual(f, 6)
        self.assertEqual(g, 7)

    def test_split_lat_coordinate_6(self):
        value = '0.34567'
        n, a, b, c, d, e, f, g = GeoCoordinate.split_lat_coordinate(value)
        self.assertEqual(n, False)
        self.assertEqual(a, 0)
        self.assertEqual(b, 0)
        self.assertEqual(c, 3)
        self.assertEqual(d, 4)
        self.assertEqual(e, 5)
        self.assertEqual(f, 6)
        self.assertEqual(g, 7)

    def test_split_lat_coordinate_7(self):
        value = '0.04567'
        n, a, b, c, d, e, f, g = GeoCoordinate.split_lat_coordinate(value)
        self.assertEqual(n, False)
        self.assertEqual(a, 0)
        self.assertEqual(b, 0)
        self.assertEqual(c, 0)
        self.assertEqual(d, 4)
        self.assertEqual(e, 5)
        self.assertEqual(f, 6)
        self.assertEqual(g, 7)

    def test_split_lon_coordinate_1(self):
        value = '123.45678'
        n, a, b, c, d, e, f, g, h = GeoCoordinate.split_lon_coordinate(value)
        self.assertEqual(n, False)
        self.assertEqual(a, 1)
        self.assertEqual(b, 2)
        self.assertEqual(c, 3)
        self.assertEqual(d, 4)
        self.assertEqual(e, 5)
        self.assertEqual(f, 6)
        self.assertEqual(g, 7)
        self.assertEqual(h, 8)

    def test_split_lon_coordinate_2(self):
        value = '-123.45678'
        n, a, b, c, d, e, f, g, h = GeoCoordinate.split_lon_coordinate(value)
        self.assertEqual(n, True)
        self.assertEqual(a, 1)
        self.assertEqual(b, 2)
        self.assertEqual(c, 3)
        self.assertEqual(d, 4)
        self.assertEqual(e, 5)
        self.assertEqual(f, 6)
        self.assertEqual(g, 7)
        self.assertEqual(h, 8)

    def test_split_lon_coordinate_3(self):
        value = '-23.45678'
        n, a, b, c, d, e, f, g, h = GeoCoordinate.split_lon_coordinate(value)
        self.assertEqual(n, True)
        self.assertEqual(a, 0)
        self.assertEqual(b, 2)
        self.assertEqual(c, 3)
        self.assertEqual(d, 4)
        self.assertEqual(e, 5)
        self.assertEqual(f, 6)
        self.assertEqual(g, 7)
        self.assertEqual(h, 8)

    def test_split_lon_coordinate_4(self):
        value = '23.45678'
        n, a, b, c, d, e, f, g, h = GeoCoordinate.split_lon_coordinate(value)
        self.assertEqual(n, False)
        self.assertEqual(a, 0)
        self.assertEqual(b, 2)
        self.assertEqual(c, 3)
        self.assertEqual(d, 4)
        self.assertEqual(e, 5)
        self.assertEqual(f, 6)
        self.assertEqual(g, 7)
        self.assertEqual(h, 8)

    def test_split_lon_coordinate_5(self):
        value = '-3.45678'
        n, a, b, c, d, e, f, g, h = GeoCoordinate.split_lon_coordinate(value)
        self.assertEqual(n, True)
        self.assertEqual(a, 0)
        self.assertEqual(b, 0)
        self.assertEqual(c, 3)
        self.assertEqual(d, 4)
        self.assertEqual(e, 5)
        self.assertEqual(f, 6)
        self.assertEqual(g, 7)
        self.assertEqual(h, 8)

    def test_split_lon_coordinate_6(self):
        value = '0.34567'
        n, a, b, c, d, e, f, g, h = GeoCoordinate.split_lon_coordinate(value)
        self.assertEqual(n, False)
        self.assertEqual(a, 0)
        self.assertEqual(b, 0)
        self.assertEqual(c, 0)
        self.assertEqual(d, 3)
        self.assertEqual(e, 4)
        self.assertEqual(f, 5)
        self.assertEqual(g, 6)
        self.assertEqual(h, 7)

    def test_split_lon_coordinate_7(self):
        value = '0.04567'
        n, a, b, c, d, e, f, g, h = GeoCoordinate.split_lon_coordinate(value)
        self.assertEqual(n, False)
        self.assertEqual(a, 0)
        self.assertEqual(b, 0)
        self.assertEqual(c, 0)
        self.assertEqual(d, 0)
        self.assertEqual(e, 4)
        self.assertEqual(f, 5)
        self.assertEqual(g, 6)
        self.assertEqual(h, 7)