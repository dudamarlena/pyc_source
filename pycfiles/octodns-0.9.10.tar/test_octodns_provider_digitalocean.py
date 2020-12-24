# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_digitalocean.py
# Compiled at: 2020-01-15 20:00:35
from __future__ import absolute_import, division, print_function, unicode_literals
from mock import Mock, call
from os.path import dirname, join
from requests import HTTPError
from requests_mock import ANY, mock as requests_mock
from six import text_type
from unittest import TestCase
from octodns.record import Record
from octodns.provider.digitalocean import DigitalOceanClientNotFound, DigitalOceanProvider
from octodns.provider.yaml import YamlProvider
from octodns.zone import Zone

class TestDigitalOceanProvider(TestCase):
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
        provider = DigitalOceanProvider(b'test', b'token')
        with requests_mock() as (mock):
            mock.get(ANY, status_code=401, text=b'{"id":"unauthorized","message":"Unable to authenticate you."}')
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
            mock.get(ANY, status_code=404, text=b'{"id":"not_found","message":"The resource you were accessing could not be found."}')
            zone = Zone(b'unit.tests.', [])
            provider.populate(zone)
            self.assertEquals(set(), zone.records)
        with requests_mock() as (mock):
            base = b'https://api.digitalocean.com/v2/domains/unit.tests/records?page='
            with open(b'tests/fixtures/digitalocean-page-1.json') as (fh):
                mock.get((b'{}{}').format(base, 1), text=fh.read())
            with open(b'tests/fixtures/digitalocean-page-2.json') as (fh):
                mock.get((b'{}{}').format(base, 2), text=fh.read())
            zone = Zone(b'unit.tests.', [])
            provider.populate(zone)
            self.assertEquals(12, len(zone.records))
            changes = self.expected.changes(zone, provider)
            self.assertEquals(0, len(changes))
        again = Zone(b'unit.tests.', [])
        provider.populate(again)
        self.assertEquals(12, len(again.records))
        del provider._zone_records[zone.name]

    def test_apply(self):
        provider = DigitalOceanProvider(b'test', b'token')
        resp = Mock()
        resp.json = Mock()
        provider._client._request = Mock(return_value=resp)
        domain_after_creation = {b'domain_records': [
                             {b'id': 11189874, 
                                b'type': b'NS', 
                                b'name': b'@', 
                                b'data': b'ns1.digitalocean.com', 
                                b'priority': None, 
                                b'port': None, 
                                b'ttl': 3600, 
                                b'weight': None, 
                                b'flags': None, 
                                b'tag': None},
                             {b'id': 11189875, 
                                b'type': b'NS', 
                                b'name': b'@', 
                                b'data': b'ns2.digitalocean.com', 
                                b'priority': None, 
                                b'port': None, 
                                b'ttl': 3600, 
                                b'weight': None, 
                                b'flags': None, 
                                b'tag': None},
                             {b'id': 11189876, 
                                b'type': b'NS', 
                                b'name': b'@', 
                                b'data': b'ns3.digitalocean.com', 
                                b'priority': None, 
                                b'port': None, 
                                b'ttl': 3600, 
                                b'weight': None, 
                                b'flags': None, 
                                b'tag': None},
                             {b'id': 11189877, 
                                b'type': b'A', 
                                b'name': b'@', 
                                b'data': b'192.0.2.1', 
                                b'priority': None, 
                                b'port': None, 
                                b'ttl': 3600, 
                                b'weight': None, 
                                b'flags': None, 
                                b'tag': None}], 
           b'links': {}, b'meta': {b'total': 4}}
        resp.json.side_effect = [
         DigitalOceanClientNotFound,
         DigitalOceanClientNotFound,
         domain_after_creation]
        plan = provider.plan(self.expected)
        n = len(self.expected.records) - 7
        self.assertEquals(n, len(plan.changes))
        self.assertEquals(n, provider.apply(plan))
        self.assertFalse(plan.exists)
        provider._client._request.assert_has_calls([
         call(b'POST', b'/domains', data={b'ip_address': b'192.0.2.1', b'name': b'unit.tests'}),
         call(b'GET', b'/domains/unit.tests/records', {b'page': 1}),
         call(b'DELETE', b'/domains/unit.tests/records/11189877'),
         call(b'POST', b'/domains/unit.tests/records', data={b'data': b'1.2.3.4', 
            b'name': b'@', 
            b'ttl': 300, 
            b'type': b'A'}),
         call(b'POST', b'/domains/unit.tests/records', data={b'data': b'1.2.3.5', 
            b'name': b'@', 
            b'ttl': 300, 
            b'type': b'A'}),
         call(b'POST', b'/domains/unit.tests/records', data={b'data': b'ca.unit.tests.', 
            b'flags': 0, 
            b'name': b'@', b'tag': b'issue', 
            b'ttl': 3600, 
            b'type': b'CAA'}),
         call(b'POST', b'/domains/unit.tests/records', data={b'name': b'_srv._tcp', 
            b'weight': 20, 
            b'data': b'foo-1.unit.tests.', 
            b'priority': 10, 
            b'ttl': 600, 
            b'type': b'SRV', 
            b'port': 30})])
        self.assertEquals(24, provider._client._request.call_count)
        provider._client._request.reset_mock()
        provider._client.records = Mock(return_value=[
         {b'id': 11189897, 
            b'name': b'www', 
            b'data': b'1.2.3.4', 
            b'ttl': 300, 
            b'type': b'A'},
         {b'id': 11189898, 
            b'name': b'www', 
            b'data': b'2.2.3.4', 
            b'ttl': 300, 
            b'type': b'A'},
         {b'id': 11189899, 
            b'name': b'ttl', 
            b'data': b'3.2.3.4', 
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
         call(b'POST', b'/domains/unit.tests/records', data={b'data': b'3.2.3.4', 
            b'type': b'A', 
            b'name': b'ttl', 
            b'ttl': 300}),
         call(b'DELETE', b'/domains/unit.tests/records/11189899'),
         call(b'DELETE', b'/domains/unit.tests/records/11189897'),
         call(b'DELETE', b'/domains/unit.tests/records/11189898')], any_order=True)
        return