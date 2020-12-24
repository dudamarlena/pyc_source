# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_rackspace.py
# Compiled at: 2020-01-06 16:40:45
from __future__ import absolute_import, division, print_function, unicode_literals
import json, re
from six import text_type
from six.moves.urllib.parse import urlparse
from unittest import TestCase
from requests import HTTPError
from requests_mock import ANY, mock as requests_mock
from octodns.provider.rackspace import RackspaceProvider
from octodns.record import Record
from octodns.zone import Zone
EMPTY_TEXT = b'\n{\n  "totalEntries" : 0,\n  "records" : []\n}\n'
with open(b'./tests/fixtures/rackspace-auth-response.json') as (fh):
    AUTH_RESPONSE = fh.read()
with open(b'./tests/fixtures/rackspace-list-domains-response.json') as (fh):
    LIST_DOMAINS_RESPONSE = fh.read()
with open(b'./tests/fixtures/rackspace-sample-recordset-page1.json') as (fh):
    RECORDS_PAGE_1 = fh.read()
with open(b'./tests/fixtures/rackspace-sample-recordset-page2.json') as (fh):
    RECORDS_PAGE_2 = fh.read()

class TestRackspaceProvider(TestCase):

    def setUp(self):
        with requests_mock() as (mock):
            mock.post(ANY, status_code=200, text=AUTH_RESPONSE)
            self.provider = RackspaceProvider(b'identity', b'test', b'api-key', b'0')
            self.assertTrue(mock.called_once)

    def test_bad_auth(self):
        with requests_mock() as (mock):
            mock.get(ANY, status_code=401, text=b'Unauthorized')
            with self.assertRaises(Exception) as (ctx):
                zone = Zone(b'unit.tests.', [])
                self.provider.populate(zone)
            self.assertTrue(b'unauthorized' in text_type(ctx.exception))
            self.assertTrue(mock.called_once)

    def test_server_error(self):
        with requests_mock() as (mock):
            mock.get(ANY, status_code=502, text=b'Things caught fire')
            with self.assertRaises(HTTPError) as (ctx):
                zone = Zone(b'unit.tests.', [])
                self.provider.populate(zone)
            self.assertEquals(502, ctx.exception.response.status_code)
            self.assertTrue(mock.called_once)

    def test_nonexistent_zone(self):
        with requests_mock() as (mock):
            mock.get(ANY, status_code=404, json={b'error': b"Could not find domain 'unit.tests.'"})
            zone = Zone(b'unit.tests.', [])
            exists = self.provider.populate(zone)
            self.assertEquals(set(), zone.records)
            self.assertTrue(mock.called_once)
            self.assertFalse(exists)

    def test_multipage_populate(self):
        with requests_mock() as (mock):
            mock.get(re.compile(b'domains$'), status_code=200, text=LIST_DOMAINS_RESPONSE)
            mock.get(re.compile(b'records'), status_code=200, text=RECORDS_PAGE_1)
            mock.get(re.compile(b'records.*offset=3'), status_code=200, text=RECORDS_PAGE_2)
            zone = Zone(b'unit.tests.', [])
            self.provider.populate(zone)
            self.assertEquals(5, len(zone.records))

    def test_plan_disappearing_ns_records(self):
        expected = Zone(b'unit.tests.', [])
        expected.add_record(Record.new(expected, b'', {b'type': b'NS', 
           b'ttl': 600, 
           b'values': [
                     b'8.8.8.8.', b'9.9.9.9.']}))
        expected.add_record(Record.new(expected, b'sub', {b'type': b'NS', 
           b'ttl': 600, 
           b'values': [
                     b'8.8.8.8.', b'9.9.9.9.']}))
        with requests_mock() as (mock):
            mock.get(re.compile(b'domains$'), status_code=200, text=LIST_DOMAINS_RESPONSE)
            mock.get(re.compile(b'records'), status_code=200, text=EMPTY_TEXT)
            plan = self.provider.plan(expected)
            self.assertTrue(mock.called)
            self.assertTrue(plan.exists)
            self.assertEquals(1, len(plan.changes))

    def test_fqdn_a_record(self):
        expected = Zone(b'example.com.', [])
        with requests_mock() as (list_mock):
            list_mock.get(re.compile(b'domains$'), status_code=200, text=LIST_DOMAINS_RESPONSE)
            list_mock.get(re.compile(b'records'), status_code=200, json={b'records': [
                          {b'type': b'A', b'name': b'foo.example.com', 
                             b'id': b'A-111111', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 300}]})
            plan = self.provider.plan(expected)
            self.assertTrue(list_mock.called)
            self.assertEqual(1, len(plan.changes))
            self.assertTrue(plan.changes[0].existing.fqdn == b'foo.example.com.')
        with requests_mock() as (mock):

            def _assert_deleting(request, context):
                parts = urlparse(request.url)
                self.assertEqual(b'id=A-111111', parts.query)

            mock.get(re.compile(b'domains$'), status_code=200, text=LIST_DOMAINS_RESPONSE)
            mock.delete(re.compile(b'domains/.*/records?.*'), status_code=202, text=_assert_deleting)
            self.provider.apply(plan)
            self.assertTrue(mock.called)

    def _test_apply_with_data(self, data):
        expected = Zone(b'unit.tests.', [])
        for record in data.OtherRecords:
            expected.add_record(Record.new(expected, record[b'subdomain'], record[b'data']))

        with requests_mock() as (list_mock):
            list_mock.get(re.compile(b'domains$'), status_code=200, text=LIST_DOMAINS_RESPONSE)
            list_mock.get(re.compile(b'records'), status_code=200, json=data.OwnRecords)
            plan = self.provider.plan(expected)
            self.assertTrue(list_mock.called)
            if not data.ExpectChanges:
                self.assertFalse(plan)
                return
        with requests_mock() as (mock):
            called = set()

            def make_assert_sending_right_body(expected):

                def _assert_sending_right_body(request, _context):
                    called.add(request.method)
                    if request.method != b'DELETE':
                        self.assertEqual(request.headers[b'content-type'], b'application/json')
                        self.assertDictEqual(expected, json.loads(request.body))
                    else:
                        parts = urlparse(request.url)
                        self.assertEqual(expected, parts.query)
                    return b''

                return _assert_sending_right_body

            mock.get(re.compile(b'domains$'), status_code=200, text=LIST_DOMAINS_RESPONSE)
            mock.post(re.compile(b'domains/.*/records$'), status_code=202, text=make_assert_sending_right_body(data.ExpectedAdditions))
            mock.delete(re.compile(b'domains/.*/records?.*'), status_code=202, text=make_assert_sending_right_body(data.ExpectedDeletions))
            mock.put(re.compile(b'domains/.*/records$'), status_code=202, text=make_assert_sending_right_body(data.ExpectedUpdates))
            self.provider.apply(plan)
            self.assertTrue(data.ExpectedAdditions is None or b'POST' in called)
            self.assertTrue(data.ExpectedDeletions is None or b'DELETE' in called)
            self.assertTrue(data.ExpectedUpdates is None or b'PUT' in called)
        return

    def test_apply_no_change_empty(self):

        class TestData(object):
            OtherRecords = []
            OwnRecords = {b'totalEntries': 0, 
               b'records': []}
            ExpectChanges = False
            ExpectedAdditions = None
            ExpectedDeletions = None
            ExpectedUpdates = None

        return self._test_apply_with_data(TestData)

    def test_apply_no_change_a_records(self):

        class TestData(object):
            OtherRecords = [
             {b'subdomain': b'', 
                b'data': {b'type': b'A', 
                          b'ttl': 300, 
                          b'values': [
                                    b'1.2.3.4', b'1.2.3.5', b'1.2.3.6']}}]
            OwnRecords = {b'totalEntries': 3, 
               b'records': [
                          {b'name': b'unit.tests', 
                             b'id': b'A-111111', 
                             b'type': b'A', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 300},
                          {b'name': b'unit.tests', 
                             b'id': b'A-222222', 
                             b'type': b'A', 
                             b'data': b'1.2.3.5', 
                             b'ttl': 300},
                          {b'name': b'unit.tests', 
                             b'id': b'A-333333', 
                             b'type': b'A', 
                             b'data': b'1.2.3.6', 
                             b'ttl': 300}]}
            ExpectChanges = False
            ExpectedAdditions = None
            ExpectedDeletions = None
            ExpectedUpdates = None

        return self._test_apply_with_data(TestData)

    def test_apply_no_change_a_records_cross_zone(self):

        class TestData(object):
            OtherRecords = [
             {b'subdomain': b'foo', 
                b'data': {b'type': b'A', 
                          b'ttl': 300, 
                          b'value': b'1.2.3.4'}},
             {b'subdomain': b'bar', 
                b'data': {b'type': b'A', 
                          b'ttl': 300, 
                          b'value': b'1.2.3.4'}}]
            OwnRecords = {b'totalEntries': 3, 
               b'records': [
                          {b'name': b'foo.unit.tests', 
                             b'id': b'A-111111', 
                             b'type': b'A', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 300},
                          {b'name': b'bar.unit.tests', 
                             b'id': b'A-222222', 
                             b'type': b'A', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 300}]}
            ExpectChanges = False
            ExpectedAdditions = None
            ExpectedDeletions = None
            ExpectedUpdates = None

        return self._test_apply_with_data(TestData)

    def test_apply_one_addition(self):

        class TestData(object):
            OtherRecords = [
             {b'subdomain': b'', 
                b'data': {b'type': b'A', 
                          b'ttl': 300, 
                          b'value': b'1.2.3.4'}},
             {b'subdomain': b'foo', 
                b'data': {b'type': b'NS', 
                          b'ttl': 300, 
                          b'value': b'ns.example.com.'}}]
            OwnRecords = {b'totalEntries': 0, 
               b'records': []}
            ExpectChanges = True
            ExpectedAdditions = {b'records': [
                          {b'name': b'unit.tests', 
                             b'type': b'A', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 300},
                          {b'name': b'foo.unit.tests', 
                             b'type': b'NS', 
                             b'data': b'ns.example.com', 
                             b'ttl': 300}]}
            ExpectedDeletions = None
            ExpectedUpdates = None

        return self._test_apply_with_data(TestData)

    def test_apply_create_MX(self):

        class TestData(object):
            OtherRecords = [
             {b'subdomain': b'', 
                b'data': {b'type': b'MX', 
                          b'ttl': 300, 
                          b'value': {b'value': b'mail1.example.com.', 
                                     b'priority': 1}}},
             {b'subdomain': b'foo', 
                b'data': {b'type': b'MX', 
                          b'ttl': 300, 
                          b'value': {b'value': b'mail2.example.com.', 
                                     b'priority': 2}}}]
            OwnRecords = {b'totalEntries': 0, 
               b'records': []}
            ExpectChanges = True
            ExpectedAdditions = {b'records': [
                          {b'name': b'foo.unit.tests', 
                             b'type': b'MX', 
                             b'data': b'mail2.example.com', 
                             b'priority': 2, 
                             b'ttl': 300},
                          {b'name': b'unit.tests', 
                             b'type': b'MX', 
                             b'data': b'mail1.example.com', 
                             b'priority': 1, 
                             b'ttl': 300}]}
            ExpectedDeletions = None
            ExpectedUpdates = None

        return self._test_apply_with_data(TestData)

    def test_apply_multiple_additions_splatting(self):

        class TestData(object):
            OtherRecords = [
             {b'subdomain': b'', 
                b'data': {b'type': b'A', 
                          b'ttl': 300, 
                          b'values': [
                                    b'1.2.3.4', b'1.2.3.5', b'1.2.3.6']}},
             {b'subdomain': b'foo', 
                b'data': {b'type': b'NS', 
                          b'ttl': 300, 
                          b'values': [
                                    b'ns1.example.com.', b'ns2.example.com.']}}]
            OwnRecords = {b'totalEntries': 0, 
               b'records': []}
            ExpectChanges = True
            ExpectedAdditions = {b'records': [
                          {b'name': b'unit.tests', 
                             b'type': b'A', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 300},
                          {b'name': b'unit.tests', 
                             b'type': b'A', 
                             b'data': b'1.2.3.5', 
                             b'ttl': 300},
                          {b'name': b'unit.tests', 
                             b'type': b'A', 
                             b'data': b'1.2.3.6', 
                             b'ttl': 300},
                          {b'name': b'foo.unit.tests', 
                             b'type': b'NS', 
                             b'data': b'ns1.example.com', 
                             b'ttl': 300},
                          {b'name': b'foo.unit.tests', 
                             b'type': b'NS', 
                             b'data': b'ns2.example.com', 
                             b'ttl': 300}]}
            ExpectedDeletions = None
            ExpectedUpdates = None

        return self._test_apply_with_data(TestData)

    def test_apply_multiple_additions_namespaced(self):

        class TestData(object):
            OtherRecords = [
             {b'subdomain': b'foo', 
                b'data': {b'type': b'A', 
                          b'ttl': 300, 
                          b'value': b'1.2.3.4'}},
             {b'subdomain': b'bar', 
                b'data': {b'type': b'A', 
                          b'ttl': 300, 
                          b'value': b'1.2.3.4'}},
             {b'subdomain': b'foo', 
                b'data': {b'type': b'NS', 
                          b'ttl': 300, 
                          b'value': b'ns.example.com.'}}]
            OwnRecords = {b'totalEntries': 0, 
               b'records': []}
            ExpectChanges = True
            ExpectedAdditions = {b'records': [
                          {b'name': b'bar.unit.tests', 
                             b'type': b'A', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 300},
                          {b'name': b'foo.unit.tests', 
                             b'type': b'A', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 300},
                          {b'name': b'foo.unit.tests', 
                             b'type': b'NS', 
                             b'data': b'ns.example.com', 
                             b'ttl': 300}]}
            ExpectedDeletions = None
            ExpectedUpdates = None

        return self._test_apply_with_data(TestData)

    def test_apply_single_deletion(self):

        class TestData(object):
            OtherRecords = []
            OwnRecords = {b'totalEntries': 1, 
               b'records': [
                          {b'name': b'unit.tests', 
                             b'id': b'A-111111', 
                             b'type': b'A', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 300},
                          {b'name': b'foo.unit.tests', 
                             b'id': b'NS-111111', 
                             b'type': b'NS', 
                             b'data': b'ns.example.com', 
                             b'ttl': 300}]}
            ExpectChanges = True
            ExpectedAdditions = None
            ExpectedDeletions = b'id=A-111111&id=NS-111111'
            ExpectedUpdates = None

        return self._test_apply_with_data(TestData)

    def test_apply_multiple_deletions(self):

        class TestData(object):
            OtherRecords = [
             {b'subdomain': b'', 
                b'data': {b'type': b'A', 
                          b'ttl': 300, 
                          b'value': b'1.2.3.5'}}]
            OwnRecords = {b'totalEntries': 3, 
               b'records': [
                          {b'name': b'unit.tests', 
                             b'id': b'A-111111', 
                             b'type': b'A', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 300},
                          {b'name': b'unit.tests', 
                             b'id': b'A-222222', 
                             b'type': b'A', 
                             b'data': b'1.2.3.5', 
                             b'ttl': 300},
                          {b'name': b'unit.tests', 
                             b'id': b'A-333333', 
                             b'type': b'A', 
                             b'data': b'1.2.3.6', 
                             b'ttl': 300},
                          {b'name': b'foo.unit.tests', 
                             b'id': b'NS-111111', 
                             b'type': b'NS', 
                             b'data': b'ns.example.com', 
                             b'ttl': 300}]}
            ExpectChanges = True
            ExpectedAdditions = None
            ExpectedDeletions = b'id=A-111111&id=A-333333&id=NS-111111'
            ExpectedUpdates = {b'records': [
                          {b'name': b'unit.tests', 
                             b'id': b'A-222222', 
                             b'data': b'1.2.3.5', 
                             b'ttl': 300}]}

        return self._test_apply_with_data(TestData)

    def test_apply_multiple_deletions_cross_zone(self):

        class TestData(object):
            OtherRecords = [
             {b'subdomain': b'', 
                b'data': {b'type': b'A', 
                          b'ttl': 300, 
                          b'value': b'1.2.3.4'}}]
            OwnRecords = {b'totalEntries': 3, 
               b'records': [
                          {b'name': b'unit.tests', 
                             b'id': b'A-111111', 
                             b'type': b'A', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 300},
                          {b'name': b'foo.unit.tests', 
                             b'id': b'A-222222', 
                             b'type': b'A', 
                             b'data': b'1.2.3.5', 
                             b'ttl': 300},
                          {b'name': b'bar.unit.tests', 
                             b'id': b'A-333333', 
                             b'type': b'A', 
                             b'data': b'1.2.3.6', 
                             b'ttl': 300}]}
            ExpectChanges = True
            ExpectedAdditions = None
            ExpectedDeletions = b'id=A-222222&id=A-333333'
            ExpectedUpdates = None

        return self._test_apply_with_data(TestData)

    def test_apply_delete_cname(self):

        class TestData(object):
            OtherRecords = []
            OwnRecords = {b'totalEntries': 3, 
               b'records': [
                          {b'name': b'foo.unit.tests', 
                             b'id': b'CNAME-111111', 
                             b'type': b'CNAME', 
                             b'data': b'a.example.com', 
                             b'ttl': 300}]}
            ExpectChanges = True
            ExpectedAdditions = None
            ExpectedDeletions = b'id=CNAME-111111'
            ExpectedUpdates = None

        return self._test_apply_with_data(TestData)

    def test_apply_single_update(self):

        class TestData(object):
            OtherRecords = [
             {b'subdomain': b'', 
                b'data': {b'type': b'A', 
                          b'ttl': 3600, 
                          b'value': b'1.2.3.4'}}]
            OwnRecords = {b'totalEntries': 1, 
               b'records': [
                          {b'name': b'unit.tests', 
                             b'id': b'A-111111', 
                             b'type': b'A', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 300}]}
            ExpectChanges = True
            ExpectedAdditions = None
            ExpectedDeletions = None
            ExpectedUpdates = {b'records': [
                          {b'name': b'unit.tests', 
                             b'id': b'A-111111', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 3600}]}

        return self._test_apply_with_data(TestData)

    def test_apply_update_TXT(self):

        class TestData(object):
            OtherRecords = [
             {b'subdomain': b'', 
                b'data': {b'type': b'TXT', 
                          b'ttl': 300, 
                          b'value': b'othervalue'}}]
            OwnRecords = {b'totalEntries': 1, 
               b'records': [
                          {b'name': b'unit.tests', 
                             b'id': b'TXT-111111', 
                             b'type': b'TXT', 
                             b'data': b'somevalue', 
                             b'ttl': 300}]}
            ExpectChanges = True
            ExpectedAdditions = {b'records': [
                          {b'name': b'unit.tests', 
                             b'type': b'TXT', 
                             b'data': b'othervalue', 
                             b'ttl': 300}]}
            ExpectedDeletions = b'id=TXT-111111'
            ExpectedUpdates = None

        return self._test_apply_with_data(TestData)

    def test_apply_update_MX(self):

        class TestData(object):
            OtherRecords = [
             {b'subdomain': b'', 
                b'data': {b'type': b'MX', 
                          b'ttl': 300, 
                          b'value': {b'priority': 50, b'value': b'mx.test.com.'}}}]
            OwnRecords = {b'totalEntries': 1, 
               b'records': [
                          {b'name': b'unit.tests', 
                             b'id': b'MX-111111', 
                             b'type': b'MX', 
                             b'priority': 20, 
                             b'data': b'mx.test.com', 
                             b'ttl': 300}]}
            ExpectChanges = True
            ExpectedAdditions = {b'records': [
                          {b'name': b'unit.tests', 
                             b'type': b'MX', 
                             b'priority': 50, 
                             b'data': b'mx.test.com', 
                             b'ttl': 300}]}
            ExpectedDeletions = b'id=MX-111111'
            ExpectedUpdates = None

        return self._test_apply_with_data(TestData)

    def test_apply_multiple_updates(self):

        class TestData(object):
            OtherRecords = [
             {b'subdomain': b'', 
                b'data': {b'type': b'A', 
                          b'ttl': 3600, 
                          b'values': [
                                    b'1.2.3.4', b'1.2.3.5', b'1.2.3.6']}}]
            OwnRecords = {b'totalEntries': 3, 
               b'records': [
                          {b'name': b'unit.tests', 
                             b'id': b'A-111111', 
                             b'type': b'A', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 300},
                          {b'name': b'unit.tests', 
                             b'id': b'A-222222', 
                             b'type': b'A', 
                             b'data': b'1.2.3.5', 
                             b'ttl': 300},
                          {b'name': b'unit.tests', 
                             b'id': b'A-333333', 
                             b'type': b'A', 
                             b'data': b'1.2.3.6', 
                             b'ttl': 300}]}
            ExpectChanges = True
            ExpectedAdditions = None
            ExpectedDeletions = None
            ExpectedUpdates = {b'records': [
                          {b'name': b'unit.tests', 
                             b'id': b'A-111111', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 3600},
                          {b'name': b'unit.tests', 
                             b'id': b'A-222222', 
                             b'data': b'1.2.3.5', 
                             b'ttl': 3600},
                          {b'name': b'unit.tests', 
                             b'id': b'A-333333', 
                             b'data': b'1.2.3.6', 
                             b'ttl': 3600}]}

        return self._test_apply_with_data(TestData)

    def test_apply_multiple_updates_cross_zone(self):

        class TestData(object):
            OtherRecords = [
             {b'subdomain': b'foo', 
                b'data': {b'type': b'A', 
                          b'ttl': 3600, 
                          b'value': b'1.2.3.4'}},
             {b'subdomain': b'bar', 
                b'data': {b'type': b'A', 
                          b'ttl': 3600, 
                          b'value': b'1.2.3.4'}}]
            OwnRecords = {b'totalEntries': 2, 
               b'records': [
                          {b'name': b'foo.unit.tests', 
                             b'id': b'A-111111', 
                             b'type': b'A', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 300},
                          {b'name': b'bar.unit.tests', 
                             b'id': b'A-222222', 
                             b'type': b'A', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 300}]}
            ExpectChanges = True
            ExpectedAdditions = None
            ExpectedDeletions = None
            ExpectedUpdates = {b'records': [
                          {b'name': b'bar.unit.tests', 
                             b'id': b'A-222222', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 3600},
                          {b'name': b'foo.unit.tests', 
                             b'id': b'A-111111', 
                             b'data': b'1.2.3.4', 
                             b'ttl': 3600}]}

        return self._test_apply_with_data(TestData)