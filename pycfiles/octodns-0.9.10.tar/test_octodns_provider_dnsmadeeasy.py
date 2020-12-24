# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_dnsmadeeasy.py
# Compiled at: 2020-01-15 20:00:35
from __future__ import absolute_import, division, print_function, unicode_literals
from mock import Mock, call
from os.path import dirname, join
from requests import HTTPError
from requests_mock import ANY, mock as requests_mock
from six import text_type
from unittest import TestCase
from octodns.record import Record
from octodns.provider.dnsmadeeasy import DnsMadeEasyClientNotFound, DnsMadeEasyProvider
from octodns.provider.yaml import YamlProvider
from octodns.zone import Zone
import json

class TestDnsMadeEasyProvider(TestCase):
    expected = Zone(b'unit.tests.', [])
    source = YamlProvider(b'test', join(dirname(__file__), b'config'))
    source.populate(expected)
    expected.add_record(Record.new(expected, b'under', {b'ttl': 3600, 
       b'type': b'NS', 
       b'values': [
                 b'ns1.unit.tests.',
                 b'ns2.unit.tests.']}))
    expected.add_record(Record.new(expected, b'', {b'ttl': 1800, 
       b'type': b'ALIAS', 
       b'value': b'aname.unit.tests.'}))
    expected.add_record(Record.new(expected, b'sub', {b'ttl': 1800, 
       b'type': b'ALIAS', 
       b'value': b'aname.unit.tests.'}))
    for record in list(expected.records):
        if record.name == b'sub' and record._type == b'NS':
            expected._remove_record(record)
            break

    def test_populate(self):
        provider = DnsMadeEasyProvider(b'test', b'api', b'secret')
        with requests_mock() as (mock):
            mock.get(ANY, status_code=401, text=b'{"error": ["API key not found"]}')
            with self.assertRaises(Exception) as (ctx):
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
            self.assertEquals(b'Unauthorized', text_type(ctx.exception))
        with requests_mock() as (mock):
            mock.get(ANY, status_code=400, text=b'{"error": ["Rate limit exceeded"]}')
            with self.assertRaises(Exception) as (ctx):
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
            self.assertEquals(b'\n  - Rate limit exceeded', text_type(ctx.exception))
        with requests_mock() as (mock):
            mock.get(ANY, status_code=502, text=b'Things caught fire')
            with self.assertRaises(HTTPError) as (ctx):
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
            self.assertEquals(502, ctx.exception.response.status_code)
        with requests_mock() as (mock):
            mock.get(ANY, status_code=404, text=b'<html><head></head><body></body></html>')
            zone = Zone(b'unit.tests.', [])
            provider.populate(zone)
            self.assertEquals(set(), zone.records)
        with requests_mock() as (mock):
            base = b'https://api.dnsmadeeasy.com/V2.0/dns/managed'
            with open(b'tests/fixtures/dnsmadeeasy-domains.json') as (fh):
                mock.get((b'{}{}').format(base, b'/'), text=fh.read())
            with open(b'tests/fixtures/dnsmadeeasy-records.json') as (fh):
                mock.get((b'{}{}').format(base, b'/123123/records'), text=fh.read())
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
                self.assertEquals(15, len(zone.records))
                changes = self.expected.changes(zone, provider)
                self.assertEquals(0, len(changes))
        again = Zone(b'unit.tests.', [])
        provider.populate(again)
        self.assertEquals(15, len(again.records))
        del provider._zone_records[zone.name]

    def test_apply(self):
        provider = DnsMadeEasyProvider(b'test', b'api', b'secret', True)
        resp = Mock()
        resp.json = Mock()
        provider._client._request = Mock(return_value=resp)
        with open(b'tests/fixtures/dnsmadeeasy-domains.json') as (fh):
            domains = json.load(fh)
        resp.json.side_effect = [
         DnsMadeEasyClientNotFound,
         DnsMadeEasyClientNotFound,
         domains]
        plan = provider.plan(self.expected)
        n = len(self.expected.records) - 5
        self.assertEquals(n, len(plan.changes))
        self.assertEquals(n, provider.apply(plan))
        provider._client._request.assert_has_calls([
         call(b'POST', b'/', data={b'name': b'unit.tests'}),
         call(b'GET', b'/'),
         call(b'POST', b'/123123/records', data={b'type': b'A', 
            b'name': b'', 
            b'value': b'1.2.3.4', 
            b'ttl': 300}),
         call(b'POST', b'/123123/records', data={b'type': b'A', 
            b'name': b'', 
            b'value': b'1.2.3.5', 
            b'ttl': 300}),
         call(b'POST', b'/123123/records', data={b'type': b'ANAME', 
            b'name': b'', 
            b'value': b'aname.unit.tests.', 
            b'ttl': 1800}),
         call(b'POST', b'/123123/records', data={b'name': b'', 
            b'value': b'ca.unit.tests', 
            b'issuerCritical': 0, 
            b'caaType': b'issue', b'ttl': 3600, 
            b'type': b'CAA'}),
         call(b'POST', b'/123123/records', data={b'name': b'_srv._tcp', 
            b'weight': 20, 
            b'value': b'foo-1.unit.tests.', 
            b'priority': 10, 
            b'ttl': 600, 
            b'type': b'SRV', 
            b'port': 30})])
        self.assertEquals(27, provider._client._request.call_count)
        provider._client._request.reset_mock()
        provider._client.records = Mock(return_value=[
         {b'id': 11189897, 
            b'name': b'www', 
            b'value': b'1.2.3.4', 
            b'ttl': 300, 
            b'type': b'A'},
         {b'id': 11189898, 
            b'name': b'www', 
            b'value': b'2.2.3.4', 
            b'ttl': 300, 
            b'type': b'A'},
         {b'id': 11189899, 
            b'name': b'ttl', 
            b'value': b'3.2.3.4', 
            b'ttl': 600, 
            b'type': b'A'}])
        resp.json.side_effect = [
         b'{}']
        wanted = Zone(b'unit.tests.', [])
        wanted.add_record(Record.new(wanted, b'ttl', {b'ttl': 300, 
           b'type': b'A', 
           b'value': b'3.2.3.4'}))
        plan = provider.plan(wanted)
        self.assertEquals(2, len(plan.changes))
        self.assertEquals(2, provider.apply(plan))
        provider._client._request.assert_has_calls([
         call(b'POST', b'/123123/records', data={b'value': b'3.2.3.4', 
            b'type': b'A', 
            b'name': b'ttl', 
            b'ttl': 300}),
         call(b'DELETE', b'/123123/records/11189899'),
         call(b'DELETE', b'/123123/records/11189897'),
         call(b'DELETE', b'/123123/records/11189898')], any_order=True)