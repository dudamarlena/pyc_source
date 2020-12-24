# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_azuredns.py
# Compiled at: 2019-04-08 15:34:11
from __future__ import absolute_import, division, print_function, unicode_literals
from octodns.record import Create, Delete, Record
from octodns.provider.azuredns import _AzureRecord, AzureProvider, _check_endswith_dot, _parse_azure_type
from octodns.zone import Zone
from octodns.provider.base import Plan
from azure.mgmt.dns.models import ARecord, AaaaRecord, CaaRecord, CnameRecord, MxRecord, SrvRecord, NsRecord, PtrRecord, TxtRecord, RecordSet, SoaRecord, Zone as AzureZone
from msrestazure.azure_exceptions import CloudError
from unittest import TestCase
from mock import Mock, patch
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
octo_records.append(Record.new(zone, b'aaaa1', {b'ttl': 300, 
   b'type': b'AAAA', 
   b'values': [
             b'2601:644:500:e210:62f8:1dff:feb8:947a',
             b'2601:642:500:e210:62f8:1dff:feb8:947a']}))
octo_records.append(Record.new(zone, b'aaaa2', {b'ttl': 300, 
   b'type': b'AAAA', 
   b'value': b'2601:644:500:e210:62f8:1dff:feb8:947a'}))
octo_records.append(Record.new(zone, b'caa1', {b'ttl': 9, 
   b'type': b'CAA', 
   b'value': {b'flags': 0, 
              b'tag': b'issue', 
              b'value': b'ca.unit.tests'}}))
octo_records.append(Record.new(zone, b'caa2', {b'ttl': 9, 
   b'type': b'CAA', 
   b'values': [
             {b'flags': 0, 
                b'tag': b'issue', 
                b'value': b'ca1.unit.tests'},
             {b'flags': 0, 
                b'tag': b'issue', 
                b'value': b'ca2.unit.tests'}]}))
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
octo_records.append(Record.new(zone, b'ptr1', {b'ttl': 5, 
   b'type': b'PTR', 
   b'value': b'ptr1.unit.tests.'}))
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
azure_records = []
_base0 = _AzureRecord(b'TestAzure', octo_records[0])
_base0.zone_name = b'unit.tests'
_base0.relative_record_set_name = b'@'
_base0.record_type = b'A'
_base0.params[b'ttl'] = 0
_base0.params[b'arecords'] = [ARecord(ipv4_address=b'1.2.3.4'),
 ARecord(ipv4_address=b'10.10.10.10')]
azure_records.append(_base0)
_base1 = _AzureRecord(b'TestAzure', octo_records[1])
_base1.zone_name = b'unit.tests'
_base1.relative_record_set_name = b'a'
_base1.record_type = b'A'
_base1.params[b'ttl'] = 1
_base1.params[b'arecords'] = [ARecord(ipv4_address=b'1.2.3.4'),
 ARecord(ipv4_address=b'1.1.1.1')]
azure_records.append(_base1)
_base2 = _AzureRecord(b'TestAzure', octo_records[2])
_base2.zone_name = b'unit.tests'
_base2.relative_record_set_name = b'aa'
_base2.record_type = b'A'
_base2.params[b'ttl'] = 9001
_base2.params[b'arecords'] = ARecord(ipv4_address=b'1.2.4.3')
azure_records.append(_base2)
_base3 = _AzureRecord(b'TestAzure', octo_records[3])
_base3.zone_name = b'unit.tests'
_base3.relative_record_set_name = b'aaa'
_base3.record_type = b'A'
_base3.params[b'ttl'] = 2
_base3.params[b'arecords'] = ARecord(ipv4_address=b'1.1.1.3')
azure_records.append(_base3)
_base4 = _AzureRecord(b'TestAzure', octo_records[4])
_base4.zone_name = b'unit.tests'
_base4.relative_record_set_name = b'aaaa1'
_base4.record_type = b'AAAA'
_base4.params[b'ttl'] = 300
aaaa1 = AaaaRecord(ipv6_address=b'2601:644:500:e210:62f8:1dff:feb8:947a')
aaaa2 = AaaaRecord(ipv6_address=b'2601:642:500:e210:62f8:1dff:feb8:947a')
_base4.params[b'aaaa_records'] = [aaaa1, aaaa2]
azure_records.append(_base4)
_base5 = _AzureRecord(b'TestAzure', octo_records[5])
_base5.zone_name = b'unit.tests'
_base5.relative_record_set_name = b'aaaa2'
_base5.record_type = b'AAAA'
_base5.params[b'ttl'] = 300
_base5.params[b'aaaa_records'] = [aaaa1]
azure_records.append(_base5)
_base6 = _AzureRecord(b'TestAzure', octo_records[6])
_base6.zone_name = b'unit.tests'
_base6.relative_record_set_name = b'caa1'
_base6.record_type = b'CAA'
_base6.params[b'ttl'] = 9
_base6.params[b'caa_records'] = [
 CaaRecord(flags=0, tag=b'issue', value=b'ca.unit.tests')]
azure_records.append(_base6)
_base7 = _AzureRecord(b'TestAzure', octo_records[7])
_base7.zone_name = b'unit.tests'
_base7.relative_record_set_name = b'caa2'
_base7.record_type = b'CAA'
_base7.params[b'ttl'] = 9
_base7.params[b'caa_records'] = [
 CaaRecord(flags=0, tag=b'issue', value=b'ca1.unit.tests'),
 CaaRecord(flags=0, tag=b'issue', value=b'ca2.unit.tests')]
azure_records.append(_base7)
_base8 = _AzureRecord(b'TestAzure', octo_records[8])
_base8.zone_name = b'unit.tests'
_base8.relative_record_set_name = b'cname'
_base8.record_type = b'CNAME'
_base8.params[b'ttl'] = 3
_base8.params[b'cname_record'] = CnameRecord(cname=b'a.unit.tests.')
azure_records.append(_base8)
_base9 = _AzureRecord(b'TestAzure', octo_records[9])
_base9.zone_name = b'unit.tests'
_base9.relative_record_set_name = b'mx1'
_base9.record_type = b'MX'
_base9.params[b'ttl'] = 3
_base9.params[b'mx_records'] = [
 MxRecord(preference=10, exchange=b'mx1.unit.tests.'),
 MxRecord(preference=20, exchange=b'mx2.unit.tests.')]
azure_records.append(_base9)
_base10 = _AzureRecord(b'TestAzure', octo_records[10])
_base10.zone_name = b'unit.tests'
_base10.relative_record_set_name = b'mx2'
_base10.record_type = b'MX'
_base10.params[b'ttl'] = 3
_base10.params[b'mx_records'] = [
 MxRecord(preference=10, exchange=b'mx1.unit.tests.')]
azure_records.append(_base10)
_base11 = _AzureRecord(b'TestAzure', octo_records[11])
_base11.zone_name = b'unit.tests'
_base11.relative_record_set_name = b'@'
_base11.record_type = b'NS'
_base11.params[b'ttl'] = 4
_base11.params[b'ns_records'] = [NsRecord(nsdname=b'ns1.unit.tests.'),
 NsRecord(nsdname=b'ns2.unit.tests.')]
azure_records.append(_base11)
_base12 = _AzureRecord(b'TestAzure', octo_records[12])
_base12.zone_name = b'unit.tests'
_base12.relative_record_set_name = b'foo'
_base12.record_type = b'NS'
_base12.params[b'ttl'] = 5
_base12.params[b'ns_records'] = [NsRecord(nsdname=b'ns1.unit.tests.')]
azure_records.append(_base12)
_base13 = _AzureRecord(b'TestAzure', octo_records[13])
_base13.zone_name = b'unit.tests'
_base13.relative_record_set_name = b'ptr1'
_base13.record_type = b'PTR'
_base13.params[b'ttl'] = 5
_base13.params[b'ptr_records'] = [PtrRecord(ptrdname=b'ptr1.unit.tests.')]
azure_records.append(_base13)
_base14 = _AzureRecord(b'TestAzure', octo_records[14])
_base14.zone_name = b'unit.tests'
_base14.relative_record_set_name = b'_srv._tcp'
_base14.record_type = b'SRV'
_base14.params[b'ttl'] = 6
_base14.params[b'srv_records'] = [
 SrvRecord(priority=10, weight=20, port=30, target=b'foo-1.unit.tests.'),
 SrvRecord(priority=12, weight=30, port=30, target=b'foo-2.unit.tests.')]
azure_records.append(_base14)
_base15 = _AzureRecord(b'TestAzure', octo_records[15])
_base15.zone_name = b'unit.tests'
_base15.relative_record_set_name = b'_srv2._tcp'
_base15.record_type = b'SRV'
_base15.params[b'ttl'] = 7
_base15.params[b'srv_records'] = [
 SrvRecord(priority=12, weight=17, port=1, target=b'srvfoo.unit.tests.')]
azure_records.append(_base15)
_base16 = _AzureRecord(b'TestAzure', octo_records[16])
_base16.zone_name = b'unit.tests'
_base16.relative_record_set_name = b'txt1'
_base16.record_type = b'TXT'
_base16.params[b'ttl'] = 8
_base16.params[b'txt_records'] = [TxtRecord(value=[b'txt singleton test'])]
azure_records.append(_base16)
_base17 = _AzureRecord(b'TestAzure', octo_records[17])
_base17.zone_name = b'unit.tests'
_base17.relative_record_set_name = b'txt2'
_base17.record_type = b'TXT'
_base17.params[b'ttl'] = 9
_base17.params[b'txt_records'] = [TxtRecord(value=[b'txt multiple test']),
 TxtRecord(value=[b'txt multiple test 2'])]
azure_records.append(_base17)

class Test_AzureRecord(TestCase):

    def test_azure_record(self):
        assert len(azure_records) == len(octo_records)
        for i in range(len(azure_records)):
            octo = _AzureRecord(b'TestAzure', octo_records[i])
            assert azure_records[i]._equals(octo)


class Test_ParseAzureType(TestCase):

    def test_parse_azure_type(self):
        for expected, test in [[b'A', b'Microsoft.Network/dnszones/A'],
         [
          b'AAAA', b'Microsoft.Network/dnszones/AAAA'],
         [
          b'NS', b'Microsoft.Network/dnszones/NS'],
         [
          b'MX', b'Microsoft.Network/dnszones/MX']]:
            self.assertEquals(expected, _parse_azure_type(test))


class Test_CheckEndswithDot(TestCase):

    def test_check_endswith_dot(self):
        for expected, test in [[b'a.', b'a'],
         [
          b'a.', b'a.'],
         [
          b'foo.bar.', b'foo.bar.'],
         [
          b'foo.bar.', b'foo.bar']]:
            self.assertEquals(expected, _check_endswith_dot(test))


class TestAzureDnsProvider(TestCase):

    def _provider(self):
        return self._get_provider(b'mock_spc', b'mock_dns_client')

    @patch(b'octodns.provider.azuredns.DnsManagementClient')
    @patch(b'octodns.provider.azuredns.ServicePrincipalCredentials')
    def _get_provider(self, mock_spc, mock_dns_client):
        """Returns a mock AzureProvider object to use in testing.

            :param mock_spc: placeholder
            :type  mock_spc: str
            :param mock_dns_client: placeholder
            :type  mock_dns_client: str

            :type return: AzureProvider
        """
        return AzureProvider(b'mock_id', b'mock_client', b'mock_key', b'mock_directory', b'mock_sub', b'mock_rg')

    def test_populate_records(self):
        provider = self._get_provider()
        rs = []
        recordSet = RecordSet(arecords=[ARecord(ipv4_address=b'1.1.1.1')])
        recordSet.name, recordSet.ttl, recordSet.type = ('a1', 0, 'A')
        rs.append(recordSet)
        recordSet = RecordSet(arecords=[ARecord(ipv4_address=b'1.1.1.1'),
         ARecord(ipv4_address=b'2.2.2.2')])
        recordSet.name, recordSet.ttl, recordSet.type = ('a2', 1, 'A')
        rs.append(recordSet)
        aaaa1 = AaaaRecord(ipv6_address=b'1:1ec:1::1')
        recordSet = RecordSet(aaaa_records=[aaaa1])
        recordSet.name, recordSet.ttl, recordSet.type = ('aaaa1', 2, 'AAAA')
        rs.append(recordSet)
        aaaa2 = AaaaRecord(ipv6_address=b'1:1ec:1::2')
        recordSet = RecordSet(aaaa_records=[aaaa1,
         aaaa2])
        recordSet.name, recordSet.ttl, recordSet.type = ('aaaa2', 3, 'AAAA')
        rs.append(recordSet)
        recordSet = RecordSet(caa_records=[
         CaaRecord(flags=0, tag=b'issue', value=b'caa1.unit.tests')])
        recordSet.name, recordSet.ttl, recordSet.type = ('caa1', 4, 'CAA')
        rs.append(recordSet)
        recordSet = RecordSet(caa_records=[
         CaaRecord(flags=0, tag=b'issue', value=b'caa1.unit.tests'),
         CaaRecord(flags=0, tag=b'issue', value=b'caa2.unit.tests')])
        recordSet.name, recordSet.ttl, recordSet.type = ('caa2', 4, 'CAA')
        rs.append(recordSet)
        cname1 = CnameRecord(cname=b'cname.unit.test.')
        recordSet = RecordSet(cname_record=cname1)
        recordSet.name, recordSet.ttl, recordSet.type = ('cname1', 5, 'CNAME')
        rs.append(recordSet)
        recordSet = RecordSet(cname_record=None)
        recordSet.name, recordSet.ttl, recordSet.type = ('cname2', 6, 'CNAME')
        rs.append(recordSet)
        recordSet = RecordSet(mx_records=[
         MxRecord(preference=10, exchange=b'mx1.unit.test.')])
        recordSet.name, recordSet.ttl, recordSet.type = ('mx1', 7, 'MX')
        rs.append(recordSet)
        recordSet = RecordSet(mx_records=[
         MxRecord(preference=10, exchange=b'mx1.unit.test.'),
         MxRecord(preference=11, exchange=b'mx2.unit.test.')])
        recordSet.name, recordSet.ttl, recordSet.type = ('mx2', 8, 'MX')
        rs.append(recordSet)
        recordSet = RecordSet(ns_records=[NsRecord(nsdname=b'ns1.unit.test.')])
        recordSet.name, recordSet.ttl, recordSet.type = ('ns1', 9, 'NS')
        rs.append(recordSet)
        recordSet = RecordSet(ns_records=[NsRecord(nsdname=b'ns1.unit.test.'),
         NsRecord(nsdname=b'ns2.unit.test.')])
        recordSet.name, recordSet.ttl, recordSet.type = ('ns2', 10, 'NS')
        rs.append(recordSet)
        ptr1 = PtrRecord(ptrdname=b'ptr1.unit.test.')
        recordSet = RecordSet(ptr_records=[ptr1])
        recordSet.name, recordSet.ttl, recordSet.type = ('ptr1', 11, 'PTR')
        rs.append(recordSet)
        recordSet = RecordSet(ptr_records=[PtrRecord(ptrdname=None)])
        recordSet.name, recordSet.ttl, recordSet.type = ('ptr2', 12, 'PTR')
        rs.append(recordSet)
        recordSet = RecordSet(srv_records=[
         SrvRecord(priority=1, weight=2, port=3, target=b'1unit.tests.')])
        recordSet.name, recordSet.ttl, recordSet.type = ('_srv1._tcp', 13, 'SRV')
        rs.append(recordSet)
        recordSet = RecordSet(srv_records=[
         SrvRecord(priority=1, weight=2, port=3, target=b'1unit.tests.'),
         SrvRecord(priority=4, weight=5, port=6, target=b'2unit.tests.')])
        recordSet.name, recordSet.ttl, recordSet.type = ('_srv2._tcp', 14, 'SRV')
        rs.append(recordSet)
        recordSet = RecordSet(txt_records=[TxtRecord(value=b'sample text1')])
        recordSet.name, recordSet.ttl, recordSet.type = ('txt1', 15, 'TXT')
        rs.append(recordSet)
        recordSet = RecordSet(txt_records=[TxtRecord(value=b'sample text1'),
         TxtRecord(value=b'sample text2')])
        recordSet.name, recordSet.ttl, recordSet.type = ('txt2', 16, 'TXT')
        rs.append(recordSet)
        recordSet = RecordSet(soa_record=[SoaRecord()])
        recordSet.name, recordSet.ttl, recordSet.type = ('', 17, 'SOA')
        rs.append(recordSet)
        record_list = provider._dns_client.record_sets.list_by_dns_zone
        record_list.return_value = rs
        exists = provider.populate(zone)
        self.assertTrue(exists)
        self.assertEquals(len(zone.records), 18)
        return

    def test_populate_zone(self):
        provider = self._get_provider()
        zone_list = provider._dns_client.zones.list_by_resource_group
        zone_list.return_value = [AzureZone(location=b'global'),
         AzureZone(location=b'global')]
        provider._populate_zones()
        self.assertEquals(len(provider._azure_zones), 1)

    def test_bad_zone_response(self):
        provider = self._get_provider()
        _get = provider._dns_client.zones.get
        _get.side_effect = CloudError(Mock(status=404), b'Azure Error')
        trip = False
        try:
            provider._check_zone(b'unit.test', create=False)
        except CloudError:
            trip = True

        self.assertEquals(trip, True)

    def test_apply(self):
        provider = self._get_provider()
        changes = []
        deletes = []
        for i in octo_records:
            changes.append(Create(i))
            deletes.append(Delete(i))

        self.assertEquals(18, provider.apply(Plan(None, zone, changes, True)))
        self.assertEquals(18, provider.apply(Plan(zone, zone, deletes, True)))
        return

    def test_create_zone(self):
        provider = self._get_provider()
        changes = []
        for i in octo_records:
            changes.append(Create(i))

        desired = Zone(b'unit2.test.', [])
        err_msg = b"The Resource 'Microsoft.Network/dnszones/unit2.test' "
        err_msg += b"under resource group 'mock_rg' was not found."
        _get = provider._dns_client.zones.get
        _get.side_effect = CloudError(Mock(status=404), err_msg)
        self.assertEquals(18, provider.apply(Plan(None, desired, changes, True)))
        return

    def test_check_zone_no_create(self):
        provider = self._get_provider()
        rs = []
        recordSet = RecordSet(arecords=[ARecord(ipv4_address=b'1.1.1.1')])
        recordSet.name, recordSet.ttl, recordSet.type = ('a1', 0, 'A')
        rs.append(recordSet)
        recordSet = RecordSet(arecords=[ARecord(ipv4_address=b'1.1.1.1'),
         ARecord(ipv4_address=b'2.2.2.2')])
        recordSet.name, recordSet.ttl, recordSet.type = ('a2', 1, 'A')
        rs.append(recordSet)
        record_list = provider._dns_client.record_sets.list_by_dns_zone
        record_list.return_value = rs
        err_msg = b"The Resource 'Microsoft.Network/dnszones/unit3.test' "
        err_msg += b"under resource group 'mock_rg' was not found."
        _get = provider._dns_client.zones.get
        _get.side_effect = CloudError(Mock(status=404), err_msg)
        exists = provider.populate(Zone(b'unit3.test.', []))
        self.assertFalse(exists)
        self.assertEquals(len(zone.records), 0)