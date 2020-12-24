# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_constellix.py
# Compiled at: 2019-10-18 13:06:59
from __future__ import absolute_import, division, print_function, unicode_literals
from mock import Mock, call
from os.path import dirname, join
from requests import HTTPError
from requests_mock import ANY, mock as requests_mock
from six import text_type
from unittest import TestCase
from octodns.record import Record
from octodns.provider.constellix import ConstellixClientNotFound, ConstellixProvider
from octodns.provider.yaml import YamlProvider
from octodns.zone import Zone
import json

class TestConstellixProvider(TestCase):
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
        provider = ConstellixProvider(b'test', b'api', b'secret')
        with requests_mock() as (mock):
            mock.get(ANY, status_code=401, text=b'{"errors": ["Unable to authenticate token"]}')
            with self.assertRaises(Exception) as (ctx):
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
            self.assertEquals(b'Unauthorized', text_type(ctx.exception))
        with requests_mock() as (mock):
            mock.get(ANY, status_code=400, text=b'{"errors": ["\\"unittests\\" is not a valid domain name"]}')
            with self.assertRaises(Exception) as (ctx):
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
            self.assertEquals(b'\n  - "unittests" is not a valid domain name', text_type(ctx.exception))
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
            base = b'https://api.dns.constellix.com/v1/domains'
            with open(b'tests/fixtures/constellix-domains.json') as (fh):
                mock.get((b'{}{}').format(base, b'/'), text=fh.read())
            with open(b'tests/fixtures/constellix-records.json') as (fh):
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
        provider = ConstellixProvider(b'test', b'api', b'secret')
        resp = Mock()
        resp.json = Mock()
        provider._client._request = Mock(return_value=resp)
        with open(b'tests/fixtures/constellix-domains.json') as (fh):
            domains = json.load(fh)
        resp.json.side_effect = [
         ConstellixClientNotFound,
         ConstellixClientNotFound,
         domains]
        plan = provider.plan(self.expected)
        n = len(self.expected.records) - 5
        self.assertEquals(n, len(plan.changes))
        self.assertEquals(n, provider.apply(plan))
        provider._client._request.assert_has_calls([
         call(b'POST', b'/', data={b'names': [b'unit.tests']}),
         call(b'GET', b'/')])
        provider._client._request.assert_has_calls([
         call(b'POST', b'/123123/records/SRV', data={b'roundRobin': [
                          {b'priority': 10, 
                             b'weight': 20, 
                             b'value': b'foo-1.unit.tests.', 
                             b'port': 30},
                          {b'priority': 12, 
                             b'weight': 20, 
                             b'value': b'foo-2.unit.tests.', 
                             b'port': 30}], 
            b'name': b'_srv._tcp', 
            b'ttl': 600})])
        self.assertEquals(20, provider._client._request.call_count)
        provider._client._request.reset_mock()
        provider._client.records = Mock(return_value=[
         {b'id': 11189897, 
            b'type': b'A', 
            b'name': b'www', 
            b'ttl': 300, 
            b'value': [
                     b'1.2.3.4',
                     b'2.2.3.4']},
         {b'id': 11189898, 
            b'type': b'A', 
            b'name': b'ttl', 
            b'ttl': 600, 
            b'value': [
                     b'3.2.3.4']},
         {b'id': 11189899, 
            b'type': b'ALIAS', 
            b'name': b'alias', 
            b'ttl': 600, 
            b'value': [
                     {b'value': b'aname.unit.tests.'}]}])
        resp.json.side_effect = [
         b'{}']
        wanted = Zone(b'unit.tests.', [])
        wanted.add_record(Record.new(wanted, b'ttl', {b'ttl': 300, 
           b'type': b'A', 
           b'value': b'3.2.3.4'}))
        plan = provider.plan(wanted)
        self.assertEquals(3, len(plan.changes))
        self.assertEquals(3, provider.apply(plan))
        provider._client._request.assert_has_calls([
         call(b'POST', b'/123123/records/A', data={b'roundRobin': [
                          {b'value': b'3.2.3.4'}], 
            b'name': b'ttl', 
            b'ttl': 300}),
         call(b'DELETE', b'/123123/records/A/11189897'),
         call(b'DELETE', b'/123123/records/A/11189898'),
         call(b'DELETE', b'/123123/records/ANAME/11189899')], any_order=True)