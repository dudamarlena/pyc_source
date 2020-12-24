# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_fastdns.py
# Compiled at: 2020-03-06 20:32:12
from __future__ import absolute_import, division, print_function, unicode_literals
from os.path import dirname, join
from requests import HTTPError
from requests_mock import ANY, mock as requests_mock
from six import text_type
from unittest import TestCase
from octodns.record import Record
from octodns.provider.fastdns import AkamaiProvider
from octodns.provider.yaml import YamlProvider
from octodns.zone import Zone

class TestFastdnsProvider(TestCase):
    expected = Zone(b'unit.tests.', [])
    source = YamlProvider(b'test', join(dirname(__file__), b'config'))
    source.populate(expected)
    expected.add_record(Record.new(expected, b'under', {b'ttl': 3600, 
       b'type': b'NS', 
       b'values': [
                 b'ns1.unit.tests.',
                 b'ns2.unit.tests.']}))
    for record in list(expected.records):
        if record.name == b'sub' and record._type == b'NS':
            expected._remove_record(record)
            break

    def test_populate(self):
        provider = AkamaiProvider(b'test', b'secret', b'akam.com', b'atok', b'ctok')
        with requests_mock() as (mock):
            mock.get(ANY, status_code=401, text=b'{"message": "Unauthorized"}')
            with self.assertRaises(Exception) as (ctx):
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
            self.assertEquals(401, ctx.exception.response.status_code)
        with requests_mock() as (mock):
            mock.get(ANY, status_code=502, text=b'Things caught fire')
            with self.assertRaises(HTTPError) as (ctx):
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
            self.assertEquals(502, ctx.exception.response.status_code)
        with requests_mock() as (mock):
            mock.get(ANY, status_code=404, text=b'{"message": "Domain `foo.bar` not found"}')
            zone = Zone(b'unit.tests.', [])
            provider.populate(zone)
            self.assertEquals(set(), zone.records)
        with requests_mock() as (mock):
            with open(b'tests/fixtures/fastdns-records.json') as (fh):
                mock.get(ANY, text=fh.read())
            zone = Zone(b'unit.tests.', [])
            provider.populate(zone)
            self.assertEquals(16, len(zone.records))
            changes = self.expected.changes(zone, provider)
            self.assertEquals(0, len(changes))
        again = Zone(b'unit.tests.', [])
        provider.populate(again)
        self.assertEquals(16, len(again.records))
        del provider._zone_records[zone.name]

    def test_apply(self):
        provider = AkamaiProvider(b'test', b's', b'akam.com', b'atok', b'ctok', b'cid', b'gid')
        with requests_mock() as (mock):
            with open(b'tests/fixtures/fastdns-records-prev.json') as (fh):
                mock.get(ANY, text=fh.read())
            plan = provider.plan(self.expected)
            mock.post(ANY, status_code=201)
            mock.put(ANY, status_code=200)
            mock.delete(ANY, status_code=204)
            changes = provider.apply(plan)
            self.assertEquals(29, changes)
        with requests_mock() as (mock):
            with open(b'tests/fixtures/fastdns-records-prev-other.json') as (fh):
                mock.get(ANY, status_code=404)
            plan = provider.plan(self.expected)
            mock.post(ANY, status_code=201)
            mock.put(ANY, status_code=200)
            mock.delete(ANY, status_code=204)
            changes = provider.apply(plan)
            self.assertEquals(14, changes)
        with requests_mock() as (mock):
            with open(b'tests/fixtures/fastdns-records-prev-other.json') as (fh):
                mock.get(ANY, status_code=404)
            provider = AkamaiProvider(b'test', b's', b'akam.com', b'atok', b'ctok', b'cid')
            plan = provider.plan(self.expected)
            mock.post(ANY, status_code=201)
            mock.put(ANY, status_code=200)
            mock.delete(ANY, status_code=204)
            changes = provider.apply(plan)
            self.assertEquals(14, changes)
        with requests_mock() as (mock):
            mock.get(ANY, status_code=404)
            provider = AkamaiProvider(b'test', b's', b'akam.com', b'atok', b'ctok')
            plan = provider.plan(self.expected)
            mock.post(ANY, status_code=201)
            mock.put(ANY, status_code=200)
            mock.delete(ANY, status_code=204)
            try:
                changes = provider.apply(plan)
            except NameError as e:
                expected = b'contractId not specified to create zone'
                self.assertEquals(text_type(e), expected)