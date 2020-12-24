# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_googlecloud.py
# Compiled at: 2020-01-15 19:08:55
from __future__ import absolute_import, division, print_function, unicode_literals
from octodns.record import Create, Delete, Update, Record
from octodns.provider.googlecloud import GoogleCloudProvider
from octodns.zone import Zone
from octodns.provider.base import Plan, BaseProvider
from unittest import TestCase
from mock import Mock, patch, PropertyMock
zone = Zone(name=b'unit.tests.', sub_zones=[])
octo_records = []
octo_records.append(Record.new(zone, b'', {b'ttl': 0, 
   b'type': b'A', 
   b'values': [
             b'1.2.3.4', b'10.10.10.10']}))
octo_records.append(Record.new(zone, b'a', {b'ttl': 1, 
   b'type': b'A', 
   b'values': [
             b'1.2.3.4', b'1.1.1.1']}))
octo_records.append(Record.new(zone, b'aa', {b'ttl': 9001, 
   b'type': b'A', 
   b'values': [
             b'1.2.4.3']}))
octo_records.append(Record.new(zone, b'aaa', {b'ttl': 2, 
   b'type': b'A', 
   b'values': [
             b'1.1.1.3']}))
octo_records.append(Record.new(zone, b'cname', {b'ttl': 3, 
   b'type': b'CNAME', 
   b'value': b'a.unit.tests.'}))
octo_records.append(Record.new(zone, b'mx1', {b'ttl': 3, 
   b'type': b'MX', 
   b'values': [
             {b'priority': 10, 
                b'value': b'mx1.unit.tests.'},
             {b'priority': 20, 
                b'value': b'mx2.unit.tests.'}]}))
octo_records.append(Record.new(zone, b'mx2', {b'ttl': 3, 
   b'type': b'MX', 
   b'values': [
             {b'priority': 10, 
                b'value': b'mx1.unit.tests.'}]}))
octo_records.append(Record.new(zone, b'', {b'ttl': 4, 
   b'type': b'NS', 
   b'values': [
             b'ns1.unit.tests.', b'ns2.unit.tests.']}))
octo_records.append(Record.new(zone, b'foo', {b'ttl': 5, 
   b'type': b'NS', 
   b'value': b'ns1.unit.tests.'}))
octo_records.append(Record.new(zone, b'_srv._tcp', {b'ttl': 6, 
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
octo_records.append(Record.new(zone, b'_srv2._tcp', {b'ttl': 7, 
   b'type': b'SRV', 
   b'values': [
             {b'priority': 12, 
                b'weight': 17, 
                b'port': 1, 
                b'target': b'srvfoo.unit.tests.'}]}))
octo_records.append(Record.new(zone, b'txt1', {b'ttl': 8, 
   b'type': b'TXT', 
   b'value': b'txt singleton test'}))
octo_records.append(Record.new(zone, b'txt2', {b'ttl': 9, 
   b'type': b'TXT', 
   b'values': [
             b'txt multiple test', b'txt multiple test 2']}))
octo_records.append(Record.new(zone, b'naptr', {b'ttl': 9, 
   b'type': b'NAPTR', 
   b'values': [
             {b'order': 100, 
                b'preference': 10, 
                b'flags': b'S', 
                b'service': b'SIP+D2U', 
                b'regexp': b'!^.*$!sip:customer-service@unit.tests!', 
                b'replacement': b'_sip._udp.unit.tests.'}]}))
octo_records.append(Record.new(zone, b'caa', {b'ttl': 9, 
   b'type': b'CAA', 
   b'value': {b'flags': 0, 
              b'tag': b'issue', 
              b'value': b'ca.unit.tests'}}))
for record in octo_records:
    zone.add_record(record)

resource_record_sets = [
 (
  b'unit.tests.', b'A', 0, [b'1.2.3.4', b'10.10.10.10']),
 (
  b'a.unit.tests.', b'A', 1, [b'1.1.1.1', b'1.2.3.4']),
 (
  b'aa.unit.tests.', b'A', 9001, [b'1.2.4.3']),
 (
  b'aaa.unit.tests.', b'A', 2, [b'1.1.1.3']),
 (
  b'cname.unit.tests.', b'CNAME', 3, [b'a.unit.tests.']),
 (
  b'mx1.unit.tests.', b'MX', 3,
  [
   b'10 mx1.unit.tests.', b'20 mx2.unit.tests.']),
 (
  b'mx2.unit.tests.', b'MX', 3, [b'10 mx1.unit.tests.']),
 (
  b'unit.tests.', b'NS', 4, [b'ns1.unit.tests.', b'ns2.unit.tests.']),
 (
  b'foo.unit.tests.', b'NS', 5, [b'ns1.unit.tests.']),
 (
  b'_srv._tcp.unit.tests.', b'SRV', 6,
  [
   b'10 20 30 foo-1.unit.tests.', b'12 30 30 foo-2.unit.tests.']),
 (
  b'_srv2._tcp.unit.tests.', b'SRV', 7, [b'12 17 1 srvfoo.unit.tests.']),
 (
  b'txt1.unit.tests.', b'TXT', 8, [b'txt singleton test']),
 (
  b'txt2.unit.tests.', b'TXT', 9,
  [
   b'txt multiple test', b'txt multiple test 2']),
 (
  b'naptr.unit.tests.', b'NAPTR', 9,
  [
   b'100 10 "S" "SIP+D2U" "!^.*$!sip:customer-service@unit.tests!" _sip._udp.unit.tests.']),
 (
  b'caa.unit.tests.', b'CAA', 9, [b'0 issue ca.unit.tests'])]

class DummyResourceRecordSet:

    def __init__(self, record_name, record_type, ttl, rrdatas):
        self.name = record_name
        self.record_type = record_type
        self.ttl = ttl
        self.rrdatas = rrdatas

    def __eq__(self, other):
        try:
            return self.name == other.name and self.record_type == other.record_type and self.ttl == other.ttl and sorted(self.rrdatas) == sorted(other.rrdatas)
        except:
            return False

    def __repr__(self):
        return (b'{} {} {} {!s}').format(self.name, self.record_type, self.ttl, self.rrdatas)

    def __hash__(self):
        return hash(repr(self))


class DummyGoogleCloudZone:

    def __init__(self, dns_name, name=b''):
        self.dns_name = dns_name
        self.name = name

    def resource_record_set(self, *args):
        return DummyResourceRecordSet(*args)

    def list_resource_record_sets(self, *args):
        pass

    def create(self, *args, **kwargs):
        pass


class DummyIterator:
    """Returns a mock DummyIterator object to use in testing.
    This is because API calls for google cloud DNS, if paged, contains a
    "next_page_token", which can be used to grab a subsequent
    iterator with more results.

        :type return: DummyIterator
    """

    def __init__(self, list_of_stuff, page_token=None):
        self.iterable = iter(list_of_stuff)
        self.next_page_token = page_token

    def __iter__(self):
        return self

    def next(self):
        return next(self.iterable)

    def __next__(self):
        return next(self.iterable)


class TestGoogleCloudProvider(TestCase):

    @patch(b'octodns.provider.googlecloud.dns')
    def _get_provider(*args):
        """Returns a mock GoogleCloudProvider object to use in testing.

            :type return: GoogleCloudProvider
        """
        return GoogleCloudProvider(id=1, project=b'mock')

    @patch(b'octodns.provider.googlecloud.dns')
    def test___init__(self, *_):
        self.assertIsInstance(GoogleCloudProvider(id=1, credentials_file=b'test', project=b'unit test'), BaseProvider)
        self.assertIsInstance(GoogleCloudProvider(id=1), BaseProvider)

    @patch(b'octodns.provider.googlecloud.time.sleep')
    @patch(b'octodns.provider.googlecloud.dns')
    def test__apply(self, *_):

        class DummyDesired:

            def __init__(self, name, changes):
                self.name = name
                self.changes = changes

        apply_z = Zone(b'unit.tests.', [])
        create_r = Record.new(apply_z, b'', {b'ttl': 0, 
           b'type': b'A', 
           b'values': [
                     b'1.2.3.4', b'10.10.10.10']})
        delete_r = Record.new(apply_z, b'a', {b'ttl': 1, 
           b'type': b'A', 
           b'values': [
                     b'1.2.3.4', b'1.1.1.1']})
        update_existing_r = Record.new(apply_z, b'aa', {b'ttl': 9001, 
           b'type': b'A', 
           b'values': [
                     b'1.2.4.3']})
        update_new_r = Record.new(apply_z, b'aa', {b'ttl': 666, 
           b'type': b'A', 
           b'values': [
                     b'1.4.3.2']})
        gcloud_zone_mock = DummyGoogleCloudZone(b'unit.tests.', b'unit-tests')
        status_mock = Mock()
        return_values_for_status = iter([
         b'pending'] * 11 + [b'done', b'done'])
        type(status_mock).status = PropertyMock(side_effect=lambda : next(return_values_for_status))
        gcloud_zone_mock.changes = Mock(return_value=status_mock)
        provider = self._get_provider()
        provider.gcloud_client = Mock()
        provider._gcloud_zones = {b'unit.tests.': gcloud_zone_mock}
        desired = Mock()
        desired.name = b'unit.tests.'
        changes = []
        changes.append(Create(create_r))
        changes.append(Delete(delete_r))
        changes.append(Update(existing=update_existing_r, new=update_new_r))
        provider.apply(Plan(existing=[
         update_existing_r, delete_r], desired=desired, changes=changes, exists=True))
        calls_mock = gcloud_zone_mock.changes.return_value
        mocked_calls = []
        for mock_call in calls_mock.add_record_set.mock_calls:
            mocked_calls.append(mock_call[1][0])

        self.assertEqual(mocked_calls, [
         DummyResourceRecordSet(b'unit.tests.', b'A', 0, [b'1.2.3.4', b'10.10.10.10']),
         DummyResourceRecordSet(b'aa.unit.tests.', b'A', 666, [b'1.4.3.2'])])
        mocked_calls2 = []
        for mock_call in calls_mock.delete_record_set.mock_calls:
            mocked_calls2.append(mock_call[1][0])

        self.assertEqual(mocked_calls2, [
         DummyResourceRecordSet(b'a.unit.tests.', b'A', 1, [b'1.2.3.4', b'1.1.1.1']),
         DummyResourceRecordSet(b'aa.unit.tests.', b'A', 9001, [b'1.2.4.3'])])
        type(status_mock).status = b'pending'
        with self.assertRaises(RuntimeError):
            provider.apply(Plan(existing=[
             update_existing_r, delete_r], desired=desired, changes=changes, exists=True))
        unsupported_change = Mock()
        unsupported_change.__len__ = Mock(return_value=1)
        type_mock = Mock()
        type_mock._type = b'A'
        unsupported_change.record = type_mock
        mock_plan = Mock()
        type(mock_plan).desired = PropertyMock(return_value=DummyDesired(b'dummy name', []))
        type(mock_plan).changes = [unsupported_change]
        with self.assertRaises(RuntimeError):
            provider.apply(mock_plan)

    def test__get_gcloud_client(self):
        provider = self._get_provider()
        self.assertIsInstance(provider, GoogleCloudProvider)

    @patch(b'octodns.provider.googlecloud.dns')
    def test_populate(self, _):

        def _get_mock_zones(page_token=None):
            if not page_token:
                return DummyIterator([
                 DummyGoogleCloudZone(b'example.com.')], page_token=b'MOCK_PAGE_TOKEN')
            if page_token == b'MOCK_PAGE_TOKEN':
                return DummyIterator([
                 DummyGoogleCloudZone(b'example2.com.')], page_token=b'MOCK_PAGE_TOKEN2')
            return DummyIterator([
             google_cloud_zone])

        def _get_mock_record_sets(page_token=None):
            if not page_token:
                return DummyIterator([ DummyResourceRecordSet(*v) for v in resource_record_sets[:3]
                                     ], page_token=b'MOCK_PAGE_TOKEN')
            if page_token == b'MOCK_PAGE_TOKEN':
                return DummyIterator([ DummyResourceRecordSet(*v) for v in resource_record_sets[3:5]
                                     ], page_token=b'MOCK_PAGE_TOKEN2')
            return DummyIterator([ DummyResourceRecordSet(*v) for v in resource_record_sets[5:] ])

        google_cloud_zone = DummyGoogleCloudZone(b'unit.tests.')
        provider = self._get_provider()
        provider.gcloud_client.list_zones = Mock(side_effect=_get_mock_zones)
        google_cloud_zone.list_resource_record_sets = Mock(side_effect=_get_mock_record_sets)
        self.assertEqual(provider.gcloud_zones.get(b'unit.tests.').dns_name, b'unit.tests.')
        test_zone = Zone(b'unit.tests.', [])
        exists = provider.populate(test_zone)
        self.assertTrue(exists)
        self.assertEqual(test_zone.records, zone.records)
        test_zone2 = Zone(b'nonexistent.zone.', [])
        exists = provider.populate(test_zone2, False, False)
        self.assertFalse(exists)
        self.assertEqual(len(test_zone2.records), 0, msg=b'Zone should not get records from wrong domain')
        provider.SUPPORTS = set()
        test_zone3 = Zone(b'unit.tests.', [])
        provider.populate(test_zone3)
        self.assertEqual(len(test_zone3.records), 0)
        return

    @patch(b'octodns.provider.googlecloud.dns')
    def test_populate_corner_cases(self, _):
        provider = self._get_provider()
        test_zone = Zone(b'unit.tests.', [])
        not_same_fqdn = (
         DummyResourceRecordSet(b'unit.tests.gr', b'A', 0, [b'1.2.3.4']),)
        provider._get_gcloud_records = Mock(side_effect=[
         not_same_fqdn])
        provider._gcloud_zones = {b'unit.tests.': DummyGoogleCloudZone(b'unit.tests.', b'unit-tests')}
        provider.populate(test_zone)
        self.assertEqual(len(test_zone.records), 1)
        self.assertEqual(test_zone.records.pop().fqdn, b'unit.tests.gr.unit.tests.')

    def test__get_gcloud_zone(self):
        provider = self._get_provider()
        provider.gcloud_client = Mock()
        provider.gcloud_client.list_zones = Mock(return_value=DummyIterator([]))
        self.assertIsNone(provider.gcloud_zones.get(b'nonexistent.zone'), msg=b"Check that nonexistent zones return None whenthere's no create=True flag")

    def test__get_rrsets(self):
        provider = self._get_provider()
        dummy_gcloud_zone = DummyGoogleCloudZone(b'unit.tests')
        for octo_record in octo_records:
            _rrset_func = getattr(provider, (b'_rrset_for_{}').format(octo_record._type))
            self.assertEqual(_rrset_func(dummy_gcloud_zone, octo_record).record_type, octo_record._type)

    def test__create_zone(self):
        provider = self._get_provider()
        provider.gcloud_client = Mock()
        provider.gcloud_client.list_zones = Mock(return_value=DummyIterator([]))
        mock_zone = provider._create_gcloud_zone(b'nonexistent.zone.mock')
        mock_zone.create.assert_called()
        provider.gcloud_client.zone.assert_called()

    def test__create_zone_ip6_arpa(self):

        def _create_dummy_zone(name, dns_name):
            return DummyGoogleCloudZone(name=name, dns_name=dns_name)

        provider = self._get_provider()
        provider.gcloud_client = Mock()
        provider.gcloud_client.zone = Mock(side_effect=_create_dummy_zone)
        mock_zone = provider._create_gcloud_zone(b'0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa')
        self.assertRegexpMatches(mock_zone.name, b'^[a-z][a-z0-9-]*[a-z0-9]$')
        self.assertEqual(len(mock_zone.name), 63)

    def test_semicolon_fixup(self):
        provider = self._get_provider()
        self.assertEquals({b'values': [
                     b'abcd\\; ef\\;g', b'hij\\; klm\\;n']}, provider._data_for_TXT(DummyResourceRecordSet(b'unit.tests.', b'TXT', 0, [b'abcd; ef;g', b'hij\\; klm\\;n'])))