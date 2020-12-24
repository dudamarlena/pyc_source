# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_powerdns.py
# Compiled at: 2020-01-15 20:00:35
from __future__ import absolute_import, division, print_function, unicode_literals
from json import loads, dumps
from os.path import dirname, join
from requests import HTTPError
from requests_mock import ANY, mock as requests_mock
from six import text_type
from unittest import TestCase
from octodns.record import Record
from octodns.provider.powerdns import PowerDnsProvider
from octodns.provider.yaml import YamlProvider
from octodns.zone import Zone
EMPTY_TEXT = b'\n{\n    "account": "",\n    "dnssec": false,\n    "id": "xunit.tests.",\n    "kind": "Master",\n    "last_check": 0,\n    "masters": [],\n    "name": "xunit.tests.",\n    "notified_serial": 0,\n    "rrsets": [],\n    "serial": 2017012801,\n    "soa_edit": "",\n    "soa_edit_api": "INCEPTION-INCREMENT",\n    "url": "api/v1/servers/localhost/zones/xunit.tests."\n}\n'
with open(b'./tests/fixtures/powerdns-full-data.json') as (fh):
    FULL_TEXT = fh.read()

class TestPowerDnsProvider(TestCase):

    def test_provider(self):
        provider = PowerDnsProvider(b'test', b'non.existent', b'api-key', nameserver_values=[
         b'8.8.8.8.',
         b'9.9.9.9.'])
        with requests_mock() as (mock):
            mock.get(ANY, status_code=401, text=b'Unauthorized')
            with self.assertRaises(Exception) as (ctx):
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
            self.assertTrue(b'unauthorized' in text_type(ctx.exception))
        with requests_mock() as (mock):
            mock.get(ANY, status_code=502, text=b'Things caught fire')
            with self.assertRaises(HTTPError) as (ctx):
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
            self.assertEquals(502, ctx.exception.response.status_code)
        with requests_mock() as (mock):
            mock.get(ANY, status_code=422, json={b'error': b"Could not find domain 'unit.tests.'"})
            zone = Zone(b'unit.tests.', [])
            provider.populate(zone)
            self.assertEquals(set(), zone.records)
        expected = Zone(b'unit.tests.', [])
        source = YamlProvider(b'test', join(dirname(__file__), b'config'))
        source.populate(expected)
        expected_n = len(expected.records) - 2
        self.assertEquals(16, expected_n)
        with requests_mock() as (mock):
            mock.get(ANY, status_code=200, text=FULL_TEXT)
            zone = Zone(b'unit.tests.', [])
            provider.populate(zone)
            self.assertEquals(16, len(zone.records))
            changes = expected.changes(zone, provider)
            self.assertEquals(0, len(changes))

        def assert_rrsets_callback(request, context):
            data = loads(request.body)
            self.assertEquals(expected_n, len(data[b'rrsets']))
            return b''

        with requests_mock() as (mock):
            mock.get(ANY, status_code=200, text=EMPTY_TEXT)
            mock.patch(ANY, status_code=201, text=assert_rrsets_callback)
            plan = provider.plan(expected)
            self.assertEquals(expected_n, len(plan.changes))
            self.assertEquals(expected_n, provider.apply(plan))
            self.assertTrue(plan.exists)
        not_found = {b'error': b"Could not find domain 'unit.tests.'"}
        with requests_mock() as (mock):
            mock.get(ANY, status_code=422, text=b'')
            mock.patch(ANY, status_code=422, text=dumps(not_found))
            mock.post(ANY, status_code=201, text=assert_rrsets_callback)
            plan = provider.plan(expected)
            self.assertEquals(expected_n, len(plan.changes))
            self.assertEquals(expected_n, provider.apply(plan))
            self.assertFalse(plan.exists)
        with requests_mock() as (mock):
            mock.get(ANY, status_code=422, text=b'')
            data = {b'error': b"Key 'name' not present or not a String"}
            mock.patch(ANY, status_code=422, text=dumps(data))
            with self.assertRaises(HTTPError) as (ctx):
                plan = provider.plan(expected)
                provider.apply(plan)
            response = ctx.exception.response
            self.assertEquals(422, response.status_code)
            self.assertTrue(b'error' in response.json())
        with requests_mock() as (mock):
            mock.get(ANY, status_code=422, text=b'')
            mock.patch(ANY, status_code=500, text=b'')
            with self.assertRaises(HTTPError):
                plan = provider.plan(expected)
                provider.apply(plan)
        with requests_mock() as (mock):
            mock.get(ANY, status_code=422, text=b'')
            mock.patch(ANY, status_code=422, text=dumps(not_found))
            mock.post(ANY, status_code=422, text=b'Hello Word!')
            with self.assertRaises(HTTPError):
                plan = provider.plan(expected)
                provider.apply(plan)

    def test_small_change(self):
        provider = PowerDnsProvider(b'test', b'non.existent', b'api-key')
        expected = Zone(b'unit.tests.', [])
        source = YamlProvider(b'test', join(dirname(__file__), b'config'))
        source.populate(expected)
        self.assertEquals(18, len(expected.records))
        with requests_mock() as (mock):
            mock.get(ANY, status_code=200, text=FULL_TEXT)
            missing = Zone(expected.name, [])
            for record in expected.records:
                if record._type != b'SPF':
                    missing.add_record(record)

            def assert_delete_callback(request, context):
                self.assertEquals({b'rrsets': [
                             {b'records': [
                                           {b'content': b'"v=spf1 ip4:192.168.0.1/16-all"', b'disabled': False}], 
                                b'changetype': b'DELETE', 
                                b'type': b'SPF', 
                                b'name': b'spf.unit.tests.', 
                                b'ttl': 600}]}, loads(request.body))
                return b''

            mock.patch(ANY, status_code=201, text=assert_delete_callback)
            plan = provider.plan(missing)
            self.assertEquals(1, len(plan.changes))
            self.assertEquals(1, provider.apply(plan))

    def test_existing_nameservers(self):
        ns_values = [b'8.8.8.8.', b'9.9.9.9.']
        provider = PowerDnsProvider(b'test', b'non.existent', b'api-key', nameserver_values=ns_values)
        expected = Zone(b'unit.tests.', [])
        ns_record = Record.new(expected, b'', {b'type': b'NS', 
           b'ttl': 600, 
           b'values': ns_values})
        expected.add_record(ns_record)
        with requests_mock() as (mock):
            data = {b'rrsets': [
                         {b'comments': [], b'name': b'unit.tests.', 
                            b'records': [
                                       {b'content': b'8.8.8.8.', 
                                          b'disabled': False},
                                       {b'content': b'9.9.9.9.', 
                                          b'disabled': False}], 
                            b'ttl': 600, 
                            b'type': b'NS'},
                         {b'comments': [], b'name': b'unit.tests.', 
                            b'records': [
                                       {b'content': b'1.2.3.4', 
                                          b'disabled': False}], 
                            b'ttl': 60, 
                            b'type': b'A'}]}
            mock.get(ANY, status_code=200, json=data)
            unrelated_record = Record.new(expected, b'', {b'type': b'A', 
               b'ttl': 60, 
               b'value': b'1.2.3.4'})
            expected.add_record(unrelated_record)
            plan = provider.plan(expected)
            self.assertFalse(plan)
            expected._remove_record(unrelated_record)
        with requests_mock() as (mock):
            data = {b'rrsets': [
                         {b'comments': [], b'name': b'unit.tests.', 
                            b'records': [
                                       {b'content': b'8.8.8.8.', 
                                          b'disabled': False},
                                       {b'content': b'9.9.9.9.', 
                                          b'disabled': False}], 
                            b'ttl': 3600, 
                            b'type': b'NS'}]}
            mock.get(ANY, status_code=200, json=data)
            plan = provider.plan(expected)
            self.assertEquals(1, len(plan.changes))
        with requests_mock() as (mock):
            data = {b'rrsets': []}
            mock.get(ANY, status_code=200, json=data)
            plan = provider.plan(expected)
            self.assertEquals(1, len(plan.changes))