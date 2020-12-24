# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_dnsimple.py
# Compiled at: 2019-10-18 13:06:59
from __future__ import absolute_import, division, print_function, unicode_literals
from mock import Mock, call
from os.path import dirname, join
from requests import HTTPError
from requests_mock import ANY, mock as requests_mock
from six import text_type
from unittest import TestCase
from octodns.record import Record
from octodns.provider.dnsimple import DnsimpleClientNotFound, DnsimpleProvider
from octodns.provider.yaml import YamlProvider
from octodns.zone import Zone

class TestDnsimpleProvider(TestCase):
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
        provider = DnsimpleProvider(b'test', b'token', 42)
        with requests_mock() as (mock):
            mock.get(ANY, status_code=401, text=b'{"message": "Authentication failed"}')
            with self.assertRaises(Exception) as (ctx):
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
            self.assertEquals(b'Unauthorized', text_type(ctx.exception))
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
            base = b'https://api.dnsimple.com/v2/42/zones/unit.tests/records?page='
            with open(b'tests/fixtures/dnsimple-page-1.json') as (fh):
                mock.get((b'{}{}').format(base, 1), text=fh.read())
            with open(b'tests/fixtures/dnsimple-page-2.json') as (fh):
                mock.get((b'{}{}').format(base, 2), text=fh.read())
            zone = Zone(b'unit.tests.', [])
            provider.populate(zone)
            self.assertEquals(16, len(zone.records))
            changes = self.expected.changes(zone, provider)
            self.assertEquals(0, len(changes))
        again = Zone(b'unit.tests.', [])
        provider.populate(again)
        self.assertEquals(16, len(again.records))
        del provider._zone_records[zone.name]
        with requests_mock() as (mock):
            with open(b'tests/fixtures/dnsimple-invalid-content.json') as (fh):
                mock.get(ANY, text=fh.read())
            zone = Zone(b'unit.tests.', [])
            provider.populate(zone, lenient=True)
            self.assertEquals(set([
             Record.new(zone, b'', {b'ttl': 3600, 
                b'type': b'SSHFP', 
                b'values': []}, lenient=True),
             Record.new(zone, b'_srv._tcp', {b'ttl': 600, 
                b'type': b'SRV', 
                b'values': []}, lenient=True),
             Record.new(zone, b'naptr', {b'ttl': 600, 
                b'type': b'NAPTR', 
                b'values': []}, lenient=True)]), zone.records)

    def test_apply(self):
        provider = DnsimpleProvider(b'test', b'token', 42)
        resp = Mock()
        resp.json = Mock()
        provider._client._request = Mock(return_value=resp)
        resp.json.side_effect = [
         DnsimpleClientNotFound,
         DnsimpleClientNotFound]
        plan = provider.plan(self.expected)
        n = len(self.expected.records) - 3
        self.assertEquals(n, len(plan.changes))
        self.assertEquals(n, provider.apply(plan))
        self.assertFalse(plan.exists)
        provider._client._request.assert_has_calls([
         call(b'POST', b'/domains', data={b'name': b'unit.tests'}),
         call(b'POST', b'/zones/unit.tests/records', data={b'content': b'1.2.3.4', 
            b'type': b'A', 
            b'name': b'', 
            b'ttl': 300}),
         call(b'POST', b'/zones/unit.tests/records', data={b'content': b'1.2.3.5', 
            b'type': b'A', 
            b'name': b'', 
            b'ttl': 300}),
         call(b'POST', b'/zones/unit.tests/records', data={b'content': b'0 issue "ca.unit.tests"', 
            b'type': b'CAA', 
            b'name': b'', 
            b'ttl': 3600}),
         call(b'POST', b'/zones/unit.tests/records', data={b'content': b'1 1 7491973e5f8b39d5327cd4e08bc81b05f7710b49', 
            b'type': b'SSHFP', 
            b'name': b'', 
            b'ttl': 3600}),
         call(b'POST', b'/zones/unit.tests/records', data={b'content': b'1 1 bf6b6825d2977c511a475bbefb88aad54a92ac73', 
            b'type': b'SSHFP', 
            b'name': b'', 
            b'ttl': 3600}),
         call(b'POST', b'/zones/unit.tests/records', data={b'content': b'20 30 foo-1.unit.tests.', 
            b'priority': 10, 
            b'type': b'SRV', 
            b'name': b'_srv._tcp', 
            b'ttl': 600})])
        self.assertEquals(28, provider._client._request.call_count)
        provider._client._request.reset_mock()
        provider._client.records = Mock(return_value=[
         {b'id': 11189897, 
            b'name': b'www', 
            b'content': b'1.2.3.4', 
            b'ttl': 300, 
            b'type': b'A'},
         {b'id': 11189898, 
            b'name': b'www', 
            b'content': b'2.2.3.4', 
            b'ttl': 300, 
            b'type': b'A'},
         {b'id': 11189899, 
            b'name': b'ttl', 
            b'content': b'3.2.3.4', 
            b'ttl': 600, 
            b'type': b'A'}])
        resp.json.side_effect = [
         b'{}']
        wanted = Zone(b'unit.tests.', [])
        wanted.add_record(Record.new(wanted, b'ttl', {b'ttl': 300, 
           b'type': b'A', 
           b'value': b'3.2.3.4'}))
        plan = provider.plan(wanted)
        self.assertTrue(plan.exists)
        self.assertEquals(2, len(plan.changes))
        self.assertEquals(2, provider.apply(plan))
        provider._client._request.assert_has_calls([
         call(b'POST', b'/zones/unit.tests/records', data={b'content': b'3.2.3.4', 
            b'type': b'A', 
            b'name': b'ttl', 
            b'ttl': 300}),
         call(b'DELETE', b'/zones/unit.tests/records/11189899'),
         call(b'DELETE', b'/zones/unit.tests/records/11189897'),
         call(b'DELETE', b'/zones/unit.tests/records/11189898')], any_order=True)