# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ben/Code/python-census-batch-geocoder/censusbatchgeocoder/tests/__init__.py
# Compiled at: 2017-07-19 12:56:27
__doc__ = b'\nTests censusbatchgeocoder wrapper.\n'
from __future__ import unicode_literals
import io, os, six, unittest, censusbatchgeocoder

class GeocoderTest(unittest.TestCase):

    def setUp(self):
        self.this_dir = os.path.abspath(os.path.dirname(__file__))
        self.small_path = os.path.join(self.this_dir, b'small.csv')
        self.incomplete_path = os.path.join(self.this_dir, b'incomplete.csv')
        self.weird_path = os.path.join(self.this_dir, b'weird.csv')
        self.wide_path = os.path.join(self.this_dir, b'wide.csv')
        self.bom_path = os.path.join(self.this_dir, b'bom.csv')
        self.extra_path = os.path.join(self.this_dir, b'extra.csv')
        self.big_path = os.path.join(self.this_dir, b'big.csv')

    def test_stringio(self):
        with open(self.small_path, b'r') as (f):
            if six.PY3:
                sample = io.StringIO(f.read())
            else:
                sample = io.BytesIO(f.read())
        result = censusbatchgeocoder.geocode(sample)
        self.assertEqual(len(result), 5)

    def test_path(self):
        result = censusbatchgeocoder.geocode(self.small_path)
        self.assertEqual(len(result), 5)

    def test_list(self):
        my_list = [
         {b'address': b'521 SWARTHMORE AVENUE', 
            b'city': b'PACIFIC PALISADES', 
            b'id': b'1', 
            b'state': b'CA', 
            b'zipcode': b'90272-4350'},
         {b'address': b'2015 W TEMPLE STREET', 
            b'city': b'LOS ANGELES', 
            b'id': b'2', 
            b'state': b'CA', 
            b'zipcode': b'90026-4913'}]
        result = censusbatchgeocoder.geocode(my_list)
        self.assertEqual(len(result), 2)

    def test_extra_columns(self):
        result = censusbatchgeocoder.geocode(self.extra_path)
        self.assertEqual([ d[b'metadata_1'] for d in result ], [
         b'foo', b'bar', b'baz', b'bada', b'bing'])
        self.assertEqual([ d[b'metadata_2'] for d in result ], [
         b'eenie', b'meenie', b'miney', b'moe', b'catch a tiger by the toe'])
        self.assertEqual(len(result), 5)

    def test_weird_headers(self):
        result = censusbatchgeocoder.geocode(self.weird_path, id=b'foo', address=b'bar', city=b'baz', state=b'bada', zipcode=b'boom')
        self.assertEqual(len(result), 5)

    def test_wide(self):
        result = censusbatchgeocoder.geocode(self.wide_path, id=b'Affidavit ID', address=b'Street', city=b'City', state=b'State', zipcode=b'Zip')
        self.assertEqual(len(result), 10)

    def test_bom(self):
        result = censusbatchgeocoder.geocode(self.bom_path, id=b'Affidavit ID', address=b'Street', city=b'City', state=b'State', zipcode=b'Zip', encoding=b'utf-8-sig')
        self.assertEqual(len(result), 4)

    def test_no_state_and_zipcode(self):
        result = censusbatchgeocoder.geocode(self.incomplete_path, state=None, zipcode=None)
        self.assertEqual(len(result), 5)
        return

    def test_nopooling(self):
        result = censusbatchgeocoder.geocode(self.small_path, pooling=False)
        self.assertEqual(len(result), 5)

    def test_batch_size(self):
        result = censusbatchgeocoder.geocode(self.small_path, batch_size=2)
        self.assertEqual(len(result), 5)

    def test_coordinates(self):
        result = censusbatchgeocoder.geocode(self.small_path)
        for row in result:
            self.assertTrue(b'latitude' in row)
            self.assertTrue(b'longitude' in row)