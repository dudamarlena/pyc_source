# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_cloudflare.py
# Compiled at: 2020-02-18 18:19:36
from __future__ import absolute_import, division, print_function, unicode_literals
from mock import Mock, call
from os.path import dirname, join
from requests import HTTPError
from requests_mock import ANY, mock as requests_mock
from six import text_type
from unittest import TestCase
from octodns.record import Record, Update
from octodns.provider.base import Plan
from octodns.provider.cloudflare import CloudflareProvider
from octodns.provider.yaml import YamlProvider
from octodns.zone import Zone

def set_record_proxied_flag(record, proxied):
    try:
        record._octodns[b'cloudflare'][b'proxied'] = proxied
    except KeyError:
        record._octodns[b'cloudflare'] = {b'proxied': proxied}

    return record


class TestCloudflareProvider(TestCase):
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

    empty = {b'result': [], b'result_info': {b'count': 0, b'per_page': 0}}

    def test_populate(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        with requests_mock() as (mock):
            mock.get(ANY, status_code=400, text=b'{"success":false,"errors":[{"code":1101,"message":"request was invalid"}],"messages":[],"result":null}')
            with self.assertRaises(Exception) as (ctx):
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
            self.assertEquals(b'CloudflareError', type(ctx.exception).__name__)
            self.assertEquals(b'request was invalid', text_type(ctx.exception))
        with requests_mock() as (mock):
            mock.get(ANY, status_code=403, text=b'{"success":false,"errors":[{"code":9103,"message":"Unknown X-Auth-Key or X-Auth-Email"}],"messages":[],"result":null}')
            with self.assertRaises(Exception) as (ctx):
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
            self.assertEquals(b'CloudflareAuthenticationError', type(ctx.exception).__name__)
            self.assertEquals(b'Unknown X-Auth-Key or X-Auth-Email', text_type(ctx.exception))
        with requests_mock() as (mock):
            mock.get(ANY, status_code=403, text=b'{}')
            with self.assertRaises(Exception) as (ctx):
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
            self.assertEquals(b'CloudflareAuthenticationError', type(ctx.exception).__name__)
            self.assertEquals(b'Cloudflare error', text_type(ctx.exception))
        with requests_mock() as (mock):
            mock.get(ANY, status_code=502, text=b'Things caught fire')
            with self.assertRaises(HTTPError) as (ctx):
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
            self.assertEquals(502, ctx.exception.response.status_code)
        with requests_mock() as (mock):
            mock.get(ANY, status_code=200, json=self.empty)
            zone = Zone(b'unit.tests.', [])
            provider.populate(zone)
            self.assertEquals(set(), zone.records)
        again = Zone(b'unit.tests.', [])
        provider.populate(again)
        self.assertEquals(set(), again.records)
        provider._zones = None
        with requests_mock() as (mock):
            base = b'https://api.cloudflare.com/client/v4/zones'
            with open(b'tests/fixtures/cloudflare-zones-page-1.json') as (fh):
                mock.get((b'{}?page=1').format(base), status_code=200, text=fh.read())
            with open(b'tests/fixtures/cloudflare-zones-page-2.json') as (fh):
                mock.get((b'{}?page=2').format(base), status_code=200, text=fh.read())
            mock.get((b'{}?page=3').format(base), status_code=200, json={b'result': [], b'result_info': {b'count': 0, b'per_page': 0}})
            base = (b'{}/234234243423aaabb334342aaa343435/dns_records').format(base)
            with open(b'tests/fixtures/cloudflare-dns_records-page-1.json') as (fh):
                mock.get((b'{}?page=1').format(base), status_code=200, text=fh.read())
            with open(b'tests/fixtures/cloudflare-dns_records-page-2.json') as (fh):
                mock.get((b'{}?page=2').format(base), status_code=200, text=fh.read())
            zone = Zone(b'unit.tests.', [])
            provider.populate(zone)
            self.assertEquals(12, len(zone.records))
            changes = self.expected.changes(zone, provider)
            self.assertEquals(0, len(changes))
        again = Zone(b'unit.tests.', [])
        provider.populate(again)
        self.assertEquals(12, len(again.records))
        return

    def test_apply(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        provider._request = Mock()
        provider._request.side_effect = [
         self.empty,
         {b'result': {b'id': 42}}] + [
         None] * 20
        plan = provider.plan(self.expected)
        self.assertEquals(12, len(plan.changes))
        self.assertEquals(12, provider.apply(plan))
        self.assertFalse(plan.exists)
        provider._request.assert_has_calls([
         call(b'POST', b'/zones', data={b'jump_start': False, 
            b'name': b'unit.tests'}),
         call(b'POST', b'/zones/42/dns_records', data={b'content': b'ns1.unit.tests.', 
            b'type': b'NS', 
            b'name': b'under.unit.tests', 
            b'ttl': 3600}),
         call(b'POST', b'/zones/42/dns_records', data={b'content': b'v=DKIM1;k=rsa;s=email;h=sha256;p=A/kinda+of/long/string+with+numb3rs', 
            b'type': b'TXT', 
            b'name': b'txt.unit.tests', 
            b'ttl': 600})], True)
        self.assertEquals(22, provider._request.call_count)
        provider._request.reset_mock()
        provider.zone_records = Mock(return_value=[
         {b'id': b'fc12ab34cd5611334422ab3322997653', 
            b'type': b'A', 
            b'name': b'www.unit.tests', 
            b'content': b'1.2.3.4', 
            b'proxiable': True, 
            b'proxied': False, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}},
         {b'id': b'fc12ab34cd5611334422ab3322997654', 
            b'type': b'A', 
            b'name': b'www.unit.tests', 
            b'content': b'2.2.3.4', 
            b'proxiable': True, 
            b'proxied': False, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:44.030044Z', 
            b'created_on': b'2017-03-11T18:01:44.030044Z', 
            b'meta': {b'auto_added': False}},
         {b'id': b'fc12ab34cd5611334422ab3322997655', 
            b'type': b'A', 
            b'name': b'nc.unit.tests', 
            b'content': b'3.2.3.4', 
            b'proxiable': True, 
            b'proxied': False, 
            b'ttl': 120, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:44.030044Z', 
            b'created_on': b'2017-03-11T18:01:44.030044Z', 
            b'meta': {b'auto_added': False}},
         {b'id': b'fc12ab34cd5611334422ab3322997655', 
            b'type': b'A', 
            b'name': b'ttl.unit.tests', 
            b'content': b'4.2.3.4', 
            b'proxiable': True, 
            b'proxied': False, 
            b'ttl': 600, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:44.030044Z', 
            b'created_on': b'2017-03-11T18:01:44.030044Z', 
            b'meta': {b'auto_added': False}}])
        provider._request.return_value = {}
        provider._request.side_effect = None
        wanted = Zone(b'unit.tests.', [])
        wanted.add_record(Record.new(wanted, b'nc', {b'ttl': 60, 
           b'type': b'A', 
           b'value': b'3.2.3.4'}))
        wanted.add_record(Record.new(wanted, b'ttl', {b'ttl': 300, 
           b'type': b'A', 
           b'value': b'3.2.3.4'}))
        plan = provider.plan(wanted)
        self.assertEquals(2, len(plan.changes))
        self.assertEquals(2, provider.apply(plan))
        self.assertTrue(plan.exists)
        provider._request.assert_has_calls([
         call(b'PUT', b'/zones/42/dns_records/fc12ab34cd5611334422ab3322997655', data={b'content': b'3.2.3.4', 
            b'type': b'A', 
            b'name': b'ttl.unit.tests', 
            b'proxied': False, 
            b'ttl': 300}),
         call(b'DELETE', b'/zones/ff12ab34cd5611334422ab3322997650/dns_records/fc12ab34cd5611334422ab3322997653'),
         call(b'DELETE', b'/zones/ff12ab34cd5611334422ab3322997650/dns_records/fc12ab34cd5611334422ab3322997654')])
        return

    def test_update_add_swap(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        provider.zone_records = Mock(return_value=[
         {b'id': b'fc12ab34cd5611334422ab3322997653', 
            b'type': b'A', 
            b'name': b'a.unit.tests', 
            b'content': b'1.1.1.1', 
            b'proxiable': True, 
            b'proxied': False, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}},
         {b'id': b'fc12ab34cd5611334422ab3322997654', 
            b'type': b'A', 
            b'name': b'a.unit.tests', 
            b'content': b'2.2.2.2', 
            b'proxiable': True, 
            b'proxied': False, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}}])
        provider._request = Mock()
        provider._request.side_effect = [
         self.empty,
         {b'result': {b'id': 42}},
         None,
         None,
         None,
         None]
        zone = Zone(b'unit.tests.', [])
        existing = Record.new(zone, b'a', {b'ttl': 300, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1', b'2.2.2.2']})
        new = Record.new(zone, b'a', {b'ttl': 300, 
           b'type': b'A', 
           b'values': [
                     b'2.2.2.2', b'3.3.3.3', b'4.4.4.4']})
        change = Update(existing, new)
        plan = Plan(zone, zone, [change], True)
        provider._apply(plan)
        provider._request.assert_has_calls([
         call(b'GET', b'/zones', params={b'page': 1}),
         call(b'POST', b'/zones', data={b'jump_start': False, 
            b'name': b'unit.tests'}),
         call(b'POST', b'/zones/42/dns_records', data={b'content': b'4.4.4.4', 
            b'type': b'A', 
            b'name': b'a.unit.tests', 
            b'proxied': False, 
            b'ttl': 300}),
         call(b'PUT', b'/zones/42/dns_records/fc12ab34cd5611334422ab3322997654', data={b'content': b'2.2.2.2', 
            b'type': b'A', 
            b'name': b'a.unit.tests', 
            b'proxied': False, 
            b'ttl': 300}),
         call(b'PUT', b'/zones/42/dns_records/fc12ab34cd5611334422ab3322997653', data={b'content': b'3.3.3.3', 
            b'type': b'A', 
            b'name': b'a.unit.tests', 
            b'proxied': False, 
            b'ttl': 300})])
        return

    def test_update_delete(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        provider.zone_records = Mock(return_value=[
         {b'id': b'fc12ab34cd5611334422ab3322997653', 
            b'type': b'NS', 
            b'name': b'unit.tests', 
            b'content': b'ns1.foo.bar', 
            b'proxiable': True, 
            b'proxied': False, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}},
         {b'id': b'fc12ab34cd5611334422ab3322997654', 
            b'type': b'NS', 
            b'name': b'unit.tests', 
            b'content': b'ns2.foo.bar', 
            b'proxiable': True, 
            b'proxied': False, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}}])
        provider._request = Mock()
        provider._request.side_effect = [
         self.empty,
         {b'result': {b'id': 42}},
         None,
         None]
        zone = Zone(b'unit.tests.', [])
        existing = Record.new(zone, b'', {b'ttl': 300, 
           b'type': b'NS', 
           b'values': [
                     b'ns1.foo.bar.', b'ns2.foo.bar.']})
        new = Record.new(zone, b'', {b'ttl': 300, 
           b'type': b'NS', 
           b'value': b'ns2.foo.bar.'})
        change = Update(existing, new)
        plan = Plan(zone, zone, [change], True)
        provider._apply(plan)
        provider._request.assert_has_calls([
         call(b'GET', b'/zones', params={b'page': 1}),
         call(b'POST', b'/zones', data={b'jump_start': False, 
            b'name': b'unit.tests'}),
         call(b'PUT', b'/zones/42/dns_records/fc12ab34cd5611334422ab3322997654', data={b'content': b'ns2.foo.bar.', 
            b'type': b'NS', 
            b'name': b'unit.tests', 
            b'ttl': 300}),
         call(b'DELETE', b'/zones/42/dns_records/fc12ab34cd5611334422ab3322997653')])
        return

    def test_srv(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        zone = Zone(b'unit.tests.', [])
        srv_record = Record.new(zone, b'_example._tcp', {b'ttl': 300, 
           b'type': b'SRV', 
           b'value': {b'port': 1234, 
                      b'priority': 0, 
                      b'target': b'nc.unit.tests.', 
                      b'weight': 5}})
        srv_record_with_sub = Record.new(zone, b'_example._tcp.sub', {b'ttl': 300, 
           b'type': b'SRV', 
           b'value': {b'port': 1234, 
                      b'priority': 0, 
                      b'target': b'nc.unit.tests.', 
                      b'weight': 5}})
        srv_record_contents = provider._gen_data(srv_record)
        srv_record_with_sub_contents = provider._gen_data(srv_record_with_sub)
        self.assertEquals({b'name': b'_example._tcp.unit.tests', 
           b'ttl': 300, 
           b'type': b'SRV', 
           b'data': {b'service': b'_example', 
                     b'proto': b'_tcp', 
                     b'name': b'unit.tests.', 
                     b'priority': 0, 
                     b'weight': 5, 
                     b'port': 1234, 
                     b'target': b'nc.unit.tests'}}, list(srv_record_contents)[0])
        self.assertEquals({b'name': b'_example._tcp.sub.unit.tests', 
           b'ttl': 300, 
           b'type': b'SRV', 
           b'data': {b'service': b'_example', 
                     b'proto': b'_tcp', 
                     b'name': b'sub', 
                     b'priority': 0, 
                     b'weight': 5, 
                     b'port': 1234, 
                     b'target': b'nc.unit.tests'}}, list(srv_record_with_sub_contents)[0])

    def test_alias(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        provider.zone_records = Mock(return_value=[
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': b'CNAME', 
            b'name': b'unit.tests', 
            b'content': b'www.unit.tests', 
            b'proxiable': True, 
            b'proxied': False, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}}])
        zone = Zone(b'unit.tests.', [])
        provider.populate(zone)
        self.assertEquals(1, len(zone.records))
        record = list(zone.records)[0]
        self.assertEquals(b'', record.name)
        self.assertEquals(b'unit.tests.', record.fqdn)
        self.assertEquals(b'ALIAS', record._type)
        self.assertEquals(b'www.unit.tests.', record.value)
        contents = provider._gen_data(record)
        self.assertEquals({b'content': b'www.unit.tests.', 
           b'name': b'unit.tests', 
           b'proxied': False, 
           b'ttl': 300, 
           b'type': b'CNAME'}, list(contents)[0])

    def test_gen_key(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        for expected, data in (
         (
          b'foo.bar.com.',
          {b'content': b'foo.bar.com.', 
             b'type': b'CNAME'}),
         (
          b'10 foo.bar.com.',
          {b'content': b'foo.bar.com.', 
             b'priority': 10, 
             b'type': b'MX'}),
         (
          b'0 tag some-value',
          {b'data': {b'flags': 0, 
                       b'tag': b'tag', 
                       b'value': b'some-value'}, 
             b'type': b'CAA'}),
         (
          b'42 100 thing-were-pointed.at 101',
          {b'data': {b'port': 42, 
                       b'priority': 100, 
                       b'target': b'thing-were-pointed.at', 
                       b'weight': 101}, 
             b'type': b'SRV'})):
            self.assertEqual(expected, provider._gen_key(data))

    def test_cdn(self):
        provider = CloudflareProvider(b'test', b'email', b'token', True)
        provider.zone_records = Mock(return_value=[
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': b'CNAME', 
            b'name': b'cname.unit.tests', 
            b'content': b'www.unit.tests', 
            b'proxiable': True, 
            b'proxied': True, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}},
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': b'A', 
            b'name': b'a.unit.tests', 
            b'content': b'1.1.1.1', 
            b'proxiable': True, 
            b'proxied': True, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}},
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': b'A', 
            b'name': b'a.unit.tests', 
            b'content': b'1.1.1.2', 
            b'proxiable': True, 
            b'proxied': True, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}},
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': b'A', 
            b'name': b'multi.unit.tests', 
            b'content': b'1.1.1.3', 
            b'proxiable': True, 
            b'proxied': True, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}},
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': b'AAAA', 
            b'name': b'multi.unit.tests', 
            b'content': b'::1', 
            b'proxiable': True, 
            b'proxied': True, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}}])
        zone = Zone(b'unit.tests.', [])
        provider.populate(zone)
        self.assertEquals(3, len(zone.records))
        ordered = sorted(zone.records, key=lambda r: r.name)
        record = ordered[0]
        self.assertEquals(b'a', record.name)
        self.assertEquals(b'a.unit.tests.', record.fqdn)
        self.assertEquals(b'CNAME', record._type)
        self.assertEquals(b'a.unit.tests.cdn.cloudflare.net.', record.value)
        record = ordered[1]
        self.assertEquals(b'cname', record.name)
        self.assertEquals(b'cname.unit.tests.', record.fqdn)
        self.assertEquals(b'CNAME', record._type)
        self.assertEquals(b'cname.unit.tests.cdn.cloudflare.net.', record.value)
        record = ordered[2]
        self.assertEquals(b'multi', record.name)
        self.assertEquals(b'multi.unit.tests.', record.fqdn)
        self.assertEquals(b'CNAME', record._type)
        self.assertEquals(b'multi.unit.tests.cdn.cloudflare.net.', record.value)
        wanted = Zone(b'unit.tests.', [])
        wanted.add_record(Record.new(wanted, b'cname', {b'ttl': 300, 
           b'type': b'CNAME', 
           b'value': b'change.unit.tests.cdn.cloudflare.net.'}))
        wanted.add_record(Record.new(wanted, b'new', {b'ttl': 300, 
           b'type': b'CNAME', 
           b'value': b'new.unit.tests.cdn.cloudflare.net.'}))
        wanted.add_record(Record.new(wanted, b'created', {b'ttl': 300, 
           b'type': b'CNAME', 
           b'value': b'www.unit.tests.'}))
        plan = provider.plan(wanted)
        self.assertEquals(1, len(plan.changes))

    def test_cdn_alias(self):
        provider = CloudflareProvider(b'test', b'email', b'token', True)
        provider.zone_records = Mock(return_value=[
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': b'CNAME', 
            b'name': b'unit.tests', 
            b'content': b'www.unit.tests', 
            b'proxiable': True, 
            b'proxied': True, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}}])
        zone = Zone(b'unit.tests.', [])
        provider.populate(zone)
        self.assertEquals(1, len(zone.records))
        record = list(zone.records)[0]
        self.assertEquals(b'', record.name)
        self.assertEquals(b'unit.tests.', record.fqdn)
        self.assertEquals(b'ALIAS', record._type)
        self.assertEquals(b'unit.tests.cdn.cloudflare.net.', record.value)
        wanted = Zone(b'unit.tests.', [])
        wanted.add_record(Record.new(wanted, b'', {b'ttl': 300, 
           b'type': b'ALIAS', 
           b'value': b'change.unit.tests.cdn.cloudflare.net.'}))
        plan = provider.plan(wanted)
        self.assertEquals(False, hasattr(plan, b'changes'))

    def test_unproxiabletype_recordfor_returnsrecordwithnocloudflare(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        name = b'unit.tests'
        _type = b'NS'
        zone_records = [
         {b'id': b'fc12ab34cd5611334422ab3322997654', 
            b'type': _type, 
            b'name': name, 
            b'content': b'ns2.foo.bar', 
            b'proxiable': True, 
            b'proxied': False, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}}]
        provider.zone_records = Mock(return_value=zone_records)
        zone = Zone(b'unit.tests.', [])
        provider.populate(zone)
        record = provider._record_for(zone, name, _type, zone_records, False)
        self.assertFalse(b'cloudflare' in record._octodns)

    def test_proxiabletype_recordfor_retrecordwithcloudflareunproxied(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        name = b'multi.unit.tests'
        _type = b'AAAA'
        zone_records = [
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': _type, 
            b'name': name, 
            b'content': b'::1', 
            b'proxiable': True, 
            b'proxied': False, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}}]
        provider.zone_records = Mock(return_value=zone_records)
        zone = Zone(b'unit.tests.', [])
        provider.populate(zone)
        record = provider._record_for(zone, name, _type, zone_records, False)
        self.assertFalse(record._octodns[b'cloudflare'][b'proxied'])

    def test_proxiabletype_recordfor_returnsrecordwithcloudflareproxied(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        name = b'multi.unit.tests'
        _type = b'AAAA'
        zone_records = [
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': _type, 
            b'name': name, 
            b'content': b'::1', 
            b'proxiable': True, 
            b'proxied': True, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}}]
        provider.zone_records = Mock(return_value=zone_records)
        zone = Zone(b'unit.tests.', [])
        provider.populate(zone)
        record = provider._record_for(zone, name, _type, zone_records, False)
        self.assertTrue(record._octodns[b'cloudflare'][b'proxied'])

    def test_proxiedrecordandnewttl_includechange_returnsfalse(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        zone = Zone(b'unit.tests.', [])
        existing = set_record_proxied_flag(Record.new(zone, b'a', {b'ttl': 1, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1', b'2.2.2.2']}), True)
        new = Record.new(zone, b'a', {b'ttl': 300, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1', b'2.2.2.2']})
        change = Update(existing, new)
        include_change = provider._include_change(change)
        self.assertFalse(include_change)

    def test_unproxiabletype_gendata_returnsnoproxied(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        zone = Zone(b'unit.tests.', [])
        record = Record.new(zone, b'a', {b'ttl': 3600, 
           b'type': b'NS', 
           b'value': b'ns1.unit.tests.'})
        data = next(provider._gen_data(record))
        self.assertFalse(b'proxied' in data)

    def test_proxiabletype_gendata_returnsunproxied(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        zone = Zone(b'unit.tests.', [])
        record = set_record_proxied_flag(Record.new(zone, b'a', {b'ttl': 300, 
           b'type': b'A', 
           b'value': b'1.2.3.4'}), False)
        data = next(provider._gen_data(record))
        self.assertFalse(data[b'proxied'])

    def test_proxiabletype_gendata_returnsproxied(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        zone = Zone(b'unit.tests.', [])
        record = set_record_proxied_flag(Record.new(zone, b'a', {b'ttl': 300, 
           b'type': b'A', 
           b'value': b'1.2.3.4'}), True)
        data = next(provider._gen_data(record))
        self.assertTrue(data[b'proxied'])

    def test_createrecord_extrachanges_returnsemptylist(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        provider.zone_records = Mock(return_value=[])
        existing = Zone(b'unit.tests.', [])
        provider.populate(existing)
        provider.zone_records = Mock(return_value=[
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': b'CNAME', 
            b'name': b'a.unit.tests', 
            b'content': b'www.unit.tests', 
            b'proxiable': True, 
            b'proxied': True, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}}])
        desired = Zone(b'unit.tests.', [])
        provider.populate(desired)
        changes = existing.changes(desired, provider)
        extra_changes = provider._extra_changes(existing, desired, changes)
        self.assertFalse(extra_changes)

    def test_updaterecord_extrachanges_returnsemptylist(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        provider.zone_records = Mock(return_value=[
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': b'CNAME', 
            b'name': b'a.unit.tests', 
            b'content': b'www.unit.tests', 
            b'proxiable': True, 
            b'proxied': True, 
            b'ttl': 120, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}}])
        existing = Zone(b'unit.tests.', [])
        provider.populate(existing)
        provider.zone_records = Mock(return_value=[
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': b'CNAME', 
            b'name': b'a.unit.tests', 
            b'content': b'www.unit.tests', 
            b'proxiable': True, 
            b'proxied': True, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}}])
        desired = Zone(b'unit.tests.', [])
        provider.populate(desired)
        changes = existing.changes(desired, provider)
        extra_changes = provider._extra_changes(existing, desired, changes)
        self.assertFalse(extra_changes)

    def test_deleterecord_extrachanges_returnsemptylist(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        provider.zone_records = Mock(return_value=[
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': b'CNAME', 
            b'name': b'a.unit.tests', 
            b'content': b'www.unit.tests', 
            b'proxiable': True, 
            b'proxied': True, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}}])
        existing = Zone(b'unit.tests.', [])
        provider.populate(existing)
        provider.zone_records = Mock(return_value=[])
        desired = Zone(b'unit.tests.', [])
        provider.populate(desired)
        changes = existing.changes(desired, provider)
        extra_changes = provider._extra_changes(existing, desired, changes)
        self.assertFalse(extra_changes)

    def test_proxify_extrachanges_returnsupdatelist(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        provider.zone_records = Mock(return_value=[
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': b'CNAME', 
            b'name': b'a.unit.tests', 
            b'content': b'www.unit.tests', 
            b'proxiable': True, 
            b'proxied': False, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}}])
        existing = Zone(b'unit.tests.', [])
        provider.populate(existing)
        provider.zone_records = Mock(return_value=[
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': b'CNAME', 
            b'name': b'a.unit.tests', 
            b'content': b'www.unit.tests', 
            b'proxiable': True, 
            b'proxied': True, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}}])
        desired = Zone(b'unit.tests.', [])
        provider.populate(desired)
        changes = existing.changes(desired, provider)
        extra_changes = provider._extra_changes(existing, desired, changes)
        self.assertEquals(1, len(extra_changes))
        self.assertFalse(extra_changes[0].existing._octodns[b'cloudflare'][b'proxied'])
        self.assertTrue(extra_changes[0].new._octodns[b'cloudflare'][b'proxied'])

    def test_unproxify_extrachanges_returnsupdatelist(self):
        provider = CloudflareProvider(b'test', b'email', b'token')
        provider.zone_records = Mock(return_value=[
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': b'CNAME', 
            b'name': b'a.unit.tests', 
            b'content': b'www.unit.tests', 
            b'proxiable': True, 
            b'proxied': True, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}}])
        existing = Zone(b'unit.tests.', [])
        provider.populate(existing)
        provider.zone_records = Mock(return_value=[
         {b'id': b'fc12ab34cd5611334422ab3322997642', 
            b'type': b'CNAME', 
            b'name': b'a.unit.tests', 
            b'content': b'www.unit.tests', 
            b'proxiable': True, 
            b'proxied': False, 
            b'ttl': 300, 
            b'locked': False, 
            b'zone_id': b'ff12ab34cd5611334422ab3322997650', 
            b'zone_name': b'unit.tests', 
            b'modified_on': b'2017-03-11T18:01:43.420689Z', 
            b'created_on': b'2017-03-11T18:01:43.420689Z', 
            b'meta': {b'auto_added': False}}])
        desired = Zone(b'unit.tests.', [])
        provider.populate(desired)
        changes = existing.changes(desired, provider)
        extra_changes = provider._extra_changes(existing, desired, changes)
        self.assertEquals(1, len(extra_changes))
        self.assertTrue(extra_changes[0].existing._octodns[b'cloudflare'][b'proxied'])
        self.assertFalse(extra_changes[0].new._octodns[b'cloudflare'][b'proxied'])

    def test_emailless_auth(self):
        provider = CloudflareProvider(b'test', token=b'token 123', email=b'email 234')
        headers = provider._sess.headers
        self.assertEquals(b'email 234', headers[b'X-Auth-Email'])
        self.assertEquals(b'token 123', headers[b'X-Auth-Key'])
        provider = CloudflareProvider(b'test', token=b'token 123')
        headers = provider._sess.headers
        self.assertEquals(b'Bearer token 123', headers[b'Authorization'])