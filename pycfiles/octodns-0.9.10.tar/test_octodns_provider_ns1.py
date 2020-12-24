# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_ns1.py
# Compiled at: 2020-04-20 12:36:38
from __future__ import absolute_import, division, print_function, unicode_literals
from collections import defaultdict
from mock import call, patch
from ns1.rest.errors import AuthException, RateLimitException, ResourceException
from six import text_type
from unittest import TestCase
from octodns.record import Delete, Record, Update
from octodns.provider.ns1 import Ns1Client, Ns1Exception, Ns1Provider
from octodns.provider.plan import Plan
from octodns.zone import Zone

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
    ns1_records = [
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

    @patch(b'ns1.rest.records.Records.retrieve')
    @patch(b'ns1.rest.zones.Zones.retrieve')
    def test_populate(self, zone_retrieve_mock, record_retrieve_mock):
        provider = Ns1Provider(b'test', b'api-key')
        zone_retrieve_mock.side_effect = AuthException(b'unauthorized')
        zone = Zone(b'unit.tests.', [])
        with self.assertRaises(AuthException) as (ctx):
            provider.populate(zone)
        self.assertEquals(zone_retrieve_mock.side_effect, ctx.exception)
        zone_retrieve_mock.reset_mock()
        zone_retrieve_mock.side_effect = ResourceException(b'boom')
        zone = Zone(b'unit.tests.', [])
        with self.assertRaises(ResourceException) as (ctx):
            provider.populate(zone)
        self.assertEquals(zone_retrieve_mock.side_effect, ctx.exception)
        self.assertEquals(('unit.tests', ), zone_retrieve_mock.call_args[0])
        zone_retrieve_mock.reset_mock()
        zone_retrieve_mock.side_effect = ResourceException(b'server error: zone not found')
        zone = Zone(b'unit.tests.', [])
        exists = provider.populate(zone)
        self.assertEquals(set(), zone.records)
        self.assertEquals(('unit.tests', ), zone_retrieve_mock.call_args[0])
        self.assertFalse(exists)
        zone_retrieve_mock.reset_mock()
        record_retrieve_mock.reset_mock()
        ns1_zone = {b'records': [
                      {b'domain': b'geo.unit.tests', 
                         b'zone': b'unit.tests', 
                         b'type': b'A', 
                         b'answers': [{b'answer': [b'1.1.1.1'], b'meta': {}}, {b'answer': [b'1.2.3.4'], b'meta': {b'ca_province': [b'ON']}}, {b'answer': [b'2.3.4.5'], b'meta': {b'us_state': [b'NY']}}, {b'answer': [b'3.4.5.6'], b'meta': {b'country': [b'US']}}, {b'answer': [b'4.5.6.7'], b'meta': {b'iso_region_code': [b'NA-US-WA']}}], b'tier': 3, 
                         b'ttl': 34}]}
        zone_retrieve_mock.side_effect = [
         ns1_zone]
        record_retrieve_mock.side_effect = ns1_zone[b'records']
        zone = Zone(b'unit.tests.', [])
        provider.populate(zone)
        self.assertEquals(1, len(zone.records))
        self.assertEquals(('unit.tests', ), zone_retrieve_mock.call_args[0])
        record_retrieve_mock.assert_has_calls([
         call(b'unit.tests', b'geo.unit.tests', b'A')])
        zone_retrieve_mock.reset_mock()
        record_retrieve_mock.reset_mock()
        ns1_zone = {b'records': self.ns1_records + [
                      {b'domain': b'geo.unit.tests', 
                         b'zone': b'unit.tests', 
                         b'type': b'A', 
                         b'answers': [{b'answer': [b'1.1.1.1'], b'meta': {}}, {b'answer': [b'1.2.3.4'], b'meta': {b'ca_province': [b'ON']}}, {b'answer': [b'2.3.4.5'], b'meta': {b'us_state': [b'NY']}}, {b'answer': [b'3.4.5.6'], b'meta': {b'country': [b'US']}}, {b'answer': [b'4.5.6.7'], b'meta': {b'iso_region_code': [b'NA-US-WA']}}], b'tier': 3, 
                         b'ttl': 34}]}
        zone_retrieve_mock.side_effect = [
         ns1_zone]
        record_retrieve_mock.side_effect = ns1_zone[b'records']
        zone = Zone(b'unit.tests.', [])
        provider.populate(zone)
        self.assertEquals(self.expected, zone.records)
        self.assertEquals(('unit.tests', ), zone_retrieve_mock.call_args[0])
        record_retrieve_mock.assert_has_calls([
         call(b'unit.tests', b'geo.unit.tests', b'A')])
        zone_retrieve_mock.reset_mock()
        record_retrieve_mock.reset_mock()
        ns1_zone = {b'records': self.ns1_records + [
                      {b'type': b'UNSUPPORTED', 
                         b'ttl': 42, 
                         b'short_answers': [
                                          b'unsupported'], 
                         b'domain': b'unsupported.unit.tests.'},
                      {b'domain': b'geo.unit.tests', 
                         b'zone': b'unit.tests', 
                         b'type': b'A', 
                         b'answers': [{b'answer': [b'1.1.1.1'], b'meta': {}}, {b'answer': [b'1.2.3.4'], b'meta': {b'ca_province': [b'ON']}}, {b'answer': [b'2.3.4.5'], b'meta': {b'us_state': [b'NY']}}, {b'answer': [b'3.4.5.6'], b'meta': {b'country': [b'US']}}, {b'answer': [b'4.5.6.7'], b'meta': {b'iso_region_code': [b'NA-US-WA']}}], b'tier': 3, 
                         b'ttl': 34}]}
        zone_retrieve_mock.side_effect = [
         ns1_zone]
        zone = Zone(b'unit.tests.', [])
        provider.populate(zone)
        self.assertEquals(self.expected, zone.records)
        self.assertEquals(('unit.tests', ), zone_retrieve_mock.call_args[0])
        record_retrieve_mock.assert_has_calls([
         call(b'unit.tests', b'geo.unit.tests', b'A')])

    @patch(b'ns1.rest.records.Records.delete')
    @patch(b'ns1.rest.records.Records.update')
    @patch(b'ns1.rest.records.Records.create')
    @patch(b'ns1.rest.records.Records.retrieve')
    @patch(b'ns1.rest.zones.Zones.create')
    @patch(b'ns1.rest.zones.Zones.retrieve')
    def test_sync(self, zone_retrieve_mock, zone_create_mock, record_retrieve_mock, record_create_mock, record_update_mock, record_delete_mock):
        provider = Ns1Provider(b'test', b'api-key')
        desired = Zone(b'unit.tests.', [])
        for r in self.expected:
            desired.add_record(r)

        plan = provider.plan(desired)
        expected_n = len(self.expected) - 1
        self.assertEquals(expected_n, len(plan.changes))
        self.assertTrue(plan.exists)
        zone_retrieve_mock.reset_mock()
        record_retrieve_mock.reset_mock()
        zone_create_mock.reset_mock()
        zone_retrieve_mock.side_effect = ResourceException(b'boom')
        with self.assertRaises(ResourceException) as (ctx):
            provider.apply(plan)
        self.assertEquals(zone_retrieve_mock.side_effect, ctx.exception)
        zone_retrieve_mock.reset_mock()
        record_retrieve_mock.reset_mock()
        zone_create_mock.reset_mock()
        zone_retrieve_mock.side_effect = ResourceException(b'server error: zone not found')
        zone_create_mock.side_effect = AuthException(b'unauthorized')
        with self.assertRaises(AuthException) as (ctx):
            provider.apply(plan)
        self.assertEquals(zone_create_mock.side_effect, ctx.exception)
        zone_retrieve_mock.reset_mock()
        record_retrieve_mock.reset_mock()
        zone_create_mock.reset_mock()
        zone_retrieve_mock.side_effect = ResourceException(b'server error: zone not found')
        zone_create_mock.side_effect = [
         b'foo']
        record_create_mock.side_effect = [
         RateLimitException(b'boo', period=0)] + [
         None] * 9
        got_n = provider.apply(plan)
        self.assertEquals(expected_n, got_n)
        zone_create_mock.assert_has_calls([call(b'unit.tests')])
        record_create_mock.assert_has_calls([
         call(b'unit.tests', b'unit.tests', b'A', answers=[{b'answer': [b'1.2.3.4'], b'meta': {}}], filters=[], ttl=32),
         call(b'unit.tests', b'unit.tests', b'CAA', answers=[
          (0, 'issue', 'ca.unit.tests')], ttl=40),
         call(b'unit.tests', b'unit.tests', b'MX', answers=[
          (10, 'mx1.unit.tests.'), (20, 'mx2.unit.tests.')], ttl=35)])
        zone_retrieve_mock.reset_mock()
        record_retrieve_mock.reset_mock()
        zone_create_mock.reset_mock()
        ns1_zone = {b'records': self.ns1_records + [
                      {b'type': b'A', 
                         b'ttl': 42, 
                         b'short_answers': [
                                          b'9.9.9.9'], 
                         b'domain': b'delete-me.unit.tests.'},
                      {b'domain': b'geo.unit.tests', 
                         b'zone': b'unit.tests', 
                         b'type': b'A', 
                         b'short_answers': [
                                          b'1.1.1.1',
                                          b'1.2.3.4',
                                          b'2.3.4.5',
                                          b'3.4.5.6',
                                          b'4.5.6.7'], 
                         b'tier': 3, 
                         b'ttl': 34}]}
        ns1_zone[b'records'][0][b'short_answers'][0] = b'2.2.2.2'
        ns1_record = {b'domain': b'geo.unit.tests', 
           b'zone': b'unit.tests', 
           b'type': b'A', 
           b'answers': [{b'answer': [b'1.1.1.1'], b'meta': {}}, {b'answer': [b'1.2.3.4'], b'meta': {b'ca_province': [b'ON']}}, {b'answer': [b'2.3.4.5'], b'meta': {b'us_state': [b'NY']}}, {b'answer': [b'3.4.5.6'], b'meta': {b'country': [b'US']}}, {b'answer': [b'4.5.6.7'], b'meta': {b'iso_region_code': [b'NA-US-WA']}}], b'tier': 3, 
           b'ttl': 34}
        record_retrieve_mock.side_effect = [
         ns1_record, ns1_record]
        zone_retrieve_mock.side_effect = [ns1_zone, ns1_zone]
        plan = provider.plan(desired)
        self.assertEquals(3, len(plan.changes))
        classes = defaultdict(lambda : 0)
        for change in plan.changes:
            classes[change.__class__] += 1

        self.assertEquals(1, classes[Delete])
        self.assertEquals(2, classes[Update])
        record_update_mock.side_effect = [
         RateLimitException(b'one', period=0),
         None,
         None]
        record_delete_mock.side_effect = [
         RateLimitException(b'two', period=0),
         None,
         None]
        record_retrieve_mock.side_effect = [
         ns1_record, ns1_record]
        zone_retrieve_mock.side_effect = [ns1_zone, ns1_zone]
        got_n = provider.apply(plan)
        self.assertEquals(3, got_n)
        record_update_mock.assert_has_calls([
         call(b'unit.tests', b'unit.tests', b'A', answers=[{b'answer': [b'1.2.3.4'], b'meta': {}}], filters=[], ttl=32),
         call(b'unit.tests', b'unit.tests', b'A', answers=[{b'answer': [b'1.2.3.4'], b'meta': {}}], filters=[], ttl=32),
         call(b'unit.tests', b'geo.unit.tests', b'A', answers=[{b'answer': [b'101.102.103.104'], b'meta': {}}, {b'answer': [b'101.102.103.105'], b'meta': {}},
          {b'answer': [
                       b'201.202.203.204'], 
             b'meta': {b'iso_region_code': [b'NA-US-NY']}}], filters=[{b'filter': b'shuffle', b'config': {}}, {b'filter': b'geotarget_country', b'config': {}}, {b'filter': b'select_first_n', b'config': {b'N': 1}}], ttl=34)])
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
        params, _ = provider._params_for_SPF(record)
        self.assertEquals([b'foo; bar baz; blip'], params[b'answers'])
        record = Record.new(zone, b'txt', {b'ttl': 35, 
           b'type': b'TXT', 
           b'value': b'foo\\; bar baz\\; blip'})
        params, _ = provider._params_for_SPF(record)
        self.assertEquals([b'foo; bar baz; blip'], params[b'answers'])

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


class TestNs1ProviderDynamic(TestCase):
    zone = Zone(b'unit.tests.', [])
    record = Record.new(zone, b'', {b'dynamic': {b'pools': {b'lhr': {b'fallback': b'iad', 
                                        b'values': [
                                                  {b'value': b'3.4.5.6'}]}, 
                               b'iad': {b'values': [
                                                  {b'value': b'1.2.3.4'},
                                                  {b'value': b'2.3.4.5'}]}}, 
                    b'rules': [
                             {b'geos': [
                                        b'AF',
                                        b'EU-GB',
                                        b'NA-US-FL'], 
                                b'pool': b'lhr'},
                             {b'geos': [
                                        b'AF-ZW'], 
                                b'pool': b'iad'},
                             {b'pool': b'iad'}]}, 
       b'octodns': {b'healthcheck': {b'host': b'send.me', 
                                     b'path': b'/_ping', 
                                     b'port': 80, 
                                     b'protocol': b'HTTP'}}, 
       b'ttl': 32, 
       b'type': b'A', 
       b'value': b'1.2.3.4', 
       b'meta': {}})

    def test_notes(self):
        provider = Ns1Provider(b'test', b'api-key')
        self.assertEquals({}, provider._parse_notes(None))
        self.assertEquals({}, provider._parse_notes(b''))
        self.assertEquals({}, provider._parse_notes(b'blah-blah-blah'))
        data = {b'key': b'value', 
           b'priority': b'1'}
        notes = provider._encode_notes(data)
        self.assertEquals(data, provider._parse_notes(notes))
        return

    def test_monitors_for(self):
        provider = Ns1Provider(b'test', b'api-key')
        monitor_one = {b'config': {b'host': b'1.2.3.4'}, 
           b'notes': b'host:unit.tests type:A'}
        monitor_four = {b'config': {b'host': b'2.3.4.5'}, 
           b'notes': b'host:unit.tests type:A'}
        provider._client._monitors_cache = {b'one': monitor_one, 
           b'two': {b'config': {b'host': b'8.8.8.8'}, 
                    b'notes': b'host:unit.tests type:AAAA'}, 
           b'three': {b'config': {b'host': b'9.9.9.9'}, 
                      b'notes': b'host:other.unit.tests type:A'}, 
           b'four': monitor_four}
        record = Record.new(self.zone, b'', {b'ttl': 32, 
           b'type': b'A', 
           b'value': b'1.2.3.4', 
           b'meta': {}})
        self.assertEquals({}, provider._monitors_for(record))
        self.assertEquals({b'1.2.3.4': monitor_one, 
           b'2.3.4.5': monitor_four}, provider._monitors_for(self.record))

    def test_uuid(self):
        provider = Ns1Provider(b'test', b'api-key')
        self.assertTrue(provider._uuid())

    @patch(b'octodns.provider.ns1.Ns1Provider._uuid')
    @patch(b'ns1.rest.data.Feed.create')
    def test_feed_create(self, datafeed_create_mock, uuid_mock):
        provider = Ns1Provider(b'test', b'api-key')
        provider._client._datasource_id = b'foo'
        provider._client._feeds_for_monitors = {}
        uuid_mock.reset_mock()
        datafeed_create_mock.reset_mock()
        uuid_mock.side_effect = [b'xxxxxxxxxxxxxx']
        feed = {b'id': b'feed'}
        datafeed_create_mock.side_effect = [
         feed]
        monitor = {b'id': b'one', 
           b'name': b'one name', 
           b'config': {b'host': b'1.2.3.4'}, 
           b'notes': b'host:unit.tests type:A'}
        self.assertEquals(b'feed', provider._feed_create(monitor))
        datafeed_create_mock.assert_has_calls([call(b'foo', b'one name - xxxxxx', {b'jobid': b'one'})])

    @patch(b'octodns.provider.ns1.Ns1Provider._feed_create')
    @patch(b'octodns.provider.ns1.Ns1Client.monitors_create')
    @patch(b'octodns.provider.ns1.Ns1Client.notifylists_create')
    def test_monitor_create(self, notifylists_create_mock, monitors_create_mock, feed_create_mock):
        provider = Ns1Provider(b'test', b'api-key')
        provider._client._datasource_id = b'foo'
        provider._client._feeds_for_monitors = {}
        notifylists_create_mock.reset_mock()
        monitors_create_mock.reset_mock()
        feed_create_mock.reset_mock()
        notifylists_create_mock.side_effect = [
         {b'id': b'nl-id'}]
        monitors_create_mock.side_effect = [
         {b'id': b'mon-id'}]
        feed_create_mock.side_effect = [
         b'feed-id']
        monitor = {b'name': b'test monitor'}
        monitor_id, feed_id = provider._monitor_create(monitor)
        self.assertEquals(b'mon-id', monitor_id)
        self.assertEquals(b'feed-id', feed_id)
        monitors_create_mock.assert_has_calls([
         call(name=b'test monitor', notify_list=b'nl-id')])

    def test_monitor_gen(self):
        provider = Ns1Provider(b'test', b'api-key')
        value = b'3.4.5.6'
        monitor = provider._monitor_gen(self.record, value)
        self.assertEquals(value, monitor[b'config'][b'host'])
        self.assertTrue(b'\\nHost: send.me\\r' in monitor[b'config'][b'send'])
        self.assertFalse(monitor[b'config'][b'ssl'])
        self.assertEquals(b'host:unit.tests type:A', monitor[b'notes'])
        self.record._octodns[b'healthcheck'][b'protocol'] = b'HTTPS'
        monitor = provider._monitor_gen(self.record, value)
        self.assertTrue(monitor[b'config'][b'ssl'])

    def test_monitor_is_match(self):
        provider = Ns1Provider(b'test', b'api-key')
        self.assertTrue(provider._monitor_is_match({}, {}))
        self.assertTrue(provider._monitor_is_match({}, {b'anything': b'goes'}))
        self.assertFalse(provider._monitor_is_match({b'exepct': b'this'}, {b'anything': b'goes'}))
        self.assertTrue(provider._monitor_is_match({b'exepct': b'this'}, {b'exepct': b'this'}))
        self.assertFalse(provider._monitor_is_match({b'exepct': b'this'}, {b'exepct': b'that'}))
        self.assertFalse(provider._monitor_is_match({b'exepct': {b'this': b'to-be'}}, {b'exepct': {b'this': b'something-else'}}))

    @patch(b'octodns.provider.ns1.Ns1Provider._feed_create')
    @patch(b'octodns.provider.ns1.Ns1Client.monitors_update')
    @patch(b'octodns.provider.ns1.Ns1Provider._monitor_create')
    @patch(b'octodns.provider.ns1.Ns1Provider._monitor_gen')
    def test_monitor_sync(self, monitor_gen_mock, monitor_create_mock, monitors_update_mock, feed_create_mock):
        provider = Ns1Provider(b'test', b'api-key')
        provider._client._datasource_id = b'foo'
        provider._client._feeds_for_monitors = {b'mon-id': b'feed-id'}
        monitor_gen_mock.reset_mock()
        monitor_create_mock.reset_mock()
        monitors_update_mock.reset_mock()
        feed_create_mock.reset_mock()
        monitor_gen_mock.side_effect = [{b'key': b'value'}]
        monitor_create_mock.side_effect = [('mon-id', 'feed-id')]
        value = b'1.2.3.4'
        monitor_id, feed_id = provider._monitor_sync(self.record, value, None)
        self.assertEquals(b'mon-id', monitor_id)
        self.assertEquals(b'feed-id', feed_id)
        monitor_gen_mock.assert_has_calls([call(self.record, value)])
        monitor_create_mock.assert_has_calls([call({b'key': b'value'})])
        monitors_update_mock.assert_not_called()
        feed_create_mock.assert_not_called()
        monitor_gen_mock.reset_mock()
        monitor_create_mock.reset_mock()
        monitors_update_mock.reset_mock()
        feed_create_mock.reset_mock()
        monitor = {b'id': b'mon-id', 
           b'key': b'value', 
           b'name': b'monitor name'}
        monitor_gen_mock.side_effect = [
         monitor]
        monitor_id, feed_id = provider._monitor_sync(self.record, value, monitor)
        self.assertEquals(b'mon-id', monitor_id)
        self.assertEquals(b'feed-id', feed_id)
        monitor_gen_mock.assert_called_once()
        monitor_create_mock.assert_not_called()
        monitors_update_mock.assert_not_called()
        feed_create_mock.assert_not_called()
        monitor_gen_mock.reset_mock()
        monitor_create_mock.reset_mock()
        monitors_update_mock.reset_mock()
        feed_create_mock.reset_mock()
        monitor = {b'id': b'mon-id2', 
           b'key': b'value', 
           b'name': b'monitor name'}
        monitor_gen_mock.side_effect = [
         monitor]
        feed_create_mock.side_effect = [b'feed-id2']
        monitor_id, feed_id = provider._monitor_sync(self.record, value, monitor)
        self.assertEquals(b'mon-id2', monitor_id)
        self.assertEquals(b'feed-id2', feed_id)
        monitor_gen_mock.assert_called_once()
        monitor_create_mock.assert_not_called()
        monitors_update_mock.assert_not_called()
        feed_create_mock.assert_has_calls([call(monitor)])
        monitor_gen_mock.reset_mock()
        monitor_create_mock.reset_mock()
        monitors_update_mock.reset_mock()
        feed_create_mock.reset_mock()
        monitor = {b'id': b'mon-id', 
           b'key': b'value', 
           b'name': b'monitor name'}
        gened = {b'other': b'thing'}
        monitor_gen_mock.side_effect = [
         gened]
        monitor_id, feed_id = provider._monitor_sync(self.record, value, monitor)
        self.assertEquals(b'mon-id', monitor_id)
        self.assertEquals(b'feed-id', feed_id)
        monitor_gen_mock.assert_called_once()
        monitor_create_mock.assert_not_called()
        monitors_update_mock.assert_has_calls([call(b'mon-id', other=b'thing')])
        feed_create_mock.assert_not_called()
        return

    @patch(b'octodns.provider.ns1.Ns1Client.notifylists_delete')
    @patch(b'octodns.provider.ns1.Ns1Client.monitors_delete')
    @patch(b'octodns.provider.ns1.Ns1Client.datafeed_delete')
    @patch(b'octodns.provider.ns1.Ns1Provider._monitors_for')
    def test_monitors_gc(self, monitors_for_mock, datafeed_delete_mock, monitors_delete_mock, notifylists_delete_mock):
        provider = Ns1Provider(b'test', b'api-key')
        provider._client._datasource_id = b'foo'
        provider._client._feeds_for_monitors = {b'mon-id': b'feed-id'}
        monitors_for_mock.reset_mock()
        datafeed_delete_mock.reset_mock()
        monitors_delete_mock.reset_mock()
        notifylists_delete_mock.reset_mock()
        monitors_for_mock.side_effect = [{}]
        provider._monitors_gc(self.record)
        monitors_for_mock.assert_has_calls([call(self.record)])
        datafeed_delete_mock.assert_not_called()
        monitors_delete_mock.assert_not_called()
        notifylists_delete_mock.assert_not_called()
        monitors_for_mock.reset_mock()
        datafeed_delete_mock.reset_mock()
        monitors_delete_mock.reset_mock()
        notifylists_delete_mock.reset_mock()
        monitors_for_mock.side_effect = [
         {b'x': {b'id': b'mon-id', 
                   b'notify_list': b'nl-id'}}]
        provider._monitors_gc(self.record)
        monitors_for_mock.assert_has_calls([call(self.record)])
        datafeed_delete_mock.assert_has_calls([call(b'foo', b'feed-id')])
        monitors_delete_mock.assert_has_calls([call(b'mon-id')])
        notifylists_delete_mock.assert_has_calls([call(b'nl-id')])
        monitors_for_mock.reset_mock()
        datafeed_delete_mock.reset_mock()
        monitors_delete_mock.reset_mock()
        notifylists_delete_mock.reset_mock()
        monitors_for_mock.side_effect = [
         {b'x': {b'id': b'mon-id', 
                   b'notify_list': b'nl-id'}}]
        provider._monitors_gc(self.record, {b'mon-id'})
        monitors_for_mock.assert_has_calls([call(self.record)])
        datafeed_delete_mock.assert_not_called()
        monitors_delete_mock.assert_not_called()
        notifylists_delete_mock.assert_not_called()
        monitors_for_mock.reset_mock()
        datafeed_delete_mock.reset_mock()
        monitors_delete_mock.reset_mock()
        notifylists_delete_mock.reset_mock()
        monitors_for_mock.side_effect = [
         {b'x': {b'id': b'mon-id', 
                   b'notify_list': b'nl-id'}, 
            b'y': {b'id': b'mon-id2', 
                   b'notify_list': b'nl-id2'}}]
        provider._monitors_gc(self.record, {b'mon-id'})
        monitors_for_mock.assert_has_calls([call(self.record)])
        datafeed_delete_mock.assert_not_called()
        monitors_delete_mock.assert_has_calls([call(b'mon-id2')])
        notifylists_delete_mock.assert_has_calls([call(b'nl-id2')])

    @patch(b'octodns.provider.ns1.Ns1Provider._monitor_sync')
    @patch(b'octodns.provider.ns1.Ns1Provider._monitors_for')
    def test_params_for_dynamic_region_only(self, monitors_for_mock, monitor_sync_mock):
        provider = Ns1Provider(b'test', b'api-key')
        provider._client._datasource_id = b'foo'
        provider._client._feeds_for_monitors = {b'mon-id': b'feed-id'}
        monitors_for_mock.reset_mock()
        monitor_sync_mock.reset_mock()
        monitors_for_mock.side_effect = [
         {b'3.4.5.6': b'mid-3'}]
        monitor_sync_mock.side_effect = [
         ('mid-1', 'fid-1'),
         ('mid-2', 'fid-2'),
         ('mid-3', 'fid-3')]
        rule0 = self.record.data[b'dynamic'][b'rules'][0]
        rule1 = self.record.data[b'dynamic'][b'rules'][1]
        rule0_saved_geos = rule0[b'geos']
        rule1_saved_geos = rule1[b'geos']
        rule0[b'geos'] = [b'AF', b'EU']
        rule1[b'geos'] = [b'NA']
        ret, _ = provider._params_for_A(self.record)
        self.assertEquals(ret[b'filters'], Ns1Provider._FILTER_CHAIN_WITH_REGION(provider, True))
        rule0[b'geos'] = rule0_saved_geos
        rule1[b'geos'] = rule1_saved_geos

    @patch(b'octodns.provider.ns1.Ns1Provider._monitor_sync')
    @patch(b'octodns.provider.ns1.Ns1Provider._monitors_for')
    def test_params_for_dynamic_oceania(self, monitors_for_mock, monitor_sync_mock):
        provider = Ns1Provider(b'test', b'api-key')
        provider._client._datasource_id = b'foo'
        provider._client._feeds_for_monitors = {b'mon-id': b'feed-id'}
        monitors_for_mock.reset_mock()
        monitor_sync_mock.reset_mock()
        monitors_for_mock.side_effect = [
         {b'3.4.5.6': b'mid-3'}]
        monitor_sync_mock.side_effect = [
         ('mid-1', 'fid-1'),
         ('mid-2', 'fid-2'),
         ('mid-3', 'fid-3')]
        rule0 = self.record.data[b'dynamic'][b'rules'][0]
        saved_geos = rule0[b'geos']
        rule0[b'geos'] = [b'OC']
        ret, _ = provider._params_for_A(self.record)
        self.assertEquals(set(ret[b'regions'][b'lhr'][b'meta'][b'country']), Ns1Provider._CONTINENT_TO_LIST_OF_COUNTRIES[b'OC'])
        self.assertEquals(ret[b'filters'], Ns1Provider._FILTER_CHAIN_WITH_COUNTRY(provider, True))
        rule0[b'geos'] = saved_geos

    @patch(b'octodns.provider.ns1.Ns1Provider._monitor_sync')
    @patch(b'octodns.provider.ns1.Ns1Provider._monitors_for')
    def test_params_for_dynamic(self, monitors_for_mock, monitors_sync_mock):
        provider = Ns1Provider(b'test', b'api-key')
        provider._client._datasource_id = b'foo'
        provider._client._feeds_for_monitors = {b'mon-id': b'feed-id'}
        monitors_for_mock.reset_mock()
        monitors_sync_mock.reset_mock()
        monitors_for_mock.side_effect = [
         {b'3.4.5.6': b'mid-3'}]
        monitors_sync_mock.side_effect = [
         ('mid-1', 'fid-1'),
         ('mid-2', 'fid-2'),
         ('mid-3', 'fid-3')]
        ret, _ = provider._params_for_A(self.record)
        self.assertEquals(ret[b'filters'], Ns1Provider._FILTER_CHAIN_WITH_REGION_AND_COUNTRY(provider, True))
        monitors_for_mock.assert_has_calls([call(self.record)])
        monitors_sync_mock.assert_has_calls([
         call(self.record, b'1.2.3.4', None),
         call(self.record, b'2.3.4.5', None),
         call(self.record, b'3.4.5.6', b'mid-3')])
        return

    def test_data_for_dynamic_A(self):
        provider = Ns1Provider(b'test', b'api-key')
        ns1_record = {b'domain': b'unit.tests', 
           b'filters': []}
        with self.assertRaises(Ns1Exception) as (ctx):
            provider._data_for_dynamic_A(b'A', ns1_record)
        self.assertEquals(b'Unrecognized advanced record', text_type(ctx.exception))
        ns1_record = {b'answers': [], b'domain': b'unit.tests', 
           b'filters': Ns1Provider._BASIC_FILTER_CHAIN(provider, True), 
           b'regions': {}, b'ttl': 42}
        data = provider._data_for_dynamic_A(b'A', ns1_record)
        self.assertEquals({b'dynamic': {b'pools': {}, b'rules': []}, b'ttl': 42, 
           b'type': b'A', 
           b'values': []}, data)
        filters = provider._get_updated_filter_chain(True, True)
        catchall_pool_name = (b'{}{}').format(provider.CATCHALL_PREFIX, b'iad')
        ns1_record = {b'answers': [
                      {b'answer': [
                                   b'3.4.5.6'], 
                         b'meta': {b'priority': 1, 
                                   b'note': b'from:lhr'}, 
                         b'region': b'lhr'},
                      {b'answer': [
                                   b'2.3.4.5'], 
                         b'meta': {b'priority': 2, 
                                   b'weight': 12, 
                                   b'note': b'from:iad'}, 
                         b'region': b'lhr'},
                      {b'answer': [
                                   b'1.2.3.4'], 
                         b'meta': {b'priority': 3, 
                                   b'note': b'from:--default--'}, 
                         b'region': b'lhr'},
                      {b'answer': [
                                   b'2.3.4.5'], 
                         b'meta': {b'priority': 1, 
                                   b'weight': 12, 
                                   b'note': b'from:iad'}, 
                         b'region': b'iad'},
                      {b'answer': [
                                   b'1.2.3.4'], 
                         b'meta': {b'priority': 2, 
                                   b'note': b'from:--default--'}, 
                         b'region': b'iad'},
                      {b'answer': [
                                   b'2.3.4.5'], 
                         b'meta': {b'priority': 1, 
                                   b'weight': 12, 
                                   b'note': (b'from:{}').format(catchall_pool_name)}, 
                         b'region': catchall_pool_name},
                      {b'answer': [
                                   b'1.2.3.4'], 
                         b'meta': {b'priority': 2, 
                                   b'note': b'from:--default--'}, 
                         b'region': catchall_pool_name}], 
           b'domain': b'unit.tests', 
           b'filters': filters, 
           b'regions': {b'lhr': {b'meta': {b'note': b'rule-order:1 fallback:iad', 
                                           b'country': [
                                                      b'CA'], 
                                           b'georegion': [
                                                        b'AFRICA'], 
                                           b'us_state': [
                                                       b'OR']}}, 
                        b'iad': {b'meta': {b'note': b'rule-order:2', 
                                           b'country': [
                                                      b'ZW']}}, 
                        catchall_pool_name: {b'meta': {b'note': b'rule-order:3'}}}, 
           b'tier': 3, 
           b'ttl': 42}
        data = provider._data_for_dynamic_A(b'A', ns1_record)
        self.assertEquals({b'dynamic': {b'pools': {b'iad': {b'fallback': None, 
                                            b'values': [
                                                      {b'value': b'2.3.4.5', 
                                                         b'weight': 12}]}, 
                                   b'lhr': {b'fallback': b'iad', 
                                            b'values': [
                                                      {b'weight': 1, 
                                                         b'value': b'3.4.5.6'}]}}, 
                        b'rules': [
                                 {b'_order': b'1', 
                                    b'geos': [
                                            b'AF',
                                            b'NA-CA',
                                            b'NA-US-OR'], 
                                    b'pool': b'lhr'},
                                 {b'_order': b'2', 
                                    b'geos': [
                                            b'AF-ZW'], 
                                    b'pool': b'iad'},
                                 {b'_order': b'3', 
                                    b'pool': b'iad'}]}, 
           b'ttl': 42, 
           b'type': b'A', 
           b'values': [
                     b'1.2.3.4']}, data)
        data2 = provider._data_for_A(b'A', ns1_record)
        self.assertEquals(data, data2)
        oc_countries = Ns1Provider._CONTINENT_TO_LIST_OF_COUNTRIES[b'OC']
        ns1_record[b'regions'][b'lhr'][b'meta'][b'country'] = list(oc_countries)
        data3 = provider._data_for_A(b'A', ns1_record)
        self.assertTrue(b'OC' in data3[b'dynamic'][b'rules'][0][b'geos'])
        partial_oc_cntry_list = list(oc_countries)[:5]
        ns1_record[b'regions'][b'lhr'][b'meta'][b'country'] = partial_oc_cntry_list
        data4 = provider._data_for_A(b'A', ns1_record)
        for c in partial_oc_cntry_list:
            self.assertTrue((b'OC-{}').format(c) in data4[b'dynamic'][b'rules'][0][b'geos'])

        return

    @patch(b'ns1.rest.records.Records.retrieve')
    @patch(b'ns1.rest.zones.Zones.retrieve')
    @patch(b'octodns.provider.ns1.Ns1Provider._monitors_for')
    def test_extra_changes(self, monitors_for_mock, zones_retrieve_mock, records_retrieve_mock):
        provider = Ns1Provider(b'test', b'api-key')
        desired = Zone(b'unit.tests.', [])
        monitors_for_mock.reset_mock()
        zones_retrieve_mock.reset_mock()
        records_retrieve_mock.reset_mock()
        extra = provider._extra_changes(desired, [])
        self.assertFalse(extra)
        monitors_for_mock.assert_not_called()
        monitors_for_mock.reset_mock()
        zones_retrieve_mock.side_effect = ResourceException(b'server error: zone not found')
        records_retrieve_mock.reset_mock()
        extra = provider._extra_changes(desired, [])
        self.assertFalse(extra)
        zones_retrieve_mock.reset_mock()
        zones_retrieve_mock.side_effect = ResourceException(b'boom')
        with self.assertRaises(ResourceException) as (ctx):
            extra = provider._extra_changes(desired, [])
        self.assertEquals(zones_retrieve_mock.side_effect, ctx.exception)
        monitors_for_mock.reset_mock()
        zones_retrieve_mock.reset_mock()
        records_retrieve_mock.reset_mock()
        zones_retrieve_mock.side_effect = ResourceException(b'server error: zone not found')
        simple = Record.new(desired, b'', {b'ttl': 32, 
           b'type': b'A', 
           b'value': b'1.2.3.4', 
           b'meta': {}})
        desired.add_record(simple)
        extra = provider._extra_changes(desired, [])
        self.assertFalse(extra)
        monitors_for_mock.assert_not_called()
        dynamic = Record.new(desired, b'dyn', {b'dynamic': {b'pools': {b'iad': {b'values': [
                                                      {b'value': b'1.2.3.4'}]}}, 
                        b'rules': [
                                 {b'pool': b'iad'}]}, 
           b'octodns': {b'healthcheck': {b'host': b'send.me', 
                                         b'path': b'/_ping', 
                                         b'port': 80, 
                                         b'protocol': b'HTTP'}}, 
           b'ttl': 32, 
           b'type': b'A', 
           b'value': b'1.2.3.4', 
           b'meta': {}})
        desired.add_record(dynamic)
        monitors_for_mock.reset_mock()
        zones_retrieve_mock.reset_mock()
        records_retrieve_mock.reset_mock()
        gend = provider._monitor_gen(dynamic, b'1.2.3.4')
        gend.update({b'id': b'mid', 
           b'notify_list': b'xyz'})
        monitors_for_mock.side_effect = [
         {b'1.2.3.4': gend}]
        extra = provider._extra_changes(desired, [])
        self.assertFalse(extra)
        monitors_for_mock.assert_has_calls([call(dynamic)])
        update = Update(dynamic, dynamic)
        monitors_for_mock.reset_mock()
        zones_retrieve_mock.reset_mock()
        records_retrieve_mock.reset_mock()
        del gend[b'notify_list']
        monitors_for_mock.side_effect = [
         {b'1.2.3.4': gend}]
        extra = provider._extra_changes(desired, [])
        self.assertEquals(1, len(extra))
        extra = list(extra)[0]
        self.assertIsInstance(extra, Update)
        self.assertEquals(dynamic, extra.new)
        monitors_for_mock.assert_has_calls([call(dynamic)])
        monitors_for_mock.reset_mock()
        zones_retrieve_mock.reset_mock()
        records_retrieve_mock.reset_mock()
        gend[b'notify_list'] = b'xyz'
        dynamic._octodns[b'healthcheck'][b'protocol'] = b'HTTPS'
        del gend[b'notify_list']
        monitors_for_mock.side_effect = [
         {b'1.2.3.4': gend}]
        extra = provider._extra_changes(desired, [])
        self.assertEquals(1, len(extra))
        extra = list(extra)[0]
        self.assertIsInstance(extra, Update)
        self.assertEquals(dynamic, extra.new)
        monitors_for_mock.assert_has_calls([call(dynamic)])
        monitors_for_mock.reset_mock()
        zones_retrieve_mock.reset_mock()
        records_retrieve_mock.reset_mock()
        extra = provider._extra_changes(desired, [update])
        self.assertFalse(extra)
        monitors_for_mock.assert_not_called()
        monitors_for_mock.reset_mock()
        zones_retrieve_mock.reset_mock()
        records_retrieve_mock.reset_mock()
        ns1_zone = {b'records': [
                      {b'domain': b'dyn.unit.tests', 
                         b'zone': b'unit.tests', 
                         b'type': b'A', 
                         b'tier': 3, 
                         b'filters': Ns1Provider._BASIC_FILTER_CHAIN(provider, True)}]}
        monitors_for_mock.side_effect = [{}]
        zones_retrieve_mock.side_effect = [
         ns1_zone]
        records_retrieve_mock.side_effect = ns1_zone[b'records']
        extra = provider._extra_changes(desired, [])
        self.assertFalse(extra)
        monitors_for_mock.reset_mock()
        zones_retrieve_mock.reset_mock()
        records_retrieve_mock.reset_mock()
        ns1_zone = {b'records': [
                      {b'domain': b'dyn.unit.tests', 
                         b'zone': b'unit.tests', 
                         b'type': b'A', 
                         b'tier': 3, 
                         b'filters': Ns1Provider._BASIC_FILTER_CHAIN(provider, False)}]}
        monitors_for_mock.side_effect = [{}]
        zones_retrieve_mock.side_effect = [
         ns1_zone]
        records_retrieve_mock.side_effect = ns1_zone[b'records']
        extra = provider._extra_changes(desired, [])
        self.assertTrue(extra)
        monitors_for_mock.reset_mock()
        zones_retrieve_mock.reset_mock()
        records_retrieve_mock.reset_mock()
        ns1_zone = {b'records': [
                      {b'domain': b'dyn.unit.tests', 
                         b'zone': b'unit.tests', 
                         b'type': b'A', 
                         b'tier': 3, 
                         b'filters': Ns1Provider._BASIC_FILTER_CHAIN(provider, True)}]}
        del ns1_zone[b'records'][0][b'filters'][0][b'disabled']
        monitors_for_mock.side_effect = [{}]
        zones_retrieve_mock.side_effect = [ns1_zone]
        records_retrieve_mock.side_effect = ns1_zone[b'records']
        with self.assertRaises(Ns1Exception) as (ctx):
            extra = provider._extra_changes(desired, [])
        self.assertTrue(b'Mixed disabled flag in filters' in text_type(ctx.exception))

    DESIRED = Zone(b'unit.tests.', [])
    SIMPLE = Record.new(DESIRED, b'sim', {b'ttl': 33, 
       b'type': b'A', 
       b'value': b'1.2.3.4'})
    DYNAMIC = Record.new(DESIRED, b'dyn', {b'dynamic': {b'pools': {b'iad': {b'values': [
                                                  {b'value': b'1.2.3.4'}]}}, 
                    b'rules': [
                             {b'pool': b'iad'}]}, 
       b'octodns': {b'healthcheck': {b'host': b'send.me', 
                                     b'path': b'/_ping', 
                                     b'port': 80, 
                                     b'protocol': b'HTTP'}}, 
       b'ttl': 32, 
       b'type': b'A', 
       b'value': b'1.2.3.4', 
       b'meta': {}})

    def test_has_dynamic(self):
        provider = Ns1Provider(b'test', b'api-key')
        simple_update = Update(self.SIMPLE, self.SIMPLE)
        dynamic_update = Update(self.DYNAMIC, self.DYNAMIC)
        self.assertFalse(provider._has_dynamic([simple_update]))
        self.assertTrue(provider._has_dynamic([dynamic_update]))
        self.assertTrue(provider._has_dynamic([simple_update, dynamic_update]))

    @patch(b'octodns.provider.ns1.Ns1Client.zones_retrieve')
    @patch(b'octodns.provider.ns1.Ns1Provider._apply_Update')
    def test_apply_monitor_regions(self, apply_update_mock, zones_retrieve_mock):
        provider = Ns1Provider(b'test', b'api-key')
        simple_update = Update(self.SIMPLE, self.SIMPLE)
        simple_plan = Plan(self.DESIRED, self.DESIRED, [simple_update], True)
        dynamic_update = Update(self.DYNAMIC, self.DYNAMIC)
        dynamic_update = Update(self.DYNAMIC, self.DYNAMIC)
        dynamic_plan = Plan(self.DESIRED, self.DESIRED, [dynamic_update], True)
        both_plan = Plan(self.DESIRED, self.DESIRED, [simple_update,
         dynamic_update], True)
        zones_retrieve_mock.side_effect = [
         b'foo',
         b'foo',
         b'foo',
         b'foo']
        apply_update_mock.reset_mock()
        provider._apply(simple_plan)
        apply_update_mock.assert_has_calls([call(b'foo', simple_update)])
        apply_update_mock.reset_mock()
        with self.assertRaises(Ns1Exception) as (ctx):
            provider._apply(dynamic_plan)
        self.assertTrue(b'monitor_regions not set' in text_type(ctx.exception))
        apply_update_mock.assert_not_called()
        apply_update_mock.reset_mock()
        with self.assertRaises(Ns1Exception) as (ctx):
            provider._apply(both_plan)
        self.assertTrue(b'monitor_regions not set' in text_type(ctx.exception))
        apply_update_mock.assert_not_called()
        provider.monitor_regions = [
         b'lga']
        apply_update_mock.reset_mock()
        provider._apply(both_plan)
        apply_update_mock.assert_has_calls([
         call(b'foo', dynamic_update),
         call(b'foo', simple_update)])


class TestNs1Client(TestCase):

    @patch(b'ns1.rest.zones.Zones.retrieve')
    def test_retry_behavior(self, zone_retrieve_mock):
        client = Ns1Client(b'dummy-key')
        zone_retrieve_mock.reset_mock()
        zone_retrieve_mock.side_effect = [b'foo']
        self.assertEquals(b'foo', client.zones_retrieve(b'unit.tests'))
        zone_retrieve_mock.assert_has_calls([call(b'unit.tests')])
        zone_retrieve_mock.reset_mock()
        zone_retrieve_mock.side_effect = [
         RateLimitException(b'boo', period=0),
         b'foo']
        self.assertEquals(b'foo', client.zones_retrieve(b'unit.tests'))
        zone_retrieve_mock.assert_has_calls([call(b'unit.tests')])
        zone_retrieve_mock.reset_mock()
        zone_retrieve_mock.side_effect = [
         RateLimitException(b'boo', period=0),
         b'foo']
        self.assertEquals(b'foo', client.zones_retrieve(b'unit.tests'))
        zone_retrieve_mock.assert_has_calls([call(b'unit.tests')])
        zone_retrieve_mock.reset_mock()
        zone_retrieve_mock.side_effect = [
         RateLimitException(b'first', period=0),
         RateLimitException(b'boo', period=0),
         RateLimitException(b'boo', period=0),
         RateLimitException(b'last', period=0)]
        with self.assertRaises(RateLimitException) as (ctx):
            client.zones_retrieve(b'unit.tests')
        self.assertEquals(b'last', text_type(ctx.exception))

    def test_client_config(self):
        with self.assertRaises(TypeError):
            Ns1Client()
        client = Ns1Client(b'dummy-key')
        self.assertEquals(client._client.config.get(b'keys'), {b'default': {b'key': b'dummy-key', b'desc': b'imported API key'}})
        self.assertEquals(client._client.config.get(b'follow_pagination'), True)
        self.assertEquals(client._client.config.get(b'rate_limit_strategy'), None)
        self.assertEquals(client._client.config.get(b'parallelism'), None)
        client = Ns1Client(b'dummy-key', parallelism=11)
        self.assertEquals(client._client.config.get(b'rate_limit_strategy'), b'concurrent')
        self.assertEquals(client._client.config.get(b'parallelism'), 11)
        client = Ns1Client(b'dummy-key', client_config={b'endpoint': b'my.endpoint.com', 
           b'follow_pagination': False})
        self.assertEquals(client._client.config.get(b'endpoint'), b'my.endpoint.com')
        self.assertEquals(client._client.config.get(b'follow_pagination'), False)
        return

    @patch(b'ns1.rest.data.Source.list')
    @patch(b'ns1.rest.data.Source.create')
    def test_datasource_id(self, datasource_create_mock, datasource_list_mock):
        client = Ns1Client(b'dummy-key')
        datasource_list_mock.reset_mock()
        datasource_create_mock.reset_mock()
        datasource_list_mock.side_effect = [[]]
        datasource_create_mock.side_effect = [
         {b'id': b'foo'}]
        self.assertEquals(b'foo', client.datasource_id)
        name = b'octoDNS NS1 Data Source'
        source_type = b'nsone_monitoring'
        datasource_create_mock.assert_has_calls([
         call(name=name, sourcetype=source_type)])
        datasource_list_mock.assert_called_once()
        datasource_list_mock.reset_mock()
        datasource_create_mock.reset_mock()
        self.assertEquals(b'foo', client.datasource_id)
        datasource_create_mock.assert_not_called()
        datasource_list_mock.assert_not_called()
        client._datasource_id = None
        datasource_list_mock.reset_mock()
        datasource_create_mock.reset_mock()
        datasource_list_mock.side_effect = [
         [
          {b'id': b'other', 
             b'name': b'not a match'},
          {b'id': b'bar', 
             b'name': name}]]
        self.assertEquals(b'bar', client.datasource_id)
        datasource_create_mock.assert_not_called()
        datasource_list_mock.assert_called_once()
        return

    @patch(b'ns1.rest.data.Feed.delete')
    @patch(b'ns1.rest.data.Feed.create')
    @patch(b'ns1.rest.data.Feed.list')
    def test_feeds_for_monitors(self, datafeed_list_mock, datafeed_create_mock, datafeed_delete_mock):
        client = Ns1Client(b'dummy-key')
        client._datasource_id = b'foo'
        datafeed_list_mock.reset_mock()
        datafeed_list_mock.side_effect = [
         [
          {b'config': {b'jobid': b'the-job'}, 
             b'id': b'the-feed'},
          {b'config': {b'jobid': b'the-other-job'}, 
             b'id': b'the-other-feed'}]]
        expected = {b'the-job': b'the-feed', 
           b'the-other-job': b'the-other-feed'}
        self.assertEquals(expected, client.feeds_for_monitors)
        datafeed_list_mock.assert_called_once()
        datafeed_list_mock.reset_mock()
        self.assertEquals(expected, client.feeds_for_monitors)
        datafeed_list_mock.assert_not_called()
        datafeed_create_mock.reset_mock()
        datafeed_create_mock.side_effect = [
         {b'id': b'new-feed'}]
        client.datafeed_create(client.datasource_id, b'new-name', {b'jobid': b'new-job'})
        datafeed_create_mock.assert_has_calls([
         call(b'foo', b'new-name', {b'jobid': b'new-job'})])
        new_expected = expected.copy()
        new_expected[b'new-job'] = b'new-feed'
        self.assertEquals(new_expected, client.feeds_for_monitors)
        datafeed_create_mock.assert_called_once()
        datafeed_delete_mock.reset_mock()
        client.datafeed_delete(client.datasource_id, b'new-feed')
        self.assertEquals(expected, client.feeds_for_monitors)
        datafeed_delete_mock.assert_called_once()

    @patch(b'ns1.rest.monitoring.Monitors.delete')
    @patch(b'ns1.rest.monitoring.Monitors.update')
    @patch(b'ns1.rest.monitoring.Monitors.create')
    @patch(b'ns1.rest.monitoring.Monitors.list')
    def test_monitors(self, monitors_list_mock, monitors_create_mock, monitors_update_mock, monitors_delete_mock):
        client = Ns1Client(b'dummy-key')
        one = {b'id': b'one', 
           b'key': b'value'}
        two = {b'id': b'two', 
           b'key': b'other-value'}
        monitors_list_mock.reset_mock()
        monitors_list_mock.side_effect = [[one, two]]
        expected = {b'one': one, 
           b'two': two}
        self.assertEquals(expected, client.monitors)
        monitors_list_mock.assert_called_once()
        monitors_list_mock.reset_mock()
        self.assertEquals(expected, client.monitors)
        monitors_list_mock.assert_not_called()
        monitors_create_mock.reset_mock()
        monitor = {b'id': b'new-id', 
           b'key': b'new-value'}
        monitors_create_mock.side_effect = [
         monitor]
        self.assertEquals(monitor, client.monitors_create(param=b'eter'))
        monitors_create_mock.assert_has_calls([call({}, param=b'eter')])
        new_expected = expected.copy()
        new_expected[b'new-id'] = monitor
        self.assertEquals(new_expected, client.monitors)
        monitors_update_mock.reset_mock()
        monitor = {b'id': b'new-id', 
           b'key': b'changed-value'}
        monitors_update_mock.side_effect = [
         monitor]
        self.assertEquals(monitor, client.monitors_update(b'new-id', key=b'changed-value'))
        monitors_update_mock.assert_has_calls([
         call(b'new-id', {}, key=b'changed-value')])
        new_expected[b'new-id'] = monitor
        self.assertEquals(new_expected, client.monitors)
        monitors_delete_mock.reset_mock()
        monitors_delete_mock.side_effect = [b'deleted']
        self.assertEquals(b'deleted', client.monitors_delete(b'new-id'))
        monitors_delete_mock.assert_has_calls([call(b'new-id')])
        self.assertEquals(expected, client.monitors)

    @patch(b'ns1.rest.monitoring.NotifyLists.delete')
    @patch(b'ns1.rest.monitoring.NotifyLists.create')
    @patch(b'ns1.rest.monitoring.NotifyLists.list')
    def test_notifylists(self, notifylists_list_mock, notifylists_create_mock, notifylists_delete_mock):
        client = Ns1Client(b'dummy-key')
        notifylists_list_mock.reset_mock()
        notifylists_create_mock.reset_mock()
        notifylists_delete_mock.reset_mock()
        notifylists_create_mock.side_effect = [b'bar']
        notify_list = [
         {b'config': {b'sourceid': b'foo'}, 
            b'type': b'datafeed'}]
        nl = client.notifylists_create(name=b'some name', notify_list=notify_list)
        self.assertEquals(b'bar', nl)
        notifylists_list_mock.assert_not_called()
        notifylists_create_mock.assert_has_calls([
         call({b'name': b'some name', b'notify_list': notify_list})])
        notifylists_delete_mock.assert_not_called()
        notifylists_list_mock.reset_mock()
        notifylists_create_mock.reset_mock()
        notifylists_delete_mock.reset_mock()
        client.notifylists_delete(b'nlid')
        notifylists_list_mock.assert_not_called()
        notifylists_create_mock.assert_not_called()
        notifylists_delete_mock.assert_has_calls([call(b'nlid')])
        notifylists_list_mock.reset_mock()
        notifylists_create_mock.reset_mock()
        notifylists_delete_mock.reset_mock()
        expected = [b'one', b'two', b'three']
        notifylists_list_mock.side_effect = [expected]
        nls = client.notifylists_list()
        self.assertEquals(expected, nls)
        notifylists_list_mock.assert_has_calls([call()])
        notifylists_create_mock.assert_not_called()
        notifylists_delete_mock.assert_not_called()