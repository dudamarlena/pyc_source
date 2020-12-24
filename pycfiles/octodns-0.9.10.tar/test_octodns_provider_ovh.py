# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_ovh.py
# Compiled at: 2020-01-27 16:06:47
from __future__ import absolute_import, division, print_function, unicode_literals
from unittest import TestCase
from mock import patch, call
from ovh import APIError, ResourceNotFoundError, InvalidCredential
from octodns.provider.ovh import OvhProvider
from octodns.record import Record
from octodns.zone import Zone

class TestOvhProvider(TestCase):
    api_record = []
    valid_dkim = []
    invalid_dkim = []
    valid_dkim_key = b'p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCxLaG16G4SaEcXVdiIxTg7gKSGbHKQLm30CHib1h9FzS9nkcyvQSyQj1rMFyqC//tft3ohx3nvJl+bGCWxdtLYDSmir9PW54e5CTdxEh8MWRkBO3StF6QG/tAh3aTGDmkqhIJGLb87iHvpmVKqURmEUzJPv5KPJfWLofADI+q9lQIDAQAB'
    zone = Zone(b'unit.tests.', [])
    expected = set()
    api_record.append({b'fieldType': b'A', 
       b'ttl': 100, 
       b'target': b'1.2.3.4', 
       b'subDomain': b'', 
       b'id': 1})
    expected.add(Record.new(zone, b'', {b'ttl': 100, 
       b'type': b'A', 
       b'value': b'1.2.3.4'}))
    api_record.append({b'fieldType': b'A', 
       b'ttl': 200, 
       b'target': b'1.2.3.4', 
       b'subDomain': b'sub', 
       b'id': 2})
    expected.add(Record.new(zone, b'sub', {b'ttl': 200, 
       b'type': b'A', 
       b'value': b'1.2.3.4'}))
    api_record.append({b'fieldType': b'CNAME', 
       b'ttl': 300, 
       b'target': b'unit.tests.', 
       b'subDomain': b'www2', 
       b'id': 3})
    expected.add(Record.new(zone, b'www2', {b'ttl': 300, 
       b'type': b'CNAME', 
       b'value': b'unit.tests.'}))
    api_record.append({b'fieldType': b'MX', 
       b'ttl': 400, 
       b'target': b'10 mx1.unit.tests.', 
       b'subDomain': b'', 
       b'id': 4})
    expected.add(Record.new(zone, b'', {b'ttl': 400, 
       b'type': b'MX', 
       b'values': [
                 {b'preference': 10, 
                    b'exchange': b'mx1.unit.tests.'}]}))
    api_record.append({b'fieldType': b'NAPTR', 
       b'ttl': 500, 
       b'target': b'10 100 "S" "SIP+D2U" "!^.*$!sip:info@bar.example.com!" .', 
       b'subDomain': b'naptr', 
       b'id': 5})
    expected.add(Record.new(zone, b'naptr', {b'ttl': 500, 
       b'type': b'NAPTR', 
       b'values': [
                 {b'flags': b'S', 
                    b'order': 10, 
                    b'preference': 100, 
                    b'regexp': b'!^.*$!sip:info@bar.example.com!', 
                    b'replacement': b'.', 
                    b'service': b'SIP+D2U'}]}))
    api_record.append({b'fieldType': b'NS', 
       b'ttl': 600, 
       b'target': b'ns1.unit.tests.', 
       b'subDomain': b'', 
       b'id': 6})
    api_record.append({b'fieldType': b'NS', 
       b'ttl': 600, 
       b'target': b'ns2.unit.tests.', 
       b'subDomain': b'', 
       b'id': 7})
    expected.add(Record.new(zone, b'', {b'ttl': 600, 
       b'type': b'NS', 
       b'values': [
                 b'ns1.unit.tests.', b'ns2.unit.tests.']}))
    api_record.append({b'fieldType': b'NS', 
       b'ttl': 700, 
       b'target': b'ns3.unit.tests.', 
       b'subDomain': b'www3', 
       b'id': 8})
    api_record.append({b'fieldType': b'NS', 
       b'ttl': 700, 
       b'target': b'ns4.unit.tests.', 
       b'subDomain': b'www3', 
       b'id': 9})
    expected.add(Record.new(zone, b'www3', {b'ttl': 700, 
       b'type': b'NS', 
       b'values': [
                 b'ns3.unit.tests.', b'ns4.unit.tests.']}))
    api_record.append({b'fieldType': b'SRV', 
       b'ttl': 800, 
       b'target': b'10 20 30 foo-1.unit.tests.', 
       b'subDomain': b'_srv._tcp', 
       b'id': 10})
    api_record.append({b'fieldType': b'SRV', 
       b'ttl': 800, 
       b'target': b'40 50 60 foo-2.unit.tests.', 
       b'subDomain': b'_srv._tcp', 
       b'id': 11})
    expected.add(Record.new(zone, b'_srv._tcp', {b'ttl': 800, 
       b'type': b'SRV', 
       b'values': [
                 {b'priority': 10, 
                    b'weight': 20, 
                    b'port': 30, 
                    b'target': b'foo-1.unit.tests.'},
                 {b'priority': 40, 
                    b'weight': 50, 
                    b'port': 60, 
                    b'target': b'foo-2.unit.tests.'}]}))
    api_record.append({b'fieldType': b'PTR', 
       b'ttl': 900, 
       b'target': b'unit.tests.', 
       b'subDomain': b'4', 
       b'id': 12})
    expected.add(Record.new(zone, b'4', {b'ttl': 900, 
       b'type': b'PTR', 
       b'value': b'unit.tests.'}))
    api_record.append({b'fieldType': b'SPF', 
       b'ttl': 1000, 
       b'target': b'v=spf1 include:unit.texts.redirect ~all', 
       b'subDomain': b'', 
       b'id': 13})
    expected.add(Record.new(zone, b'', {b'ttl': 1000, 
       b'type': b'SPF', 
       b'value': b'v=spf1 include:unit.texts.redirect ~all'}))
    api_record.append({b'fieldType': b'SSHFP', 
       b'ttl': 1100, 
       b'target': b'1 1 bf6b6825d2977c511a475bbefb88aad54a92ac73 ', 
       b'subDomain': b'', 
       b'id': 14})
    expected.add(Record.new(zone, b'', {b'ttl': 1100, 
       b'type': b'SSHFP', 
       b'value': {b'algorithm': 1, 
                  b'fingerprint': b'bf6b6825d2977c511a475bbefb88aad54a92ac73', 
                  b'fingerprint_type': 1}}))
    api_record.append({b'fieldType': b'AAAA', 
       b'ttl': 1200, 
       b'target': b'1:1ec:1::1', 
       b'subDomain': b'', 
       b'id': 15})
    expected.add(Record.new(zone, b'', {b'ttl': 200, 
       b'type': b'AAAA', 
       b'value': b'1:1ec:1::1'}))
    api_record.append({b'fieldType': b'DKIM', 
       b'ttl': 1300, 
       b'target': valid_dkim_key, 
       b'subDomain': b'dkim', 
       b'id': 16})
    expected.add(Record.new(zone, b'dkim', {b'ttl': 1300, 
       b'type': b'TXT', 
       b'value': valid_dkim_key}))
    api_record.append({b'fieldType': b'TXT', 
       b'ttl': 1400, 
       b'target': b'TXT text', 
       b'subDomain': b'txt', 
       b'id': 17})
    expected.add(Record.new(zone, b'txt', {b'ttl': 1400, 
       b'type': b'TXT', 
       b'value': b'TXT text'}))
    api_record.append({b'fieldType': b'LOC', 
       b'ttl': 1500, 
       b'target': b'1 1 1 N 1 1 1 E 1m 1m', 
       b'subDomain': b'', 
       b'id': 18})
    api_record.append({b'fieldType': b'CAA', 
       b'ttl': 1600, 
       b'target': b'0 issue "ca.unit.tests"', 
       b'subDomain': b'caa', 
       b'id': 19})
    expected.add(Record.new(zone, b'caa', {b'ttl': 1600, 
       b'type': b'CAA', 
       b'values': [
                 {b'flags': 0, 
                    b'tag': b'issue', 
                    b'value': b'ca.unit.tests'}]}))
    valid_dkim = [
     valid_dkim_key,
     b'v=DKIM1 \\; %s' % valid_dkim_key,
     b'h=sha256 \\; %s' % valid_dkim_key,
     b'h=sha1 \\; %s' % valid_dkim_key,
     b's=* \\; %s' % valid_dkim_key,
     b's=email \\; %s' % valid_dkim_key,
     b't=y \\; %s' % valid_dkim_key,
     b't=s \\; %s' % valid_dkim_key,
     b'k=rsa \\; %s' % valid_dkim_key,
     b'n=notes \\; %s' % valid_dkim_key,
     b'g=granularity \\; %s' % valid_dkim_key]
    invalid_dkim = [
     b'p=%invalid%',
     b'v=DKIM1',
     b'v=DKIM2 \\; %s' % valid_dkim_key,
     b'h=sha512 \\; %s' % valid_dkim_key,
     b's=fake \\; %s' % valid_dkim_key,
     b't=fake \\; %s' % valid_dkim_key,
     b'u=invalid \\; %s' % valid_dkim_key]

    @patch(b'ovh.Client')
    def test_populate(self, client_mock):
        provider = OvhProvider(b'test', b'endpoint', b'application_key', b'application_secret', b'consumer_key')
        with patch.object(provider._client, b'get') as (get_mock):
            zone = Zone(b'unit.tests.', [])
            get_mock.side_effect = ResourceNotFoundError(b'boom')
            with self.assertRaises(APIError) as (ctx):
                provider.populate(zone)
            self.assertEquals(get_mock.side_effect, ctx.exception)
            get_mock.side_effect = InvalidCredential(b'boom')
            with self.assertRaises(APIError) as (ctx):
                provider.populate(zone)
            self.assertEquals(get_mock.side_effect, ctx.exception)
            zone = Zone(b'unit.tests.', [])
            get_mock.side_effect = ResourceNotFoundError(b'This service does not exist')
            exists = provider.populate(zone)
            self.assertEquals(set(), zone.records)
            self.assertFalse(exists)
            zone = Zone(b'unit.tests.', [])
            get_returns = [[ record[b'id'] for record in self.api_record ]]
            get_returns += self.api_record
            get_mock.side_effect = get_returns
            exists = provider.populate(zone)
            self.assertEquals(self.expected, zone.records)
            self.assertTrue(exists)

    @patch(b'ovh.Client')
    def test_is_valid_dkim(self, client_mock):
        """Test _is_valid_dkim"""
        provider = OvhProvider(b'test', b'endpoint', b'application_key', b'application_secret', b'consumer_key')
        for dkim in self.valid_dkim:
            self.assertTrue(provider._is_valid_dkim(dkim))

        for dkim in self.invalid_dkim:
            self.assertFalse(provider._is_valid_dkim(dkim))

    @patch(b'ovh.Client')
    def test_apply(self, client_mock):
        provider = OvhProvider(b'test', b'endpoint', b'application_key', b'application_secret', b'consumer_key')
        desired = Zone(b'unit.tests.', [])
        for r in self.expected:
            desired.add_record(r)

        with patch.object(provider._client, b'post') as (get_mock):
            plan = provider.plan(desired)
            get_mock.side_effect = APIError(b'boom')
            with self.assertRaises(APIError) as (ctx):
                provider.apply(plan)
            self.assertEquals(get_mock.side_effect, ctx.exception)
        with patch.object(provider._client, b'get') as (get_mock):
            get_returns = [[1, 2, 3, 4],
             {b'fieldType': b'A', b'ttl': 600, b'target': b'5.6.7.8', b'subDomain': b'', 
                b'id': 100},
             {b'fieldType': b'A', b'ttl': 600, b'target': b'5.6.7.8', b'subDomain': b'fake', 
                b'id': 101},
             {b'fieldType': b'TXT', b'ttl': 600, b'target': b'fake txt record', b'subDomain': b'txt', 
                b'id': 102},
             {b'fieldType': b'DKIM', b'ttl': 600, b'target': b'v=DKIM1; %s' % self.valid_dkim_key, 
                b'subDomain': b'dkim', 
                b'id': 103}]
            get_mock.side_effect = get_returns
            plan = provider.plan(desired)
            with patch.object(provider._client, b'post') as (post_mock):
                with patch.object(provider._client, b'delete') as (delete_mock):
                    get_mock.side_effect = [
                     [
                      100], [101], [102], [103]]
                    provider.apply(plan)
                    wanted_calls = [
                     call(b'/domain/zone/unit.tests/record', fieldType=b'A', subDomain=b'', target=b'1.2.3.4', ttl=100),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'AAAA', subDomain=b'', target=b'1:1ec:1::1', ttl=200),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'MX', subDomain=b'', target=b'10 mx1.unit.tests.', ttl=400),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'SPF', subDomain=b'', target=b'v=spf1 include:unit.texts.redirect ~all', ttl=1000),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'SSHFP', subDomain=b'', target=b'1 1 bf6b6825d2977c511a475bbefb88aad54a92ac73', ttl=1100),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'PTR', subDomain=b'4', target=b'unit.tests.', ttl=900),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'SRV', subDomain=b'_srv._tcp', target=b'10 20 30 foo-1.unit.tests.', ttl=800),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'SRV', subDomain=b'_srv._tcp', target=b'40 50 60 foo-2.unit.tests.', ttl=800),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'CAA', subDomain=b'caa', target=b'0 issue "ca.unit.tests"', ttl=1600),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'DKIM', subDomain=b'dkim', target=b'p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCxLaG16G4SaEcXVdiIxTg7gKSGbHKQLm30CHib1h9FzS9nkcyvQSyQj1rMFyqC//tft3ohx3nvJl+bGCWxdtLYDSmir9PW54e5CTdxEh8MWRkBO3StF6QG/tAh3aTGDmkqhIJGLb87iHvpmVKqURmEUzJPv5KPJfWLofADI+q9lQIDAQAB', ttl=1300),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'NAPTR', subDomain=b'naptr', target=b'10 100 "S" "SIP+D2U" "!^.*$!sip:info@bar.example.com!" .', ttl=500),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'A', subDomain=b'sub', target=b'1.2.3.4', ttl=200),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'TXT', subDomain=b'txt', target=b'TXT text', ttl=1400),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'CNAME', subDomain=b'www2', target=b'unit.tests.', ttl=300),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'NS', subDomain=b'www3', target=b'ns3.unit.tests.', ttl=700),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'NS', subDomain=b'www3', target=b'ns4.unit.tests.', ttl=700),
                     call(b'/domain/zone/unit.tests/refresh')]
                    post_mock.assert_has_calls(wanted_calls)
                    wanted_get_calls = [
                     call(b'/domain/zone/unit.tests/record', fieldType=b'A', subDomain=b''),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'DKIM', subDomain=b'dkim'),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'A', subDomain=b'fake'),
                     call(b'/domain/zone/unit.tests/record', fieldType=b'TXT', subDomain=b'txt')]
                    get_mock.assert_has_calls(wanted_get_calls)
                    delete_mock.assert_has_calls([
                     call(b'/domain/zone/unit.tests/record/100'),
                     call(b'/domain/zone/unit.tests/record/101'),
                     call(b'/domain/zone/unit.tests/record/102'),
                     call(b'/domain/zone/unit.tests/record/103')])