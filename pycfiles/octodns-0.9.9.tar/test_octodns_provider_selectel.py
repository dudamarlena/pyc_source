# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_selectel.py
# Compiled at: 2019-10-18 13:06:59
from __future__ import absolute_import, division, print_function, unicode_literals
from unittest import TestCase
from six import text_type
import requests_mock
from octodns.provider.selectel import SelectelProvider
from octodns.record import Record, Update
from octodns.zone import Zone

class TestSelectelProvider(TestCase):
    API_URL = b'https://api.selectel.ru/domains/v1'
    api_record = []
    zone = Zone(b'unit.tests.', [])
    expected = set()
    domain = [{b'name': b'unit.tests', b'id': 100000}]
    api_record.append({b'type': b'A', 
       b'ttl': 100, 
       b'content': b'1.2.3.4', 
       b'name': b'unit.tests', 
       b'id': 1})
    expected.add(Record.new(zone, b'', {b'ttl': 100, 
       b'type': b'A', 
       b'value': b'1.2.3.4'}))
    api_record.append({b'type': b'A', 
       b'ttl': 200, 
       b'content': b'1.2.3.4', 
       b'name': b'sub.unit.tests', 
       b'id': 2})
    expected.add(Record.new(zone, b'sub', {b'ttl': 200, 
       b'type': b'A', 
       b'value': b'1.2.3.4'}))
    api_record.append({b'type': b'CNAME', 
       b'ttl': 300, 
       b'content': b'unit.tests', 
       b'name': b'www2.unit.tests', 
       b'id': 3})
    expected.add(Record.new(zone, b'www2', {b'ttl': 300, 
       b'type': b'CNAME', 
       b'value': b'unit.tests.'}))
    api_record.append({b'type': b'MX', 
       b'ttl': 400, 
       b'content': b'mx1.unit.tests', 
       b'priority': 10, 
       b'name': b'unit.tests', 
       b'id': 4})
    expected.add(Record.new(zone, b'', {b'ttl': 400, 
       b'type': b'MX', 
       b'values': [
                 {b'preference': 10, 
                    b'exchange': b'mx1.unit.tests.'}]}))
    api_record.append({b'type': b'NS', 
       b'ttl': 600, 
       b'content': b'ns1.unit.tests', 
       b'name': b'unit.tests.', 
       b'id': 6})
    api_record.append({b'type': b'NS', 
       b'ttl': 600, 
       b'content': b'ns2.unit.tests', 
       b'name': b'unit.tests', 
       b'id': 7})
    expected.add(Record.new(zone, b'', {b'ttl': 600, 
       b'type': b'NS', 
       b'values': [
                 b'ns1.unit.tests.', b'ns2.unit.tests.']}))
    api_record.append({b'type': b'NS', 
       b'ttl': 700, 
       b'content': b'ns3.unit.tests', 
       b'name': b'www3.unit.tests', 
       b'id': 8})
    api_record.append({b'type': b'NS', 
       b'ttl': 700, 
       b'content': b'ns4.unit.tests', 
       b'name': b'www3.unit.tests', 
       b'id': 9})
    expected.add(Record.new(zone, b'www3', {b'ttl': 700, 
       b'type': b'NS', 
       b'values': [
                 b'ns3.unit.tests.', b'ns4.unit.tests.']}))
    api_record.append({b'type': b'SRV', 
       b'ttl': 800, 
       b'target': b'foo-1.unit.tests', 
       b'weight': 20, 
       b'priority': 10, 
       b'port': 30, 
       b'id': 10, 
       b'name': b'_srv._tcp.unit.tests'})
    api_record.append({b'type': b'SRV', 
       b'ttl': 800, 
       b'target': b'foo-2.unit.tests', 
       b'name': b'_srv._tcp.unit.tests', 
       b'weight': 50, 
       b'priority': 40, 
       b'port': 60, 
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
    aaaa_record = {b'type': b'AAAA', 
       b'ttl': 200, 
       b'content': b'1:1ec:1::1', 
       b'name': b'unit.tests', 
       b'id': 15}
    api_record.append(aaaa_record)
    expected.add(Record.new(zone, b'', {b'ttl': 200, 
       b'type': b'AAAA', 
       b'value': b'1:1ec:1::1'}))
    api_record.append({b'type': b'TXT', 
       b'ttl': 300, 
       b'content': b'little text', 
       b'name': b'text.unit.tests', 
       b'id': 16})
    expected.add(Record.new(zone, b'text', {b'ttl': 200, 
       b'type': b'TXT', 
       b'value': b'little text'}))

    @requests_mock.Mocker()
    def test_populate(self, fake_http):
        zone = Zone(b'unit.tests.', [])
        fake_http.get((b'{}/unit.tests/records/').format(self.API_URL), json=self.api_record)
        fake_http.get((b'{}/').format(self.API_URL), json=self.domain)
        fake_http.head((b'{}/unit.tests/records/').format(self.API_URL), headers={b'X-Total-Count': str(len(self.api_record))})
        fake_http.head((b'{}/').format(self.API_URL), headers={b'X-Total-Count': str(len(self.domain))})
        provider = SelectelProvider(123, b'secret_token')
        provider.populate(zone)
        self.assertEquals(self.expected, zone.records)

    @requests_mock.Mocker()
    def test_populate_invalid_record(self, fake_http):
        more_record = self.api_record
        more_record.append({b'name': b'unit.tests', b'id': 100001, 
           b'content': b'support.unit.tests.', 
           b'ttl': 300, 
           b'ns': b'ns1.unit.tests', b'type': b'SOA', 
           b'email': b'support@unit.tests'})
        zone = Zone(b'unit.tests.', [])
        fake_http.get((b'{}/unit.tests/records/').format(self.API_URL), json=more_record)
        fake_http.get((b'{}/').format(self.API_URL), json=self.domain)
        fake_http.head((b'{}/unit.tests/records/').format(self.API_URL), headers={b'X-Total-Count': str(len(self.api_record))})
        fake_http.head((b'{}/').format(self.API_URL), headers={b'X-Total-Count': str(len(self.domain))})
        zone.add_record(Record.new(self.zone, b'unsup', {b'ttl': 200, 
           b'type': b'NAPTR', 
           b'value': {b'order': 40, 
                      b'preference': 70, 
                      b'flags': b'U', 
                      b'service': b'SIP+D2U', 
                      b'regexp': b'!^.*$!sip:info@bar.example.com!', 
                      b'replacement': b'.'}}))
        provider = SelectelProvider(123, b'secret_token')
        provider.populate(zone)
        self.assertNotEqual(self.expected, zone.records)

    @requests_mock.Mocker()
    def test_apply(self, fake_http):
        fake_http.get((b'{}/unit.tests/records/').format(self.API_URL), json=list())
        fake_http.get((b'{}/').format(self.API_URL), json=self.domain)
        fake_http.head((b'{}/unit.tests/records/').format(self.API_URL), headers={b'X-Total-Count': b'0'})
        fake_http.head((b'{}/').format(self.API_URL), headers={b'X-Total-Count': str(len(self.domain))})
        fake_http.post((b'{}/100000/records/').format(self.API_URL), json=list())
        provider = SelectelProvider(123, b'test_token')
        zone = Zone(b'unit.tests.', [])
        for record in self.expected:
            zone.add_record(record)

        plan = provider.plan(zone)
        self.assertEquals(8, len(plan.changes))
        self.assertEquals(8, provider.apply(plan))

    @requests_mock.Mocker()
    def test_domain_list(self, fake_http):
        fake_http.get((b'{}/').format(self.API_URL), json=self.domain)
        fake_http.head((b'{}/').format(self.API_URL), headers={b'X-Total-Count': str(len(self.domain))})
        expected = {b'unit.tests': self.domain[0]}
        provider = SelectelProvider(123, b'test_token')
        result = provider.domain_list()
        self.assertEquals(result, expected)

    @requests_mock.Mocker()
    def test_authentication_fail(self, fake_http):
        fake_http.get((b'{}/').format(self.API_URL), status_code=401)
        fake_http.head((b'{}/').format(self.API_URL), headers={b'X-Total-Count': str(len(self.domain))})
        with self.assertRaises(Exception) as (ctx):
            SelectelProvider(123, b'fail_token')
        self.assertEquals(text_type(ctx.exception), b'Authorization failed. Invalid or empty token.')

    @requests_mock.Mocker()
    def test_not_exist_domain(self, fake_http):
        fake_http.get((b'{}/').format(self.API_URL), status_code=404, json=b'')
        fake_http.head((b'{}/').format(self.API_URL), headers={b'X-Total-Count': str(len(self.domain))})
        fake_http.post((b'{}/').format(self.API_URL), json={b'name': b'unit.tests', b'create_date': 1507154178, 
           b'id': 100000})
        fake_http.get((b'{}/unit.tests/records/').format(self.API_URL), json=list())
        fake_http.head((b'{}/unit.tests/records/').format(self.API_URL), headers={b'X-Total-Count': str(len(self.api_record))})
        fake_http.post((b'{}/100000/records/').format(self.API_URL), json=list())
        provider = SelectelProvider(123, b'test_token')
        zone = Zone(b'unit.tests.', [])
        for record in self.expected:
            zone.add_record(record)

        plan = provider.plan(zone)
        self.assertEquals(8, len(plan.changes))
        self.assertEquals(8, provider.apply(plan))

    @requests_mock.Mocker()
    def test_delete_no_exist_record(self, fake_http):
        fake_http.get((b'{}/').format(self.API_URL), json=self.domain)
        fake_http.get((b'{}/100000/records/').format(self.API_URL), json=list())
        fake_http.head((b'{}/').format(self.API_URL), headers={b'X-Total-Count': str(len(self.domain))})
        fake_http.head((b'{}/unit.tests/records/').format(self.API_URL), headers={b'X-Total-Count': b'0'})
        provider = SelectelProvider(123, b'test_token')
        zone = Zone(b'unit.tests.', [])
        provider.delete_record(b'unit.tests', b'NS', zone)

    @requests_mock.Mocker()
    def test_change_record(self, fake_http):
        exist_record = [self.aaaa_record,
         {b'content': b'6.6.5.7', b'ttl': 100, 
            b'type': b'A', 
            b'id': 100001, 
            b'name': b'delete.unit.tests'},
         {b'content': b'9.8.2.1', b'ttl': 100, 
            b'type': b'A', 
            b'id': 100002, 
            b'name': b'unit.tests'}]
        fake_http.get((b'{}/unit.tests/records/').format(self.API_URL), json=exist_record)
        fake_http.get((b'{}/').format(self.API_URL), json=self.domain)
        fake_http.get((b'{}/100000/records/').format(self.API_URL), json=exist_record)
        fake_http.head((b'{}/unit.tests/records/').format(self.API_URL), headers={b'X-Total-Count': str(len(exist_record))})
        fake_http.head((b'{}/').format(self.API_URL), headers={b'X-Total-Count': str(len(self.domain))})
        fake_http.head((b'{}/100000/records/').format(self.API_URL), headers={b'X-Total-Count': str(len(exist_record))})
        fake_http.post((b'{}/100000/records/').format(self.API_URL), json=list())
        fake_http.delete((b'{}/100000/records/100001').format(self.API_URL), text=b'')
        fake_http.delete((b'{}/100000/records/100002').format(self.API_URL), text=b'')
        provider = SelectelProvider(123, b'test_token')
        zone = Zone(b'unit.tests.', [])
        for record in self.expected:
            zone.add_record(record)

        plan = provider.plan(zone)
        self.assertEquals(8, len(plan.changes))
        self.assertEquals(8, provider.apply(plan))

    @requests_mock.Mocker()
    def test_include_change_returns_false(self, fake_http):
        fake_http.get((b'{}/').format(self.API_URL), json=self.domain)
        fake_http.head((b'{}/').format(self.API_URL), headers={b'X-Total-Count': str(len(self.domain))})
        provider = SelectelProvider(123, b'test_token')
        zone = Zone(b'unit.tests.', [])
        exist_record = Record.new(zone, b'', {b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1', b'2.2.2.2']})
        new = Record.new(zone, b'', {b'ttl': 10, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1', b'2.2.2.2']})
        change = Update(exist_record, new)
        include_change = provider._include_change(change)
        self.assertFalse(include_change)