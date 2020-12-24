# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_source_axfr.py
# Compiled at: 2019-10-18 13:06:59
from __future__ import absolute_import, division, print_function, unicode_literals
import dns.zone
from dns.exception import DNSException
from mock import patch
from six import text_type
from unittest import TestCase
from octodns.source.axfr import AxfrSource, AxfrSourceZoneTransferFailed, ZoneFileSource, ZoneFileSourceLoadFailure
from octodns.zone import Zone

class TestAxfrSource(TestCase):
    source = AxfrSource(b'test', b'localhost')
    forward_zonefile = dns.zone.from_file(b'./tests/zones/unit.tests.', b'unit.tests', relativize=False)

    @patch(b'dns.zone.from_xfr')
    def test_populate(self, from_xfr_mock):
        got = Zone(b'unit.tests.', [])
        from_xfr_mock.side_effect = [
         self.forward_zonefile,
         DNSException]
        self.source.populate(got)
        self.assertEquals(11, len(got.records))
        with self.assertRaises(AxfrSourceZoneTransferFailed) as (ctx):
            zone = Zone(b'unit.tests.', [])
            self.source.populate(zone)
        self.assertEquals(b'Unable to Perform Zone Transfer', text_type(ctx.exception))


class TestZoneFileSource(TestCase):
    source = ZoneFileSource(b'test', b'./tests/zones')

    def test_populate(self):
        valid = Zone(b'unit.tests.', [])
        self.source.populate(valid)
        self.assertEquals(11, len(valid.records))
        again = Zone(b'unit.tests.', [])
        self.source.populate(again)
        self.assertEquals(11, len(again.records))
        del self.source._zone_records[valid.name]
        missing = Zone(b'missing.zone.', [])
        self.source.populate(missing)
        self.assertEquals(0, len(missing.records))
        with self.assertRaises(ZoneFileSourceLoadFailure) as (ctx):
            zone = Zone(b'invalid.zone.', [])
            self.source.populate(zone)
        self.assertEquals(b'The DNS zone has no NS RRset at its origin.', text_type(ctx.exception))