# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_record_geo.py
# Compiled at: 2019-03-28 16:58:28
from __future__ import absolute_import, division, print_function, unicode_literals
from unittest import TestCase
from octodns.record.geo import GeoCodes

class TestRecordGeoCodes(TestCase):

    def test_validate(self):
        prefix = b'xyz '
        self.assertEquals([], GeoCodes.validate(b'NA', prefix))
        self.assertEquals([], GeoCodes.validate(b'NA-US', prefix))
        self.assertEquals([], GeoCodes.validate(b'NA-US-OR', prefix))
        self.assertEquals([b'xyz invalid geo code "XX-YY-ZZ-AA"'], GeoCodes.validate(b'XX-YY-ZZ-AA', prefix))
        self.assertEquals([b'xyz unknown continent code "X-Y-Z"'], GeoCodes.validate(b'X-Y-Z', prefix))
        self.assertEquals([b'xyz unknown continent code "XXX-Y-Z"'], GeoCodes.validate(b'XXX-Y-Z', prefix))
        self.assertEquals([b'xyz unknown continent code "XX"'], GeoCodes.validate(b'XX', prefix))
        self.assertEquals([b'xyz unknown continent code "XX-US"'], GeoCodes.validate(b'XX-US', prefix))
        self.assertEquals([b'xyz unknown continent code "XX-US-OR"'], GeoCodes.validate(b'XX-US-OR', prefix))
        self.assertEquals([b'xyz unknown country code "NA-XX"'], GeoCodes.validate(b'NA-XX', prefix))
        self.assertEquals([b'xyz unknown country code "NA-XX-OR"'], GeoCodes.validate(b'NA-XX-OR', prefix))
        self.assertEquals([b'xyz unknown country code "NA-GB"'], GeoCodes.validate(b'NA-GB', prefix))
        self.assertEquals([b'xyz unknown province code "NA-US-XX"'], GeoCodes.validate(b'NA-US-XX', prefix))

    def test_parse(self):
        self.assertEquals({b'continent_code': b'NA', 
           b'country_code': None, 
           b'province_code': None}, GeoCodes.parse(b'NA'))
        self.assertEquals({b'continent_code': b'NA', 
           b'country_code': b'US', 
           b'province_code': None}, GeoCodes.parse(b'NA-US'))
        self.assertEquals({b'continent_code': b'NA', 
           b'country_code': b'US', 
           b'province_code': b'CA'}, GeoCodes.parse(b'NA-US-CA'))
        return

    def test_country_to_code(self):
        self.assertEquals(b'NA-US', GeoCodes.country_to_code(b'US'))
        self.assertEquals(b'EU-GB', GeoCodes.country_to_code(b'GB'))
        self.assertFalse(GeoCodes.country_to_code(b'XX'))

    def test_province_to_code(self):
        self.assertEquals(b'NA-US-OR', GeoCodes.province_to_code(b'OR'))
        self.assertEquals(b'NA-US-KY', GeoCodes.province_to_code(b'KY'))
        self.assertFalse(GeoCodes.province_to_code(b'XX'))