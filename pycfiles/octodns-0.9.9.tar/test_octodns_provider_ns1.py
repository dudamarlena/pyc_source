# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_ns1.py
# Compiled at: 2019-10-18 13:06:59
from __future__ import absolute_import, division, print_function, unicode_literals
from collections import defaultdict
from mock import Mock, call, patch
from ns1.rest.errors import AuthException, RateLimitException, ResourceException
from unittest import TestCase
from octodns.record import Delete, Record, Update
from octodns.provider.ns1 import Ns1Provider
from octodns.zone import Zone

class DummyZone(object):

    def __init__(self, records):
        self.data = {b'records': records}


class TestNs1Provider(TestCase):
    zone = Zone(b'unit.tests.', [])
    expected = set()
    expected.add(Record.new(zone, b'', {b'ttl': 32, 
       b'type': b'A', 
       b'value': b'1.2.3.4', 
       b'meta': {}}))
    expected.add(Record.new(zone, b'foo', {b'ttl': 33, 
       b'type': b'A', 
       b'values': [
                 b'1.2.3.4', b'1.2.3.5'], 
       b'meta': {}}))
    expected.add(Record.new(zone, b'geo', {b'ttl': 34, 
       b'type': b'A', 
       b'values': [
                 b'101.102.103.104', b'101.102.103.105'], 
       b'geo': {b'NA-US-NY': [b'201.202.203.204']}, b'meta': {}}))
    expected.add(Record.new(zone, b'cname', {b'ttl': 34, 
       b'type': b'CNAME', 
       b'value': b'foo.unit.tests.'}))
    expected.add(Record.new(zone, b'', {b'ttl': 35, 
       b'type': b'MX', 
       b'values': [
                 {b'preference': 10, 
                    b'exchange': b'mx1.unit.tests.'},
                 {b'preference': 20, 
                    b'exchange': b'mx2.unit.tests.'}]}))
    expected.add(Record.new(zone, b'naptr', {b'ttl': 36, 
       b'type': b'NAPTR', 
       b'values': [
                 {b'flags': b'U', 
                    b'order': 100, 
                    b'preference': 100, 
                    b'regexp': b'!^.*$!sip:info@bar.example.com!', 
                    b'replacement': b'.', 
                    b'service': b'SIP+D2U'},
                 {b'flags': b'S', 
                    b'order': 10, 
                    b'preference': 100, 
                    b'regexp': b'!^.*$!sip:info@bar.example.com!', 
                    b'replacement': b'.', 
                    b'service': b'SIP+D2U'}]}))
    expected.add(Record.new(zone, b'', {b'ttl': 37, 
       b'type': b'NS', 
       b'values': [
                 b'ns1.unit.tests.', b'ns2.unit.tests.']}))
    expected.add(Record.new(zone, b'_srv._tcp', {b'ttl': 38, 
       b'type': b'SRV', 
       b'values': [
                 {b'priority': 10, 
                    b'weight': 20, 
                    b'port': 30, 
                    b'target': b'foo-1.unit.tests.'},
                 {b'priority': 12, 
                    b'weight': 30, 
                    b'port': 30, 
                    b'target': b'foo-2.unit.tests.'}]}))
    expected.add(Record.new(zone, b'sub', {b'ttl': 39, 
       b'type': b'NS', 
       b'values': [
                 b'ns3.unit.tests.', b'ns4.unit.tests.']}))
    expected.add(Record.new(zone, b'', {b'ttl': 40, 
       b'type': b'CAA', 
       b'value': {b'flags': 0, 
                  b'tag': b'issue', 
                  b'value': b'ca.unit.tests'}}))
    nsone_records = [
     {b'type': b'A', 
        b'ttl': 32, 
        b'short_answers': [
                         b'1.2.3.4'], 
        b'domain': b'unit.tests.'},
     {b'type': b'A', 
        b'ttl': 33, 
        b'short_answers': [
                         b'1.2.3.4', b'1.2.3.5'], 
        b'domain': b'foo.unit.tests.'},
     {b'type': b'A', 
        b'ttl': 34, 
        b'short_answers': [
                         b'101.102.103.104', b'101.102.103.105'], 
        b'domain': b'geo.unit.tests'},
     {b'type': b'CNAME', 
        b'ttl': 34, 
        b'short_answers': [
                         b'foo.unit.tests'], 
        b'domain': b'cname.unit.tests.'},
     {b'type': b'MX', 
        b'ttl': 35, 
        b'short_answers': [
                         b'10 mx1.unit.tests.', b'20 mx2.unit.tests'], 
        b'domain': b'unit.tests.'},
     {b'type': b'NAPTR', 
        b'ttl': 36, 
        b'short_answers': [
                         b'10 100 S SIP+D2U !^.*$!sip:info@bar.example.com! .',
                         b'100 100 U SIP+D2U !^.*$!sip:info@bar.example.com! .'], 
        b'domain': b'naptr.unit.tests.'},
     {b'type': b'NS', 
        b'ttl': 37, 
        b'short_answers': [
                         b'ns1.unit.tests.', b'ns2.unit.tests'], 
        b'domain': b'unit.tests.'},
     {b'type': b'SRV', 
        b'ttl': 38, 
        b'short_answers': [
                         b'12 30 30 foo-2.unit.tests.',
                         b'10 20 30 foo-1.unit.tests'], 
        b'domain': b'_srv._tcp.unit.tests.'},
     {b'type': b'NS', 
        b'ttl': 39, 
        b'short_answers': [
                         b'ns3.unit.tests.', b'ns4.unit.tests'], 
        b'domain': b'sub.unit.tests.'},
     {b'type': b'CAA', 
        b'ttl': 40, 
        b'short_answers': [
                         b'0 issue ca.unit.tests'], 
        b'domain': b'unit.tests.'}]

    @patch(b'ns1.NS1.loadZone')
    def test_populate(self, load_mock):
        provider = Ns1Provider(b'test', b'api-key')
        load_mock.side_effect = AuthException(b'unauthorized')
        zone = Zone(b'unit.tests.', [])
        with self.assertRaises(AuthException) as (ctx):
            provider.populate(zone)
        self.assertEquals(load_mock.side_effect, ctx.exception)
        load_mock.reset_mock()
        load_mock.side_effect = ResourceException(b'boom')
        zone = Zone(b'unit.tests.', [])
        with self.assertRaises(ResourceException) as (ctx):
            provider.populate(zone)
        self.assertEquals(load_mock.side_effect, ctx.exception)
        self.assertEquals(('unit.tests', ), load_mock.call_args[0])
        load_mock.reset_mock()
        load_mock.side_effect = ResourceException(b'server error: zone not found')
        zone = Zone(b'unit.tests.', [])
        exists = provider.populate(zone)
        self.assertEquals(set(), zone.records)
        self.assertEquals(('unit.tests', ), load_mock.call_args[0])
        self.assertFalse(exists)
        load_mock.reset_mock()
        nsone_zone = DummyZone([])
        load_mock.side_effect = [nsone_zone]
        zone_search = Mock()
        zone_search.return_value = [
         {b'domain': b'geo.unit.tests', 
            b'zone': b'unit.tests', 
            b'type': b'A', 
            b'answers': [{b'answer': [b'1.1.1.1'], b'meta': {}}, {b'answer': [b'1.2.3.4'], b'meta': {b'ca_province': [b'ON']}}, {b'answer': [b'2.3.4.5'], b'meta': {b'us_state': [b'NY']}}, {b'answer': [b'3.4.5.6'], b'meta': {b'country': [b'US']}}, {b'answer': [b'4.5.6.7'], b'meta': {b'iso_region_code': [b'NA-US-WA']}}], b'ttl': 34}]
        nsone_zone.search = zone_search
        zone = Zone(b'unit.tests.', [])
        provider.populate(zone)
        self.assertEquals(1, len(zone.records))
        self.assertEquals(('unit.tests', ), load_mock.call_args[0])
        load_mock.reset_mock()
        nsone_zone = DummyZone(self.nsone_records)
        load_mock.side_effect = [nsone_zone]
        zone_search = Mock()
        zone_search.return_value = [
         {b'domain': b'geo.unit.tests', 
            b'zone': b'unit.tests', 
            b'type': b'A', 
            b'answers': [{b'answer': [b'1.1.1.1'], b'meta': {}}, {b'answer': [b'1.2.3.4'], b'meta': {b'ca_province': [b'ON']}}, {b'answer': [b'2.3.4.5'], b'meta': {b'us_state': [b'NY']}}, {b'answer': [b'3.4.5.6'], b'meta': {b'country': [b'US']}}, {b'answer': [b'4.5.6.7'], b'meta': {b'iso_region_code': [b'NA-US-WA']}}], b'ttl': 34}]
        nsone_zone.search = zone_search
        zone = Zone(b'unit.tests.', [])
        provider.populate(zone)
        self.assertEquals(self.expected, zone.records)
        self.assertEquals(('unit.tests', ), load_mock.call_args[0])
        load_mock.reset_mock()
        nsone_zone = DummyZone(self.nsone_records + [
         {b'type': b'UNSUPPORTED', 
            b'ttl': 42, 
            b'short_answers': [
                             b'unsupported'], 
            b'domain': b'unsupported.unit.tests.'}])
        load_mock.side_effect = [
         nsone_zone]
        zone_search = Mock()
        zone_search.return_value = [
         {b'domain': b'geo.unit.tests', 
            b'zone': b'unit.tests', 
            b'type': b'A', 
            b'answers': [{b'answer': [b'1.1.1.1'], b'meta': {}}, {b'answer': [b'1.2.3.4'], b'meta': {b'ca_province': [b'ON']}}, {b'answer': [b'2.3.4.5'], b'meta': {b'us_state': [b'NY']}}, {b'answer': [b'3.4.5.6'], b'meta': {b'country': [b'US']}}, {b'answer': [b'4.5.6.7'], b'meta': {b'iso_region_code': [b'NA-US-WA']}}], b'ttl': 34}]
        nsone_zone.search = zone_search
        zone = Zone(b'unit.tests.', [])
        provider.populate(zone)
        self.assertEquals(self.expected, zone.records)
        self.assertEquals(('unit.tests', ), load_mock.call_args[0])

    @patch(b'ns1.NS1.createZone')
    @patch(b'ns1.NS1.loadZone')
    def test_sync(self, load_mock, create_mock):
        provider = Ns1Provider(b'test', b'api-key')
        desired = Zone(b'unit.tests.', [])
        for r in self.expected:
            desired.add_record(r)

        plan = provider.plan(desired)
        expected_n = len(self.expected) - 1
        self.assertEquals(expected_n, len(plan.changes))
        self.assertTrue(plan.exists)
        load_mock.reset_mock()
        create_mock.reset_mock()
        load_mock.side_effect = ResourceException(b'boom')
        with self.assertRaises(ResourceException) as (ctx):
            provider.apply(plan)
        self.assertEquals(load_mock.side_effect, ctx.exception)
        load_mock.reset_mock()
        create_mock.reset_mock()
        load_mock.side_effect = ResourceException(b'server error: zone not found')
        create_mock.side_effect = AuthException(b'unauthorized')
        with self.assertRaises(AuthException) as (ctx):
            provider.apply(plan)
        self.assertEquals(create_mock.side_effect, ctx.exception)
        load_mock.reset_mock()
        create_mock.reset_mock()
        load_mock.side_effect = ResourceException(b'server error: zone not found')
        mock_zone = Mock()
        mock_zone.add_SRV = Mock()
        mock_zone.add_SRV.side_effect = [
         RateLimitException(b'boo', period=0),
         None]
        create_mock.side_effect = [
         mock_zone]
        got_n = provider.apply(plan)
        self.assertEquals(expected_n, got_n)
        load_mock.reset_mock()
        create_mock.reset_mock()
        nsone_zone = DummyZone(self.nsone_records + [
         {b'type': b'A', 
            b'ttl': 42, 
            b'short_answers': [
                             b'9.9.9.9'], 
            b'domain': b'delete-me.unit.tests.'}])
        nsone_zone.data[b'records'][0][b'short_answers'][0] = b'2.2.2.2'
        nsone_zone.loadRecord = Mock()
        zone_search = Mock()
        zone_search.return_value = [
         {b'domain': b'geo.unit.tests', 
            b'zone': b'unit.tests', 
            b'type': b'A', 
            b'answers': [{b'answer': [b'1.1.1.1'], b'meta': {}}, {b'answer': [b'1.2.3.4'], b'meta': {b'ca_province': [b'ON']}}, {b'answer': [b'2.3.4.5'], b'meta': {b'us_state': [b'NY']}}, {b'answer': [b'3.4.5.6'], b'meta': {b'country': [b'US']}}, {b'answer': [b'4.5.6.7'], b'meta': {b'iso_region_code': [b'NA-US-WA']}}], b'ttl': 34}]
        nsone_zone.search = zone_search
        load_mock.side_effect = [nsone_zone, nsone_zone]
        plan = provider.plan(desired)
        self.assertEquals(3, len(plan.changes))
        classes = defaultdict(lambda : 0)
        for change in plan.changes:
            classes[change.__class__] += 1

        self.assertEquals(1, classes[Delete])
        self.assertEquals(2, classes[Update])
        mock_record = Mock()
        mock_record.update.side_effect = [
         RateLimitException(b'one', period=0),
         None,
         None]
        mock_record.delete.side_effect = [
         RateLimitException(b'two', period=0),
         None,
         None]
        nsone_zone.loadRecord.side_effect = [
         mock_record, mock_record,
         mock_record]
        got_n = provider.apply(plan)
        self.assertEquals(3, got_n)
        nsone_zone.loadRecord.assert_has_calls([
         call(b'unit.tests', b'A'),
         call(b'delete-me', b'A'),
         call(b'geo', b'A')])
        mock_record.assert_has_calls([
         call.update(answers=[{b'answer': [b'1.2.3.4'], b'meta': {}}], filters=[], ttl=32),
         call.update(answers=[{b'answer': [b'1.2.3.4'], b'meta': {}}], filters=[], ttl=32),
         call.delete(),
         call.delete(),
         call.update(answers=[{b'answer': [b'101.102.103.104'], b'meta': {}}, {b'answer': [b'101.102.103.105'], b'meta': {}},
          {b'answer': [
                       b'201.202.203.204'], 
             b'meta': {b'iso_region_code': [
                                          b'NA-US-NY']}}], filters=[{b'filter': b'shuffle', b'config': {}}, {b'filter': b'geotarget_country', b'config': {}}, {b'filter': b'select_first_n', b'config': {b'N': 1}}], ttl=34)])
        return

    def test_escaping(self):
        provider = Ns1Provider(b'test', b'api-key')
        record = {b'ttl': 31, 
           b'short_answers': [
                            b'foo; bar baz; blip']}
        self.assertEquals([b'foo\\; bar baz\\; blip'], provider._data_for_SPF(b'SPF', record)[b'values'])
        record = {b'ttl': 31, 
           b'short_answers': [
                            b'no', b'foo; bar baz; blip', b'yes']}
        self.assertEquals([b'no', b'foo\\; bar baz\\; blip', b'yes'], provider._data_for_TXT(b'TXT', record)[b'values'])
        zone = Zone(b'unit.tests.', [])
        record = Record.new(zone, b'spf', {b'ttl': 34, 
           b'type': b'SPF', 
           b'value': b'foo\\; bar baz\\; blip'})
        self.assertEquals([b'foo; bar baz; blip'], provider._params_for_SPF(record)[b'answers'])
        record = Record.new(zone, b'txt', {b'ttl': 35, 
           b'type': b'TXT', 
           b'value': b'foo\\; bar baz\\; blip'})
        self.assertEquals([b'foo; bar baz; blip'], provider._params_for_TXT(record)[b'answers'])

    def test_data_for_CNAME(self):
        provider = Ns1Provider(b'test', b'api-key')
        a_record = {b'ttl': 31, 
           b'type': b'CNAME', 
           b'short_answers': [
                            b'foo.unit.tests.']}
        a_expected = {b'ttl': 31, 
           b'type': b'CNAME', 
           b'value': b'foo.unit.tests.'}
        self.assertEqual(a_expected, provider._data_for_CNAME(a_record[b'type'], a_record))
        b_record = {b'ttl': 32, 
           b'type': b'CNAME', 
           b'short_answers': []}
        b_expected = {b'ttl': 32, 
           b'type': b'CNAME', 
           b'value': None}
        self.assertEqual(b_expected, provider._data_for_CNAME(b_record[b'type'], b_record))
        return