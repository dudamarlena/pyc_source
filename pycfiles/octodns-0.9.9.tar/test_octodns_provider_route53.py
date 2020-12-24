# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_route53.py
# Compiled at: 2019-10-18 13:06:59
from __future__ import absolute_import, division, print_function, unicode_literals
from botocore.exceptions import ClientError
from botocore.stub import ANY, Stubber
from six import text_type
from unittest import TestCase
from mock import patch
from octodns.record import Create, Delete, Record, Update
from octodns.provider.route53 import Route53Provider, _Route53GeoDefault, _Route53DynamicValue, _Route53GeoRecord, _Route53Record, _mod_keyer, _octal_replace
from octodns.zone import Zone
from helpers import GeoProvider

class DummyR53Record(object):

    def __init__(self, health_check_id):
        self.health_check_id = health_check_id


class TestOctalReplace(TestCase):

    def test_basic(self):
        for expected, s in (
         ('', ''),
         ('abc', 'abc'),
         ('123', '123'),
         ('abc123', 'abc123'),
         ('*', '\\052'),
         ('abc*', 'abc\\052'),
         ('*abc', '\\052abc'),
         ('123*', '123\\052'),
         ('*123', '\\052123'),
         ('**', '\\052\\052')):
            self.assertEquals(expected, _octal_replace(s))


dynamic_rrsets = [
 {b'Name': b'_octodns-default-pool.unit.tests.', 
    b'ResourceRecords': [{b'Value': b'1.1.2.1'}, {b'Value': b'1.1.2.2'}], b'TTL': 60, 
    b'Type': b'A'},
 {b'HealthCheckId': b'76', 
    b'Name': b'_octodns-ap-southeast-1-value.unit.tests.', 
    b'ResourceRecords': [{b'Value': b'1.4.1.1'}], b'SetIdentifier': b'ap-southeast-1-000', 
    b'TTL': 60, 
    b'Type': b'A', 
    b'Weight': 2},
 {b'HealthCheckId': b'09', 
    b'Name': b'_octodns-ap-southeast-1-value.unit.tests.', 
    b'ResourceRecords': [{b'Value': b'1.4.1.2'}], b'SetIdentifier': b'ap-southeast-1-001', 
    b'TTL': 60, 
    b'Type': b'A', 
    b'Weight': 2},
 {b'HealthCheckId': b'ab', 
    b'Name': b'_octodns-eu-central-1-value.unit.tests.', 
    b'ResourceRecords': [{b'Value': b'1.3.1.1'}], b'SetIdentifier': b'eu-central-1-000', 
    b'TTL': 60, 
    b'Type': b'A', 
    b'Weight': 1},
 {b'HealthCheckId': b'1e', 
    b'Name': b'_octodns-eu-central-1-value.unit.tests.', 
    b'ResourceRecords': [{b'Value': b'1.3.1.2'}], b'SetIdentifier': b'eu-central-1-001', 
    b'TTL': 60, 
    b'Type': b'A', 
    b'Weight': 1},
 {b'HealthCheckId': b'2a', 
    b'Name': b'_octodns-us-east-1-value.unit.tests.', 
    b'ResourceRecords': [{b'Value': b'1.5.1.1'}], b'SetIdentifier': b'us-east-1-000', 
    b'TTL': 60, 
    b'Type': b'A', 
    b'Weight': 1},
 {b'HealthCheckId': b'61', 
    b'Name': b'_octodns-us-east-1-value.unit.tests.', 
    b'ResourceRecords': [{b'Value': b'1.5.1.2'}], b'SetIdentifier': b'us-east-1-001', 
    b'TTL': 60, 
    b'Type': b'A', 
    b'Weight': 1},
 {b'AliasTarget': {b'DNSName': b'_octodns-default-pool.unit.tests.', b'EvaluateTargetHealth': True, 
                     b'HostedZoneId': b'Z2'}, 
    b'Failover': b'SECONDARY', 
    b'Name': b'_octodns-us-east-1-pool.unit.tests.', 
    b'SetIdentifier': b'us-east-1-Secondary-default', 
    b'Type': b'A'},
 {b'AliasTarget': {b'DNSName': b'_octodns-us-east-1-value.unit.tests.', 
                     b'EvaluateTargetHealth': True, 
                     b'HostedZoneId': b'Z2'}, 
    b'Failover': b'PRIMARY', 
    b'Name': b'_octodns-us-east-1-pool.unit.tests.', 
    b'SetIdentifier': b'us-east-1-Primary', 
    b'Type': b'A'},
 {b'AliasTarget': {b'DNSName': b'_octodns-us-east-1-pool.unit.tests.', b'EvaluateTargetHealth': True, 
                     b'HostedZoneId': b'Z2'}, 
    b'Failover': b'SECONDARY', 
    b'Name': b'_octodns-eu-central-1-pool.unit.tests.', 
    b'SetIdentifier': b'eu-central-1-Secondary-default', 
    b'Type': b'A'},
 {b'AliasTarget': {b'DNSName': b'_octodns-eu-central-1-value.unit.tests.', 
                     b'EvaluateTargetHealth': True, 
                     b'HostedZoneId': b'Z2'}, 
    b'Failover': b'PRIMARY', 
    b'Name': b'_octodns-eu-central-1-pool.unit.tests.', 
    b'SetIdentifier': b'eu-central-1-Primary', 
    b'Type': b'A'},
 {b'AliasTarget': {b'DNSName': b'_octodns-us-east-1-pool.unit.tests.', b'EvaluateTargetHealth': True, 
                     b'HostedZoneId': b'Z2'}, 
    b'Failover': b'SECONDARY', 
    b'Name': b'_octodns-ap-southeast-1-pool.unit.tests.', 
    b'SetIdentifier': b'ap-southeast-1-Secondary-default', 
    b'Type': b'A'},
 {b'AliasTarget': {b'DNSName': b'_octodns-ap-southeast-1-value.unit.tests.', 
                     b'EvaluateTargetHealth': True, 
                     b'HostedZoneId': b'Z2'}, 
    b'Failover': b'PRIMARY', 
    b'Name': b'_octodns-ap-southeast-1-pool.unit.tests.', 
    b'SetIdentifier': b'ap-southeast-1-Primary', 
    b'Type': b'A'},
 {b'AliasTarget': {b'DNSName': b'_octodns-ap-southeast-1-pool.unit.tests.', b'EvaluateTargetHealth': True, 
                     b'HostedZoneId': b'Z2'}, 
    b'GeoLocation': {b'CountryCode': b'JP'}, b'Name': b'unit.tests.', 
    b'SetIdentifier': b'1-ap-southeast-1-AS-JP', 
    b'Type': b'A'},
 {b'AliasTarget': {b'DNSName': b'_octodns-ap-southeast-1-pool.unit.tests.', b'EvaluateTargetHealth': True, 
                     b'HostedZoneId': b'Z2'}, 
    b'GeoLocation': {b'CountryCode': b'CN'}, b'Name': b'unit.tests.', 
    b'SetIdentifier': b'1-ap-southeast-1-AS-CN', 
    b'Type': b'A'},
 {b'AliasTarget': {b'DNSName': b'_octodns-eu-central-1-pool.unit.tests.', b'EvaluateTargetHealth': True, 
                     b'HostedZoneId': b'Z2'}, 
    b'GeoLocation': {b'ContinentCode': b'NA-US-FL'}, b'Name': b'unit.tests.', 
    b'SetIdentifier': b'2-eu-central-1-NA-US-FL', 
    b'Type': b'A'},
 {b'AliasTarget': {b'DNSName': b'_octodns-eu-central-1-pool.unit.tests.', b'EvaluateTargetHealth': True, 
                     b'HostedZoneId': b'Z2'}, 
    b'GeoLocation': {b'ContinentCode': b'EU'}, b'Name': b'unit.tests.', 
    b'SetIdentifier': b'2-eu-central-1-EU', 
    b'Type': b'A'},
 {b'AliasTarget': {b'DNSName': b'_octodns-us-east-1-pool.unit.tests.', b'EvaluateTargetHealth': True, 
                     b'HostedZoneId': b'Z2'}, 
    b'GeoLocation': {b'CountryCode': b'*'}, b'Name': b'unit.tests.', 
    b'SetIdentifier': b'3-us-east-1-None', 
    b'Type': b'A'}]
dynamic_record_data = {b'dynamic': {b'pools': {b'ap-southeast-1': {b'fallback': b'us-east-1', 
                                               b'values': [
                                                         {b'weight': 2, 
                                                            b'value': b'1.4.1.1'},
                                                         {b'weight': 2, 
                                                            b'value': b'1.4.1.2'}]}, 
                           b'eu-central-1': {b'fallback': b'us-east-1', 
                                             b'values': [
                                                       {b'weight': 1, 
                                                          b'value': b'1.3.1.1'},
                                                       {b'weight': 1, 
                                                          b'value': b'1.3.1.2'}]}, 
                           b'us-east-1': {b'values': [
                                                    {b'weight': 1, 
                                                       b'value': b'1.5.1.1'},
                                                    {b'weight': 1, 
                                                       b'value': b'1.5.1.2'}]}}, 
                b'rules': [
                         {b'geos': [
                                    b'AS-CN', b'AS-JP'], 
                            b'pool': b'ap-southeast-1'},
                         {b'geos': [
                                    b'EU', b'NA-US-FL'], 
                            b'pool': b'eu-central-1'},
                         {b'pool': b'us-east-1'}]}, 
   b'ttl': 60, 
   b'type': b'A', 
   b'values': [
             b'1.1.2.1',
             b'1.1.2.2']}

class TestRoute53Provider(TestCase):
    expected = Zone(b'unit.tests.', [])
    for name, data in (
     (
      b'simple', {b'ttl': 60, b'type': b'A', b'values': [b'1.2.3.4', b'2.2.3.4']}),
     (
      b'',
      {b'ttl': 61, b'type': b'A', b'values': [b'2.2.3.4', b'3.2.3.4'], b'geo': {b'AF': [
                        b'4.2.3.4'], 
                  b'NA-US': [
                           b'5.2.3.4', b'6.2.3.4'], 
                  b'NA-US-CA': [
                              b'7.2.3.4']}}),
     (
      b'cname', {b'ttl': 62, b'type': b'CNAME', b'value': b'unit.tests.'}),
     (
      b'txt',
      {b'ttl': 63, b'type': b'TXT', b'values': [b'Hello World!',
                   b'Goodbye World?']}),
     (
      b'',
      {b'ttl': 64, b'type': b'MX', b'values': [
                   {b'preference': 10, 
                      b'exchange': b'smtp-1.unit.tests.'},
                   {b'preference': 20, 
                      b'exchange': b'smtp-2.unit.tests.'}]}),
     (
      b'naptr',
      {b'ttl': 65, b'type': b'NAPTR', b'value': {b'order': 10, 
                    b'preference': 20, 
                    b'flags': b'U', 
                    b'service': b'SIP+D2U', 
                    b'regexp': b'!^.*$!sip:info@bar.example.com!', 
                    b'replacement': b'.'}}),
     (
      b'_srv._tcp',
      {b'ttl': 66, b'type': b'SRV', b'value': {b'priority': 10, 
                    b'weight': 20, 
                    b'port': 30, 
                    b'target': b'cname.unit.tests.'}}),
     (
      b'', {b'ttl': 67, b'type': b'NS', b'values': [b'8.2.3.4.', b'9.2.3.4.']}),
     (
      b'sub', {b'ttl': 68, b'type': b'NS', b'values': [b'5.2.3.4.', b'6.2.3.4.']}),
     (
      b'',
      {b'ttl': 69, b'type': b'CAA', b'value': {b'flags': 0, 
                    b'tag': b'issue', 
                    b'value': b'ca.unit.tests'}})):
        record = Record.new(expected, name, data)
        expected.add_record(record)

    caller_ref = (b'{}:A:unit.tests.:1324').format(Route53Provider.HEALTH_CHECK_VERSION)
    health_checks = [
     {b'Id': b'42', 
        b'CallerReference': caller_ref, 
        b'HealthCheckConfig': {b'Type': b'HTTPS', 
                               b'FullyQualifiedDomainName': b'unit.tests', 
                               b'IPAddress': b'4.2.3.4', 
                               b'ResourcePath': b'/_dns', 
                               b'Type': b'HTTPS', 
                               b'Port': 443, 
                               b'MeasureLatency': True}, 
        b'HealthCheckVersion': 2},
     {b'Id': b'ignored-also', 
        b'CallerReference': b'something-else', 
        b'HealthCheckConfig': {b'Type': b'HTTPS', 
                               b'FullyQualifiedDomainName': b'unit.tests', 
                               b'IPAddress': b'5.2.3.4', 
                               b'ResourcePath': b'/_dns', 
                               b'Type': b'HTTPS', 
                               b'Port': 443, 
                               b'MeasureLatency': True}, 
        b'HealthCheckVersion': 42},
     {b'Id': b'43', 
        b'CallerReference': caller_ref, 
        b'HealthCheckConfig': {b'Type': b'HTTPS', 
                               b'FullyQualifiedDomainName': b'unit.tests', 
                               b'IPAddress': b'5.2.3.4', 
                               b'ResourcePath': b'/_dns', 
                               b'Type': b'HTTPS', 
                               b'Port': 443, 
                               b'MeasureLatency': True}, 
        b'HealthCheckVersion': 2},
     {b'Id': b'44', 
        b'CallerReference': caller_ref, 
        b'HealthCheckConfig': {b'Type': b'HTTPS', 
                               b'FullyQualifiedDomainName': b'unit.tests', 
                               b'IPAddress': b'7.2.3.4', 
                               b'ResourcePath': b'/_dns', 
                               b'Type': b'HTTPS', 
                               b'Port': 443, 
                               b'MeasureLatency': True}, 
        b'HealthCheckVersion': 2},
     {b'Id': b'45', 
        b'CallerReference': caller_ref.replace(b':A:', b':AAAA:'), 
        b'HealthCheckConfig': {b'Type': b'HTTPS', 
                               b'FullyQualifiedDomainName': b'unit.tests', 
                               b'IPAddress': b'7.2.3.4', 
                               b'ResourcePath': b'/_dns', 
                               b'Type': b'HTTPS', 
                               b'Port': 443, 
                               b'MeasureLatency': True}, 
        b'HealthCheckVersion': 2}]

    def _get_stubbed_provider(self):
        provider = Route53Provider(b'test', b'abc', b'123')
        stubber = Stubber(provider._conn)
        stubber.activate()
        return (
         provider, stubber)

    def _get_stubbed_fallback_auth_provider(self):
        provider = Route53Provider(b'test')
        stubber = Stubber(provider._conn)
        stubber.activate()
        return (
         provider, stubber)

    def test_populate_with_fallback(self):
        provider, stubber = self._get_stubbed_fallback_auth_provider()
        got = Zone(b'unit.tests.', [])
        with self.assertRaises(ClientError):
            stubber.add_client_error(b'list_hosted_zones')
            provider.populate(got)

    def test_populate(self):
        provider, stubber = self._get_stubbed_provider()
        got = Zone(b'unit.tests.', [])
        with self.assertRaises(ClientError):
            stubber.add_client_error(b'list_hosted_zones')
            provider.populate(got)
        with self.assertRaises(ClientError):
            list_hosted_zones_resp = {b'HostedZones': [
                              {b'Name': b'unit.tests.', 
                                 b'Id': b'z42', 
                                 b'CallerReference': b'abc'}], 
               b'Marker': b'm', 
               b'IsTruncated': False, 
               b'MaxItems': b'100'}
            stubber.add_response(b'list_hosted_zones', list_hosted_zones_resp, {})
            stubber.add_client_error(b'list_resource_record_sets', expected_params={b'HostedZoneId': b'z42'})
            provider.populate(got)
            stubber.assert_no_pending_responses()
        list_resource_record_sets_resp_p1 = {b'ResourceRecordSets': [
                                 {b'Name': b'simple.unit.tests.', 
                                    b'Type': b'A', 
                                    b'ResourceRecords': [
                                                       {b'Value': b'1.2.3.4'},
                                                       {b'Value': b'2.2.3.4'}], 
                                    b'TTL': 60},
                                 {b'Name': b'unit.tests.', 
                                    b'Type': b'A', 
                                    b'GeoLocation': {b'CountryCode': b'*'}, 
                                    b'ResourceRecords': [
                                                       {b'Value': b'2.2.3.4'},
                                                       {b'Value': b'3.2.3.4'}], 
                                    b'TTL': 61},
                                 {b'Name': b'unit.tests.', 
                                    b'Type': b'A', 
                                    b'GeoLocation': {b'ContinentCode': b'AF'}, 
                                    b'ResourceRecords': [
                                                       {b'Value': b'4.2.3.4'}], 
                                    b'TTL': 61},
                                 {b'Name': b'unit.tests.', 
                                    b'Type': b'A', 
                                    b'GeoLocation': {b'CountryCode': b'US'}, 
                                    b'ResourceRecords': [
                                                       {b'Value': b'5.2.3.4'},
                                                       {b'Value': b'6.2.3.4'}], 
                                    b'TTL': 61},
                                 {b'Name': b'unit.tests.', 
                                    b'Type': b'A', 
                                    b'GeoLocation': {b'CountryCode': b'US', 
                                                     b'SubdivisionCode': b'CA'}, 
                                    b'ResourceRecords': [
                                                       {b'Value': b'7.2.3.4'}], 
                                    b'TTL': 61}], 
           b'IsTruncated': True, 
           b'NextRecordName': b'next_name', 
           b'NextRecordType': b'next_type', 
           b'MaxItems': b'100'}
        stubber.add_response(b'list_resource_record_sets', list_resource_record_sets_resp_p1, {b'HostedZoneId': b'z42'})
        list_resource_record_sets_resp_p2 = {b'ResourceRecordSets': [
                                 {b'Name': b'cname.unit.tests.', 
                                    b'Type': b'CNAME', 
                                    b'ResourceRecords': [
                                                       {b'Value': b'unit.tests.'}], 
                                    b'TTL': 62},
                                 {b'Name': b'txt.unit.tests.', 
                                    b'Type': b'TXT', 
                                    b'ResourceRecords': [
                                                       {b'Value': b'"Hello World!"'},
                                                       {b'Value': b'"Goodbye World?"'}], 
                                    b'TTL': 63},
                                 {b'Name': b'unit.tests.', 
                                    b'Type': b'MX', 
                                    b'ResourceRecords': [
                                                       {b'Value': b'10 smtp-1.unit.tests.'},
                                                       {b'Value': b'20  smtp-2.unit.tests.'}], 
                                    b'TTL': 64},
                                 {b'Name': b'naptr.unit.tests.', 
                                    b'Type': b'NAPTR', 
                                    b'ResourceRecords': [
                                                       {b'Value': b'10 20 "U" "SIP+D2U" "!^.*$!sip:info@bar.example.com!" .'}], 
                                    b'TTL': 65},
                                 {b'Name': b'_srv._tcp.unit.tests.', 
                                    b'Type': b'SRV', 
                                    b'ResourceRecords': [
                                                       {b'Value': b'10 20 30 cname.unit.tests.'}], 
                                    b'TTL': 66},
                                 {b'Name': b'unit.tests.', 
                                    b'Type': b'NS', 
                                    b'ResourceRecords': [
                                                       {b'Value': b'ns1.unit.tests.'}], 
                                    b'TTL': 67},
                                 {b'Name': b'sub.unit.tests.', 
                                    b'Type': b'NS', 
                                    b'GeoLocation': {b'ContinentCode': b'AF'}, 
                                    b'ResourceRecords': [
                                                       {b'Value': b'5.2.3.4.'},
                                                       {b'Value': b'6.2.3.4.'}], 
                                    b'TTL': 68},
                                 {b'Name': b'soa.unit.tests.', 
                                    b'Type': b'SOA', 
                                    b'ResourceRecords': [
                                                       {b'Value': b'ns1.unit.tests.'}], 
                                    b'TTL': 69},
                                 {b'Name': b'unit.tests.', 
                                    b'Type': b'CAA', 
                                    b'ResourceRecords': [
                                                       {b'Value': b'0 issue "ca.unit.tests"'}], 
                                    b'TTL': 69},
                                 {b'AliasTarget': {b'HostedZoneId': b'Z119WBBTVP5WFX', 
                                                     b'EvaluateTargetHealth': False, 
                                                     b'DNSName': b'unit.tests.'}, 
                                    b'Type': b'A', 
                                    b'Name': b'alias.unit.tests.'}], 
           b'IsTruncated': False, 
           b'MaxItems': b'100'}
        stubber.add_response(b'list_resource_record_sets', list_resource_record_sets_resp_p2, {b'HostedZoneId': b'z42', b'StartRecordName': b'next_name', 
           b'StartRecordType': b'next_type'})
        provider.populate(got)
        changes = self.expected.changes(got, GeoProvider())
        self.assertEquals(0, len(changes))
        stubber.assert_no_pending_responses()
        nonexistent = Zone(b'does.not.exist.', [])
        provider.populate(nonexistent)
        self.assertEquals(set(), nonexistent.records)

    def test_sync(self):
        provider, stubber = self._get_stubbed_provider()
        list_hosted_zones_resp = {b'HostedZones': [
                          {b'Name': b'unit.tests.', 
                             b'Id': b'z42', 
                             b'CallerReference': b'abc'}], 
           b'Marker': b'm', 
           b'IsTruncated': False, 
           b'MaxItems': b'100'}
        stubber.add_response(b'list_hosted_zones', list_hosted_zones_resp, {})
        list_resource_record_sets_resp = {b'ResourceRecordSets': [], b'IsTruncated': False, 
           b'MaxItems': b'100'}
        stubber.add_response(b'list_resource_record_sets', list_resource_record_sets_resp, {b'HostedZoneId': b'z42'})
        plan = provider.plan(self.expected)
        self.assertEquals(9, len(plan.changes))
        self.assertTrue(plan.exists)
        for change in plan.changes:
            self.assertIsInstance(change, Create)

        stubber.assert_no_pending_responses()
        stubber.add_response(b'list_health_checks', {b'HealthChecks': self.health_checks, 
           b'IsTruncated': False, 
           b'MaxItems': b'100', 
           b'Marker': b''})
        stubber.add_response(b'change_resource_record_sets', {b'ChangeInfo': {b'Id': b'id', 
                           b'Status': b'PENDING', 
                           b'SubmittedAt': b'2017-01-29T01:02:03Z'}}, {b'HostedZoneId': b'z42', b'ChangeBatch': ANY})
        self.assertEquals(9, provider.apply(plan))
        stubber.assert_no_pending_responses()

        def add_extra_populate(existing, target, lenient):
            for record in self.expected.records:
                existing.add_record(record)

            record = Record.new(existing, b'extra', {b'ttl': 99, b'type': b'A', b'values': [
                         b'9.9.9.9']})
            existing.add_record(record)

        provider.populate = add_extra_populate
        change_resource_record_sets_params = {b'ChangeBatch': {b'Changes': [
                                       {b'Action': b'DELETE', 
                                          b'ResourceRecordSet': {b'Name': b'extra.unit.tests.', 
                                                                 b'ResourceRecords': [{b'Value': b'9.9.9.9'}], b'TTL': 99, 
                                                                 b'Type': b'A'}}], 
                            b'Comment': ANY}, 
           b'HostedZoneId': b'z42'}
        stubber.add_response(b'change_resource_record_sets', {b'ChangeInfo': {b'Id': b'id', 
                           b'Status': b'PENDING', 
                           b'SubmittedAt': b'2017-01-29T01:02:03Z'}}, change_resource_record_sets_params)
        plan = provider.plan(self.expected)
        self.assertEquals(1, len(plan.changes))
        self.assertIsInstance(plan.changes[0], Delete)
        self.assertEquals(1, provider.apply(plan))
        stubber.assert_no_pending_responses()

        def mod_geo_populate(existing, target, lenient):
            for record in self.expected.records:
                if record._type != b'A' or not record.geo:
                    existing.add_record(record)

            record = Record.new(existing, b'', {b'ttl': 61, 
               b'type': b'A', 
               b'values': [
                         b'8.2.3.4', b'3.2.3.4'], 
               b'geo': {b'AF': [
                              b'4.2.3.4'], 
                        b'NA-US': [
                                 b'5.2.3.4', b'6.2.3.4'], 
                        b'NA-US-KY': [
                                    b'7.2.3.4']}})
            existing.add_record(record)

        provider.populate = mod_geo_populate
        change_resource_record_sets_params = {b'ChangeBatch': {b'Changes': [
                                       {b'Action': b'DELETE', 
                                          b'ResourceRecordSet': {b'GeoLocation': {b'CountryCode': b'US', b'SubdivisionCode': b'KY'}, 
                                                                 b'HealthCheckId': b'44', 
                                                                 b'Name': b'unit.tests.', 
                                                                 b'ResourceRecords': [{b'Value': b'7.2.3.4'}], b'SetIdentifier': b'NA-US-KY', 
                                                                 b'TTL': 61, 
                                                                 b'Type': b'A'}},
                                       {b'Action': b'UPSERT', 
                                          b'ResourceRecordSet': {b'GeoLocation': {b'ContinentCode': b'AF'}, b'Name': b'unit.tests.', 
                                                                 b'HealthCheckId': b'42', 
                                                                 b'ResourceRecords': [{b'Value': b'4.2.3.4'}], b'SetIdentifier': b'AF', 
                                                                 b'TTL': 61, 
                                                                 b'Type': b'A'}},
                                       {b'Action': b'UPSERT', 
                                          b'ResourceRecordSet': {b'GeoLocation': {b'CountryCode': b'US'}, b'HealthCheckId': b'43', 
                                                                 b'Name': b'unit.tests.', 
                                                                 b'ResourceRecords': [{b'Value': b'5.2.3.4'}, {b'Value': b'6.2.3.4'}], b'SetIdentifier': b'NA-US', 
                                                                 b'TTL': 61, 
                                                                 b'Type': b'A'}},
                                       {b'Action': b'CREATE', 
                                          b'ResourceRecordSet': {b'GeoLocation': {b'CountryCode': b'US', b'SubdivisionCode': b'CA'}, 
                                                                 b'HealthCheckId': b'44', 
                                                                 b'Name': b'unit.tests.', 
                                                                 b'ResourceRecords': [{b'Value': b'7.2.3.4'}], b'SetIdentifier': b'NA-US-CA', 
                                                                 b'TTL': 61, 
                                                                 b'Type': b'A'}},
                                       {b'Action': b'UPSERT', 
                                          b'ResourceRecordSet': {b'GeoLocation': {b'CountryCode': b'*'}, b'Name': b'unit.tests.', 
                                                                 b'ResourceRecords': [{b'Value': b'2.2.3.4'}, {b'Value': b'3.2.3.4'}], b'SetIdentifier': b'default', 
                                                                 b'TTL': 61, 
                                                                 b'Type': b'A'}}], 
                            b'Comment': ANY}, 
           b'HostedZoneId': b'z42'}
        stubber.add_response(b'change_resource_record_sets', {b'ChangeInfo': {b'Id': b'id', 
                           b'Status': b'PENDING', 
                           b'SubmittedAt': b'2017-01-29T01:02:03Z'}}, change_resource_record_sets_params)
        plan = provider.plan(self.expected)
        self.assertEquals(1, len(plan.changes))
        self.assertIsInstance(plan.changes[0], Update)
        self.assertEquals(1, provider.apply(plan))
        stubber.assert_no_pending_responses()

        def mod_add_geo_populate(existing, target, lenient):
            for record in self.expected.records:
                if record._type != b'A' or record.geo:
                    existing.add_record(record)

            record = Record.new(existing, b'simple', {b'ttl': 61, 
               b'type': b'A', 
               b'values': [
                         b'1.2.3.4', b'2.2.3.4'], 
               b'geo': {b'OC': [
                              b'3.2.3.4', b'4.2.3.4']}})
            existing.add_record(record)

        provider.populate = mod_add_geo_populate
        change_resource_record_sets_params = {b'ChangeBatch': {b'Changes': [
                                       {b'Action': b'DELETE', 
                                          b'ResourceRecordSet': {b'GeoLocation': {b'ContinentCode': b'OC'}, b'Name': b'simple.unit.tests.', 
                                                                 b'ResourceRecords': [{b'Value': b'3.2.3.4'}, {b'Value': b'4.2.3.4'}], b'SetIdentifier': b'OC', 
                                                                 b'TTL': 61, 
                                                                 b'Type': b'A'}},
                                       {b'Action': b'DELETE', 
                                          b'ResourceRecordSet': {b'GeoLocation': {b'CountryCode': b'*'}, b'Name': b'simple.unit.tests.', 
                                                                 b'ResourceRecords': [{b'Value': b'1.2.3.4'}, {b'Value': b'2.2.3.4'}], b'SetIdentifier': b'default', 
                                                                 b'TTL': 61, 
                                                                 b'Type': b'A'}},
                                       {b'Action': b'CREATE', 
                                          b'ResourceRecordSet': {b'Name': b'simple.unit.tests.', 
                                                                 b'ResourceRecords': [{b'Value': b'1.2.3.4'}, {b'Value': b'2.2.3.4'}], b'TTL': 60, 
                                                                 b'Type': b'A'}}], 
                            b'Comment': ANY}, 
           b'HostedZoneId': b'z42'}
        stubber.add_response(b'change_resource_record_sets', {b'ChangeInfo': {b'Id': b'id', 
                           b'Status': b'PENDING', 
                           b'SubmittedAt': b'2017-01-29T01:02:03Z'}}, change_resource_record_sets_params)
        plan = provider.plan(self.expected)
        self.assertEquals(1, len(plan.changes))
        self.assertIsInstance(plan.changes[0], Update)
        self.assertEquals(1, provider.apply(plan))
        stubber.assert_no_pending_responses()

    def test_sync_create(self):
        provider, stubber = self._get_stubbed_provider()
        got = Zone(b'unit.tests.', [])
        list_hosted_zones_resp = {b'HostedZones': [], b'Marker': b'm', 
           b'IsTruncated': False, 
           b'MaxItems': b'100'}
        stubber.add_response(b'list_hosted_zones', list_hosted_zones_resp, {})
        plan = provider.plan(self.expected)
        self.assertEquals(9, len(plan.changes))
        self.assertFalse(plan.exists)
        for change in plan.changes:
            self.assertIsInstance(change, Create)

        stubber.assert_no_pending_responses()
        create_hosted_zone_resp = {b'HostedZone': {b'Name': b'unit.tests.', 
                           b'Id': b'z42', 
                           b'CallerReference': b'abc'}, 
           b'ChangeInfo': {b'Id': b'a12', 
                           b'Status': b'PENDING', 
                           b'SubmittedAt': b'2017-01-29T01:02:03Z', 
                           b'Comment': b'hrm'}, 
           b'DelegationSet': {b'Id': b'b23', 
                              b'CallerReference': b'blip', 
                              b'NameServers': [
                                             b'n12.unit.tests.']}, 
           b'Location': b'us-east-1'}
        stubber.add_response(b'create_hosted_zone', create_hosted_zone_resp, {b'Name': got.name, 
           b'CallerReference': ANY})
        list_resource_record_sets_resp = {b'ResourceRecordSets': [
                                 {b'Name': b'a.unit.tests.', 
                                    b'Type': b'A', 
                                    b'GeoLocation': {b'ContinentCode': b'NA'}, 
                                    b'ResourceRecords': [
                                                       {b'Value': b'2.2.3.4'}], 
                                    b'TTL': 61}], 
           b'IsTruncated': False, 
           b'MaxItems': b'100'}
        stubber.add_response(b'list_resource_record_sets', list_resource_record_sets_resp, {b'HostedZoneId': b'z42'})
        stubber.add_response(b'list_health_checks', {b'HealthChecks': self.health_checks, 
           b'IsTruncated': False, 
           b'MaxItems': b'100', 
           b'Marker': b''})
        stubber.add_response(b'change_resource_record_sets', {b'ChangeInfo': {b'Id': b'id', 
                           b'Status': b'PENDING', 
                           b'SubmittedAt': b'2017-01-29T01:02:03Z'}}, {b'HostedZoneId': b'z42', b'ChangeBatch': ANY})
        self.assertEquals(9, provider.apply(plan))
        stubber.assert_no_pending_responses()

    def test_health_checks_pagination(self):
        provider, stubber = self._get_stubbed_provider()
        health_checks_p1 = [
         {b'Id': b'42', 
            b'CallerReference': self.caller_ref, 
            b'HealthCheckConfig': {b'Type': b'HTTPS', 
                                   b'FullyQualifiedDomainName': b'unit.tests', 
                                   b'IPAddress': b'4.2.3.4', 
                                   b'ResourcePath': b'/_dns', 
                                   b'Type': b'HTTPS', 
                                   b'Port': 443, 
                                   b'MeasureLatency': True}, 
            b'HealthCheckVersion': 2},
         {b'Id': b'43', 
            b'CallerReference': b'abc123', 
            b'HealthCheckConfig': {b'Type': b'HTTPS', 
                                   b'FullyQualifiedDomainName': b'unit.tests', 
                                   b'IPAddress': b'9.2.3.4', 
                                   b'ResourcePath': b'/_dns', 
                                   b'Type': b'HTTPS', 
                                   b'Port': 443, 
                                   b'MeasureLatency': True}, 
            b'HealthCheckVersion': 2}]
        stubber.add_response(b'list_health_checks', {b'HealthChecks': health_checks_p1, 
           b'IsTruncated': True, 
           b'MaxItems': b'2', 
           b'Marker': b'', 
           b'NextMarker': b'moar'})
        health_checks_p2 = [
         {b'Id': b'44', 
            b'CallerReference': self.caller_ref, 
            b'HealthCheckConfig': {b'Type': b'HTTPS', 
                                   b'FullyQualifiedDomainName': b'unit.tests', 
                                   b'IPAddress': b'8.2.3.4', 
                                   b'ResourcePath': b'/_dns', 
                                   b'Type': b'HTTPS', 
                                   b'Port': 443, 
                                   b'MeasureLatency': True}, 
            b'HealthCheckVersion': 2}]
        stubber.add_response(b'list_health_checks', {b'HealthChecks': health_checks_p2, 
           b'IsTruncated': False, 
           b'MaxItems': b'2', 
           b'Marker': b'moar'}, {b'Marker': b'moar'})
        health_checks = provider.health_checks
        self.assertEquals({b'42': health_checks_p1[0], 
           b'44': health_checks_p2[0]}, health_checks)
        stubber.assert_no_pending_responses()
        record = Record.new(self.expected, b'', {b'ttl': 61, 
           b'type': b'A', 
           b'values': [
                     b'2.2.3.4', b'3.2.3.4'], 
           b'geo': {b'AF': [
                          b'4.2.3.4']}})
        value = record.geo[b'AF'].values[0]
        id = provider.get_health_check_id(record, value, True)
        self.assertEquals(b'42', id)

    def test_health_check_create(self):
        provider, stubber = self._get_stubbed_provider()
        caller_ref = (b'{}:AAAA:foo1234').format(Route53Provider.HEALTH_CHECK_VERSION)
        health_checks = [
         {b'Id': b'42', 
            b'CallerReference': b'9999:A:foo1234', 
            b'HealthCheckConfig': {b'Type': b'HTTPS', 
                                   b'FullyQualifiedDomainName': b'unit.tests', 
                                   b'IPAddress': b'4.2.3.4', 
                                   b'ResourcePath': b'/_dns', 
                                   b'Type': b'HTTPS', 
                                   b'Port': 443, 
                                   b'MeasureLatency': True}, 
            b'HealthCheckVersion': 2},
         {b'Id': b'43', 
            b'CallerReference': caller_ref, 
            b'HealthCheckConfig': {b'Type': b'HTTPS', 
                                   b'FullyQualifiedDomainName': b'unit.tests', 
                                   b'IPAddress': b'4.2.3.4', 
                                   b'ResourcePath': b'/_dns', 
                                   b'Type': b'HTTPS', 
                                   b'Port': 443, 
                                   b'MeasureLatency': True}, 
            b'HealthCheckVersion': 2}]
        stubber.add_response(b'list_health_checks', {b'HealthChecks': health_checks, 
           b'IsTruncated': False, 
           b'MaxItems': b'100', 
           b'Marker': b''})
        health_check_config = {b'EnableSNI': False, 
           b'FailureThreshold': 6, 
           b'FullyQualifiedDomainName': b'foo.bar.com', 
           b'IPAddress': b'4.2.3.4', 
           b'MeasureLatency': True, 
           b'Port': 8080, 
           b'RequestInterval': 10, 
           b'ResourcePath': b'/_status', 
           b'Type': b'HTTP'}
        stubber.add_response(b'create_health_check', {b'HealthCheck': {b'Id': b'42', 
                            b'CallerReference': self.caller_ref, 
                            b'HealthCheckConfig': health_check_config, 
                            b'HealthCheckVersion': 1}, 
           b'Location': b'http://url'}, {b'CallerReference': ANY, 
           b'HealthCheckConfig': health_check_config})
        stubber.add_response(b'change_tags_for_resource', {})
        record = Record.new(self.expected, b'', {b'ttl': 61, 
           b'type': b'A', 
           b'values': [
                     b'2.2.3.4', b'3.2.3.4'], 
           b'geo': {b'AF': [
                          b'4.2.3.4']}, 
           b'octodns': {b'healthcheck': {b'host': b'foo.bar.com', 
                                         b'path': b'/_status', 
                                         b'port': 8080, 
                                         b'protocol': b'HTTP'}}})
        value = record.geo[b'AF'].values[0]
        id = provider.get_health_check_id(record, value, False)
        self.assertFalse(id)
        id = provider.get_health_check_id(record, value, True)
        self.assertEquals(b'42', id)
        stubber.assert_no_pending_responses()
        health_check_config = {b'EnableSNI': False, 
           b'FailureThreshold': 6, 
           b'FullyQualifiedDomainName': b'target-1.unit.tests.', 
           b'MeasureLatency': True, 
           b'Port': 8080, 
           b'RequestInterval': 10, 
           b'ResourcePath': b'/_status', 
           b'Type': b'HTTP'}
        stubber.add_response(b'create_health_check', {b'HealthCheck': {b'Id': b'42', 
                            b'CallerReference': self.caller_ref, 
                            b'HealthCheckConfig': health_check_config, 
                            b'HealthCheckVersion': 1}, 
           b'Location': b'http://url'}, {b'CallerReference': ANY, 
           b'HealthCheckConfig': health_check_config})
        stubber.add_response(b'change_tags_for_resource', {})
        id = provider.get_health_check_id(record, b'target-1.unit.tests.', True)
        self.assertEquals(b'42', id)
        stubber.assert_no_pending_responses()

    def test_health_check_measure_latency(self):
        provider, stubber = self._get_stubbed_provider()
        record_true = Record.new(self.expected, b'a', {b'ttl': 61, 
           b'type': b'A', 
           b'value': b'1.2.3.4', 
           b'octodns': {b'healthcheck': {}, b'route53': {b'healthcheck': {b'measure_latency': True}}}})
        measure_latency = provider._healthcheck_measure_latency(record_true)
        self.assertTrue(measure_latency)
        record_default = Record.new(self.expected, b'a', {b'ttl': 61, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        measure_latency = provider._healthcheck_measure_latency(record_default)
        self.assertTrue(measure_latency)
        record_false = Record.new(self.expected, b'a', {b'ttl': 61, 
           b'type': b'A', 
           b'value': b'1.2.3.4', 
           b'octodns': {b'healthcheck': {}, b'route53': {b'healthcheck': {b'measure_latency': False}}}})
        measure_latency = provider._healthcheck_measure_latency(record_false)
        self.assertFalse(measure_latency)

    def test_create_health_checks_measure_latency(self):
        provider, stubber = self._get_stubbed_provider()
        health_check_config = {b'EnableSNI': True, 
           b'FailureThreshold': 6, 
           b'FullyQualifiedDomainName': b'a.unit.tests', 
           b'IPAddress': b'1.2.3.4', 
           b'MeasureLatency': False, 
           b'Port': 443, 
           b'RequestInterval': 10, 
           b'ResourcePath': b'/_dns', 
           b'Type': b'HTTPS'}
        stubber.add_response(b'list_health_checks', {b'HealthChecks': [], b'IsTruncated': False, 
           b'MaxItems': b'100', 
           b'Marker': b''})
        stubber.add_response(b'create_health_check', {b'HealthCheck': {b'Id': b'42', 
                            b'CallerReference': self.caller_ref, 
                            b'HealthCheckConfig': health_check_config, 
                            b'HealthCheckVersion': 1}, 
           b'Location': b'http://url'}, {b'CallerReference': ANY, 
           b'HealthCheckConfig': health_check_config})
        stubber.add_response(b'change_tags_for_resource', {})
        stubber.add_response(b'change_tags_for_resource', {})
        record = Record.new(self.expected, b'a', {b'ttl': 61, 
           b'type': b'A', 
           b'value': b'2.2.3.4', 
           b'geo': {b'AF': [
                          b'1.2.3.4']}, 
           b'octodns': {b'healthcheck': {}, b'route53': {b'healthcheck': {b'measure_latency': False}}}})
        value = record.geo[b'AF'].values[0]
        id = provider.get_health_check_id(record, value, True)
        ml = provider.health_checks[id][b'HealthCheckConfig'][b'MeasureLatency']
        self.assertEqual(False, ml)

    def test_health_check_gc(self):
        provider, stubber = self._get_stubbed_provider()
        stubber.add_response(b'list_health_checks', {b'HealthChecks': self.health_checks, 
           b'IsTruncated': False, 
           b'MaxItems': b'100', 
           b'Marker': b''})
        record = Record.new(self.expected, b'', {b'ttl': 61, 
           b'type': b'A', 
           b'values': [
                     b'2.2.3.4', b'3.2.3.4'], 
           b'geo': {b'AF': [
                          b'4.2.3.4'], 
                    b'NA-US': [
                             b'5.2.3.4', b'6.2.3.4']}})
        stubber.add_response(b'delete_health_check', {}, {b'HealthCheckId': b'44'})
        provider._gc_health_checks(record, [
         DummyR53Record(b'42'),
         DummyR53Record(b'43')])
        stubber.assert_no_pending_responses()
        stubber.add_response(b'delete_health_check', {}, {b'HealthCheckId': b'44'})
        change = Create(record)
        provider._mod_Create(change, b'z43', [])
        stubber.assert_no_pending_responses()
        stubber.add_response(b'delete_health_check', {}, {b'HealthCheckId': b'44'})
        change = Update(record, record)
        provider._mod_Create(change, b'z43', [])
        stubber.assert_no_pending_responses()
        stubber.add_response(b'delete_health_check', {}, {b'HealthCheckId': ANY})
        stubber.add_response(b'delete_health_check', {}, {b'HealthCheckId': ANY})
        stubber.add_response(b'delete_health_check', {}, {b'HealthCheckId': ANY})
        change = Delete(record)
        provider._mod_Delete(change, b'z43', [])
        stubber.assert_no_pending_responses()
        stubber.add_response(b'delete_health_check', {}, {b'HealthCheckId': b'45'})
        record = Record.new(self.expected, b'', {b'ttl': 61, 
           b'type': b'AAAA', 
           b'value': b'2001:0db8:3c4d:0015:0000:0000:1a2f:1a4b'})
        provider._gc_health_checks(record, [])
        stubber.assert_no_pending_responses()

    def test_legacy_health_check_gc(self):
        provider, stubber = self._get_stubbed_provider()
        old_caller_ref = b'0000:A:3333'
        health_checks = [
         {b'Id': b'42', 
            b'CallerReference': self.caller_ref, 
            b'HealthCheckConfig': {b'Type': b'HTTPS', 
                                   b'FullyQualifiedDomainName': b'unit.tests', 
                                   b'IPAddress': b'4.2.3.4', 
                                   b'ResourcePath': b'/_dns', 
                                   b'Type': b'HTTPS', 
                                   b'Port': 443, 
                                   b'MeasureLatency': True}, 
            b'HealthCheckVersion': 2},
         {b'Id': b'43', 
            b'CallerReference': old_caller_ref, 
            b'HealthCheckConfig': {b'Type': b'HTTPS', 
                                   b'FullyQualifiedDomainName': b'unit.tests', 
                                   b'IPAddress': b'4.2.3.4', 
                                   b'ResourcePath': b'/_dns', 
                                   b'Type': b'HTTPS', 
                                   b'Port': 443, 
                                   b'MeasureLatency': True}, 
            b'HealthCheckVersion': 2},
         {b'Id': b'44', 
            b'CallerReference': old_caller_ref, 
            b'HealthCheckConfig': {b'Type': b'HTTPS', 
                                   b'FullyQualifiedDomainName': b'other.unit.tests', 
                                   b'IPAddress': b'4.2.3.4', 
                                   b'ResourcePath': b'/_dns', 
                                   b'Type': b'HTTPS', 
                                   b'Port': 443, 
                                   b'MeasureLatency': True}, 
            b'HealthCheckVersion': 2}]
        stubber.add_response(b'list_health_checks', {b'HealthChecks': health_checks, 
           b'IsTruncated': False, 
           b'MaxItems': b'100', 
           b'Marker': b''})
        record = Record.new(self.expected, b'', {b'ttl': 61, 
           b'type': b'A', 
           b'values': [
                     b'2.2.3.4', b'3.2.3.4'], 
           b'geo': {b'AF': [
                          b'4.2.3.4'], 
                    b'NA-US': [
                             b'5.2.3.4', b'6.2.3.4'], 
                    b'NA-US-CA': [
                                b'7.2.3.4']}})
        stubber.add_response(b'delete_health_check', {}, {b'HealthCheckId': b'43'})
        provider._gc_health_checks(record, [
         DummyR53Record(b'42')])

    def test_no_extra_changes(self):
        provider, stubber = self._get_stubbed_provider()
        list_hosted_zones_resp = {b'HostedZones': [
                          {b'Name': b'unit.tests.', 
                             b'Id': b'z42', 
                             b'CallerReference': b'abc'}], 
           b'Marker': b'm', 
           b'IsTruncated': False, 
           b'MaxItems': b'100'}
        stubber.add_response(b'list_hosted_zones', list_hosted_zones_resp, {})
        desired = Zone(b'unit.tests.', [])
        extra = provider._extra_changes(desired=desired, changes=[])
        self.assertEquals([], extra)
        stubber.assert_no_pending_responses()
        desired = Zone(b'unit.tests.', [])
        record = Record.new(desired, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        desired.add_record(record)
        extra = provider._extra_changes(desired=desired, changes=[])
        self.assertEquals([], extra)
        stubber.assert_no_pending_responses()
        other = Zone(b'other.tests.', [])
        extra = provider._extra_changes(desired=other, changes=[])
        self.assertEquals([], extra)
        stubber.assert_no_pending_responses()

    def test_extra_change_no_health_check(self):
        provider, stubber = self._get_stubbed_provider()
        list_hosted_zones_resp = {b'HostedZones': [
                          {b'Name': b'unit.tests.', 
                             b'Id': b'z42', 
                             b'CallerReference': b'abc'}], 
           b'Marker': b'm', 
           b'IsTruncated': False, 
           b'MaxItems': b'100'}
        stubber.add_response(b'list_hosted_zones', list_hosted_zones_resp, {})
        desired = Zone(b'unit.tests.', [])
        record = Record.new(desired, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4', 
           b'geo': {b'NA': [
                          b'2.2.3.4']}})
        desired.add_record(record)
        list_resource_record_sets_resp = {b'ResourceRecordSets': [
                                 {b'Name': b'a.unit.tests.', 
                                    b'Type': b'A', 
                                    b'GeoLocation': {b'ContinentCode': b'NA'}, 
                                    b'ResourceRecords': [
                                                       {b'Value': b'2.2.3.4'}], 
                                    b'TTL': 61}], 
           b'IsTruncated': False, 
           b'MaxItems': b'100'}
        stubber.add_response(b'list_resource_record_sets', list_resource_record_sets_resp, {b'HostedZoneId': b'z42'})
        extra = provider._extra_changes(desired=desired, changes=[])
        self.assertEquals(1, len(extra))
        stubber.assert_no_pending_responses()

    def test_extra_change_has_wrong_health_check(self):
        provider, stubber = self._get_stubbed_provider()
        list_hosted_zones_resp = {b'HostedZones': [
                          {b'Name': b'unit.tests.', 
                             b'Id': b'z42', 
                             b'CallerReference': b'abc'}], 
           b'Marker': b'm', 
           b'IsTruncated': False, 
           b'MaxItems': b'100'}
        stubber.add_response(b'list_hosted_zones', list_hosted_zones_resp, {})
        desired = Zone(b'unit.tests.', [])
        record = Record.new(desired, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4', 
           b'geo': {b'NA': [
                          b'2.2.3.4']}})
        desired.add_record(record)
        list_resource_record_sets_resp = {b'ResourceRecordSets': [
                                 {b'Name': b'a.unit.tests.', 
                                    b'Type': b'A', 
                                    b'GeoLocation': {b'ContinentCode': b'NA'}, 
                                    b'ResourceRecords': [
                                                       {b'Value': b'2.2.3.4'}], 
                                    b'TTL': 61, 
                                    b'HealthCheckId': b'42'}], 
           b'IsTruncated': False, 
           b'MaxItems': b'100'}
        stubber.add_response(b'list_resource_record_sets', list_resource_record_sets_resp, {b'HostedZoneId': b'z42'})
        stubber.add_response(b'list_health_checks', {b'HealthChecks': [
                           {b'Id': b'42', 
                              b'CallerReference': b'foo', 
                              b'HealthCheckConfig': {b'Type': b'HTTPS', 
                                                     b'FullyQualifiedDomainName': b'unit.tests', 
                                                     b'IPAddress': b'2.2.3.4', 
                                                     b'ResourcePath': b'/_dns', 
                                                     b'Type': b'HTTPS', 
                                                     b'Port': 443, 
                                                     b'MeasureLatency': True}, 
                              b'HealthCheckVersion': 2}], 
           b'IsTruncated': False, 
           b'MaxItems': b'100', 
           b'Marker': b''})
        extra = provider._extra_changes(desired=desired, changes=[])
        self.assertEquals(1, len(extra))
        stubber.assert_no_pending_responses()
        for change in (Create(record), Update(record, record), Delete(record)):
            extra = provider._extra_changes(desired=desired, changes=[change])
            self.assertEquals(0, len(extra))
            stubber.assert_no_pending_responses()

    def test_extra_change_has_health_check(self):
        provider, stubber = self._get_stubbed_provider()
        list_hosted_zones_resp = {b'HostedZones': [
                          {b'Name': b'unit.tests.', 
                             b'Id': b'z42', 
                             b'CallerReference': b'abc'}], 
           b'Marker': b'm', 
           b'IsTruncated': False, 
           b'MaxItems': b'100'}
        stubber.add_response(b'list_hosted_zones', list_hosted_zones_resp, {})
        desired = Zone(b'unit.tests.', [])
        record = Record.new(desired, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4', 
           b'geo': {b'NA': [
                          b'2.2.3.4']}})
        desired.add_record(record)
        list_resource_record_sets_resp = {b'ResourceRecordSets': [
                                 {b'Name': b'unit.tests.', 
                                    b'Type': b'A', 
                                    b'GeoLocation': {b'CountryCode': b'*'}, 
                                    b'ResourceRecords': [
                                                       {b'Value': b'1.2.3.4'}], 
                                    b'TTL': 61},
                                 {b'Name': b'a.unit.tests.', 
                                    b'Type': b'AAAA', 
                                    b'ResourceRecords': [
                                                       {b'Value': b'2001:0db8:3c4d:0015:0000:0000:1a2f:1a4b'}], 
                                    b'TTL': 61},
                                 {b'Name': b'a.unit.tests.', 
                                    b'Type': b'A', 
                                    b'GeoLocation': {b'CountryCode': b'*'}, 
                                    b'ResourceRecords': [
                                                       {b'Value': b'1.2.3.4'}], 
                                    b'TTL': 61},
                                 {b'Name': b'a.unit.tests.', 
                                    b'Type': b'A', 
                                    b'GeoLocation': {b'ContinentCode': b'NA'}, 
                                    b'ResourceRecords': [
                                                       {b'Value': b'2.2.3.4'}], 
                                    b'TTL': 61, 
                                    b'HealthCheckId': b'42'}], 
           b'IsTruncated': False, 
           b'MaxItems': b'100'}
        stubber.add_response(b'list_resource_record_sets', list_resource_record_sets_resp, {b'HostedZoneId': b'z42'})
        stubber.add_response(b'list_health_checks', {b'HealthChecks': [
                           {b'Id': b'42', 
                              b'CallerReference': self.caller_ref, 
                              b'HealthCheckConfig': {b'Type': b'HTTPS', 
                                                     b'FullyQualifiedDomainName': b'a.unit.tests', 
                                                     b'IPAddress': b'2.2.3.4', 
                                                     b'ResourcePath': b'/_dns', 
                                                     b'Type': b'HTTPS', 
                                                     b'Port': 443, 
                                                     b'MeasureLatency': True}, 
                              b'HealthCheckVersion': 2}], 
           b'IsTruncated': False, 
           b'MaxItems': b'100', 
           b'Marker': b''})
        extra = provider._extra_changes(desired=desired, changes=[])
        self.assertEquals(0, len(extra))
        stubber.assert_no_pending_responses()
        record._octodns[b'healthcheck'] = {b'path': b'/_ready'}
        extra = provider._extra_changes(desired=desired, changes=[])
        self.assertEquals(1, len(extra))
        stubber.assert_no_pending_responses()

    def test_extra_change_dynamic_has_health_check(self):
        provider, stubber = self._get_stubbed_provider()
        list_hosted_zones_resp = {b'HostedZones': [
                          {b'Name': b'unit.tests.', 
                             b'Id': b'z42', 
                             b'CallerReference': b'abc'}], 
           b'Marker': b'm', 
           b'IsTruncated': False, 
           b'MaxItems': b'100'}
        stubber.add_response(b'list_hosted_zones', list_hosted_zones_resp, {})
        desired = Zone(b'unit.tests.', [])
        record = Record.new(desired, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4', 
           b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'2.2.3.4'}]}}, 
                        b'rules': [
                                 {b'pool': b'one'}]}})
        desired.add_record(record)
        list_resource_record_sets_resp = {b'ResourceRecordSets': [
                                 {b'Name': b'unit.tests.', 
                                    b'Type': b'A', 
                                    b'GeoLocation': {b'CountryCode': b'*'}, 
                                    b'ResourceRecords': [
                                                       {b'Value': b'1.2.3.4'}], 
                                    b'TTL': 61, 
                                    b'HealthCheckId': b'33'},
                                 {b'Name': b'a.unit.tests.', 
                                    b'Type': b'AAAA', 
                                    b'ResourceRecords': [
                                                       {b'Value': b'2001:0db8:3c4d:0015:0000:0000:1a2f:1a4b'}], 
                                    b'TTL': 61, 
                                    b'HealthCheckId': b'33'},
                                 {b'Name': b'_octodns-default-value.a.unit.tests.', 
                                    b'Type': b'A', 
                                    b'GeoLocation': {b'CountryCode': b'*'}, 
                                    b'ResourceRecords': [
                                                       {b'Value': b'1.2.3.4'}], 
                                    b'TTL': 61, 
                                    b'HealthCheckId': b'33'},
                                 {b'Name': b'_octodns-two-value.other.unit.tests.', 
                                    b'Type': b'A', 
                                    b'GeoLocation': {b'CountryCode': b'*'}, 
                                    b'ResourceRecords': [
                                                       {b'Value': b'1.2.3.4'}], 
                                    b'TTL': 61, 
                                    b'HealthCheckId': b'33'},
                                 {b'Name': b'_octodns-one-value.a.unit.tests.', 
                                    b'Type': b'AAAA', 
                                    b'ResourceRecords': [
                                                       {b'Value': b'2001:0db8:3c4d:0015:0000:0000:1a2f:1a4b'}], 
                                    b'TTL': 61, 
                                    b'HealthCheckId': b'33'},
                                 {b'Name': b'_octodns-one-value.sub.a.unit.tests.', 
                                    b'Type': b'A', 
                                    b'ResourceRecords': [
                                                       {b'Value': b'1.2.3.4'}], 
                                    b'TTL': 61, 
                                    b'HealthCheckId': b'33'},
                                 {b'Name': b'_octodns-one-value.a.unit.tests.', 
                                    b'Type': b'A', 
                                    b'ResourceRecords': [
                                                       {b'Value': b'2.2.3.4'}], 
                                    b'TTL': 61, 
                                    b'HealthCheckId': b'42'}], 
           b'IsTruncated': False, 
           b'MaxItems': b'100'}
        stubber.add_response(b'list_resource_record_sets', list_resource_record_sets_resp, {b'HostedZoneId': b'z42'})
        stubber.add_response(b'list_health_checks', {b'HealthChecks': [
                           {b'Id': b'42', 
                              b'CallerReference': self.caller_ref, 
                              b'HealthCheckConfig': {b'Type': b'HTTPS', 
                                                     b'FullyQualifiedDomainName': b'a.unit.tests', 
                                                     b'IPAddress': b'2.2.3.4', 
                                                     b'ResourcePath': b'/_dns', 
                                                     b'Type': b'HTTPS', 
                                                     b'Port': 443, 
                                                     b'MeasureLatency': True}, 
                              b'HealthCheckVersion': 2}], 
           b'IsTruncated': False, 
           b'MaxItems': b'100', 
           b'Marker': b''})
        extra = provider._extra_changes(desired=desired, changes=[])
        self.assertEquals(0, len(extra))
        stubber.assert_no_pending_responses()
        record._octodns[b'healthcheck'] = {b'path': b'/_ready'}
        extra = provider._extra_changes(desired=desired, changes=[])
        self.assertEquals(1, len(extra))
        stubber.assert_no_pending_responses()
        record._octodns[b'healthcheck'] = {b'host': b'foo.bar.io'}
        extra = provider._extra_changes(desired=desired, changes=[])
        self.assertEquals(1, len(extra))
        stubber.assert_no_pending_responses()

    def _get_test_plan(self, max_changes):
        provider = Route53Provider(b'test', b'abc', b'123', max_changes)
        stubber = Stubber(provider._conn)
        stubber.activate()
        got = Zone(b'unit.tests.', [])
        list_hosted_zones_resp = {b'HostedZones': [], b'Marker': b'm', 
           b'IsTruncated': False, 
           b'MaxItems': b'100'}
        stubber.add_response(b'list_hosted_zones', list_hosted_zones_resp, {})
        create_hosted_zone_resp = {b'HostedZone': {b'Name': b'unit.tests.', 
                           b'Id': b'z42', 
                           b'CallerReference': b'abc'}, 
           b'ChangeInfo': {b'Id': b'a12', 
                           b'Status': b'PENDING', 
                           b'SubmittedAt': b'2017-01-29T01:02:03Z', 
                           b'Comment': b'hrm'}, 
           b'DelegationSet': {b'Id': b'b23', 
                              b'CallerReference': b'blip', 
                              b'NameServers': [
                                             b'n12.unit.tests.']}, 
           b'Location': b'us-east-1'}
        stubber.add_response(b'create_hosted_zone', create_hosted_zone_resp, {b'Name': got.name, 
           b'CallerReference': ANY})
        stubber.add_response(b'list_health_checks', {b'HealthChecks': self.health_checks, 
           b'IsTruncated': False, 
           b'MaxItems': b'100', 
           b'Marker': b''})
        stubber.add_response(b'change_resource_record_sets', {b'ChangeInfo': {b'Id': b'id', 
                           b'Status': b'PENDING', 
                           b'SubmittedAt': b'2017-01-29T01:02:03Z'}}, {b'HostedZoneId': b'z42', b'ChangeBatch': ANY})
        plan = provider.plan(self.expected)
        return (
         provider, plan)

    @patch(b'octodns.provider.route53.Route53Provider._load_records')
    @patch(b'octodns.provider.route53.Route53Provider._really_apply')
    def test_apply_1(self, really_apply_mock, _):
        provider, plan = self._get_test_plan(19)
        provider.apply(plan)
        really_apply_mock.assert_called_once()

    @patch(b'octodns.provider.route53.Route53Provider._load_records')
    @patch(b'octodns.provider.route53.Route53Provider._really_apply')
    def test_apply_2(self, really_apply_mock, _):
        provider, plan = self._get_test_plan(18)
        provider.apply(plan)
        self.assertEquals(2, really_apply_mock.call_count)

    @patch(b'octodns.provider.route53.Route53Provider._load_records')
    @patch(b'octodns.provider.route53.Route53Provider._really_apply')
    def test_apply_3(self, really_apply_mock, _):
        provider, plan = self._get_test_plan(7)
        provider.apply(plan)
        self.assertEquals(3, really_apply_mock.call_count)

    @patch(b'octodns.provider.route53.Route53Provider._load_records')
    @patch(b'octodns.provider.route53.Route53Provider._really_apply')
    def test_apply_4(self, really_apply_mock, _):
        provider, plan = self._get_test_plan(11)
        provider.apply(plan)
        self.assertEquals(2, really_apply_mock.call_count)

    @patch(b'octodns.provider.route53.Route53Provider._load_records')
    @patch(b'octodns.provider.route53.Route53Provider._really_apply')
    def test_apply_bad(self, really_apply_mock, _):
        provider, plan = self._get_test_plan(1)
        with self.assertRaises(Exception) as (ctx):
            provider.apply(plan)
        self.assertTrue(b'modifications' in text_type(ctx.exception))

    def test_semicolon_fixup(self):
        provider = Route53Provider(b'test', b'abc', b'123')
        self.assertEquals({b'type': b'TXT', 
           b'ttl': 30, 
           b'values': [
                     b'abcd\\; ef\\;g',
                     b'hij\\; klm\\;n']}, provider._data_for_quoted({b'ResourceRecords': [
                              {b'Value': b'"abcd; ef;g"'},
                              {b'Value': b'"hij\\; klm\\;n"'}], 
           b'TTL': 30, 
           b'Type': b'TXT'}))

    def test_client_max_attempts(self):
        provider = Route53Provider(b'test', b'abc', b'123', client_max_attempts=42)
        self.assertEquals(43, provider._conn.meta.events._unique_id_handlers[b'retry-config-route53'][b'handler']._checker.__dict__[b'_max_attempts'])

    def test_data_for_dynamic(self):
        provider = Route53Provider(b'test', b'abc', b'123')
        data = provider._data_for_dynamic(b'', b'A', dynamic_rrsets)
        self.assertEquals(dynamic_record_data, data)

    @patch(b'octodns.provider.route53.Route53Provider._get_zone_id')
    @patch(b'octodns.provider.route53.Route53Provider._load_records')
    def test_dynamic_populate(self, load_records_mock, get_zone_id_mock):
        provider = Route53Provider(b'test', b'abc', b'123')
        get_zone_id_mock.side_effect = [
         b'z44']
        load_records_mock.side_effect = [dynamic_rrsets]
        got = Zone(b'unit.tests.', [])
        provider.populate(got)
        self.assertEquals(1, len(got.records))
        record = list(got.records)[0]
        self.assertEquals(b'', record.name)
        self.assertEquals(b'A', record._type)
        self.assertEquals([
         b'1.1.2.1',
         b'1.1.2.2'], record.values)
        self.assertTrue(record.dynamic)
        self.assertEquals({b'ap-southeast-1': {b'fallback': b'us-east-1', 
                               b'values': [
                                         {b'weight': 2, 
                                            b'value': b'1.4.1.1'},
                                         {b'weight': 2, 
                                            b'value': b'1.4.1.2'}]}, 
           b'eu-central-1': {b'fallback': b'us-east-1', 
                             b'values': [
                                       {b'weight': 1, 
                                          b'value': b'1.3.1.1'},
                                       {b'weight': 1, 
                                          b'value': b'1.3.1.2'}]}, 
           b'us-east-1': {b'fallback': None, 
                          b'values': [
                                    {b'weight': 1, 
                                       b'value': b'1.5.1.1'},
                                    {b'weight': 1, 
                                       b'value': b'1.5.1.2'}]}}, {k:v.data for k, v in record.dynamic.pools.items()})
        self.assertEquals([
         {b'geos': [
                    b'AS-CN', b'AS-JP'], 
            b'pool': b'ap-southeast-1'},
         {b'geos': [
                    b'EU', b'NA-US-FL'], 
            b'pool': b'eu-central-1'},
         {b'pool': b'us-east-1'}], [ r.data for r in record.dynamic.rules ])
        return


class DummyProvider(object):

    def get_health_check_id(self, *args, **kwargs):
        return


class TestRoute53Records(TestCase):
    existing = Zone(b'unit.tests.', [])
    record_a = Record.new(existing, b'', {b'geo': {b'NA-US': [
                         b'2.2.2.2', b'3.3.3.3'], 
                b'OC': [
                      b'4.4.4.4', b'5.5.5.5']}, 
       b'ttl': 99, 
       b'type': b'A', 
       b'values': [
                 b'9.9.9.9']})

    def test_value_fors(self):
        route53_record = _Route53Record(None, self.record_a, False)
        for value in (None, '', 'foo', 'bar', '1.2.3.4'):
            converted = route53_record._value_convert_value(value, self.record_a)
            self.assertEquals(value, converted)

        record_txt = Record.new(self.existing, b'txt', {b'ttl': 98, 
           b'type': b'TXT', 
           b'value': b'Not Important'})
        self.assertEquals(b'"Not Important"', route53_record._value_convert_quoted(record_txt.values[0], record_txt))
        return

    def test_route53_record(self):
        a = _Route53Record(None, self.record_a, False)
        self.assertEquals(a, a)
        b = _Route53Record(None, Record.new(self.existing, b'', {b'ttl': 32, b'type': b'A', b'values': [
                     b'8.8.8.8',
                     b'1.1.1.1']}), False)
        self.assertEquals(b, b)
        c = _Route53Record(None, Record.new(self.existing, b'other', {b'ttl': 99, b'type': b'A', b'values': [
                     b'9.9.9.9']}), False)
        self.assertEquals(c, c)
        d = _Route53Record(None, Record.new(self.existing, b'', {b'ttl': 42, b'type': b'MX', b'value': {b'preference': 10, 
                      b'exchange': b'foo.bar.'}}), False)
        self.assertEquals(d, d)
        self.assertEquals(a, b)
        self.assertNotEquals(a, d)
        self.assertNotEquals(a, c)
        e = _Route53GeoDefault(None, self.record_a, False)
        self.assertNotEquals(a, e)
        provider = DummyProvider()
        f = _Route53GeoRecord(provider, self.record_a, b'NA-US', self.record_a.geo[b'NA-US'], False)
        self.assertEquals(f, f)
        g = _Route53GeoRecord(provider, self.record_a, b'OC', self.record_a.geo[b'OC'], False)
        self.assertEquals(g, g)
        self.assertNotEquals(f, a)
        self.assertNotEquals(f, g)
        a.__repr__()
        e.__repr__()
        f.__repr__()
        return

    def test_route53_record_ordering(self):
        a = _Route53Record(None, self.record_a, False)
        b = _Route53Record(None, self.record_a, False)
        self.assertTrue(a == b)
        self.assertFalse(a != b)
        self.assertFalse(a < b)
        self.assertTrue(a <= b)
        self.assertFalse(a > b)
        self.assertTrue(a >= b)
        fqdn = _Route53Record(None, self.record_a, False, fqdn_override=b'other')
        self.assertFalse(a == fqdn)
        self.assertTrue(a != fqdn)
        self.assertFalse(a < fqdn)
        self.assertFalse(a <= fqdn)
        self.assertTrue(a > fqdn)
        self.assertTrue(a >= fqdn)
        provider = DummyProvider()
        geo_a = _Route53GeoRecord(provider, self.record_a, b'NA-US', self.record_a.geo[b'NA-US'], False)
        geo_b = _Route53GeoRecord(provider, self.record_a, b'NA-US', self.record_a.geo[b'NA-US'], False)
        self.assertTrue(geo_a == geo_b)
        self.assertFalse(geo_a != geo_b)
        self.assertFalse(geo_a < geo_b)
        self.assertTrue(geo_a <= geo_b)
        self.assertFalse(geo_a > geo_b)
        self.assertTrue(geo_a >= geo_b)
        geo_fqdn = _Route53GeoRecord(provider, self.record_a, b'NA-US', self.record_a.geo[b'NA-US'], False)
        geo_fqdn.fqdn = b'other'
        self.assertFalse(geo_a == geo_fqdn)
        self.assertTrue(geo_a != geo_fqdn)
        self.assertFalse(geo_a < geo_fqdn)
        self.assertFalse(geo_a <= geo_fqdn)
        self.assertTrue(geo_a > geo_fqdn)
        self.assertTrue(geo_a >= geo_fqdn)
        self.assertFalse(a == geo_a)
        self.assertTrue(a != geo_a)
        self.assertFalse(a < geo_a)
        self.assertFalse(a <= geo_a)
        self.assertTrue(a > geo_a)
        self.assertTrue(a >= geo_a)
        return

    def test_dynamic_value_delete(self):
        provider = DummyProvider()
        geo = _Route53DynamicValue(provider, self.record_a, b'iad', b'2.2.2.2', 1, 0, False)
        rrset = {b'HealthCheckId': b'x12346z', 
           b'Name': b'_octodns-iad-value.unit.tests.', 
           b'ResourceRecords': [
                              {b'Value': b'2.2.2.2'}], 
           b'SetIdentifier': b'iad-000', 
           b'TTL': 99, 
           b'Type': b'A', 
           b'Weight': 1}
        candidates = [{},
         {b'SetIdentifier': b'not-a-match'},
         {b'Name': b'not-a-match', 
            b'SetIdentifier': b'x12346z'},
         rrset]
        mod = geo.mod(b'DELETE', candidates)
        self.assertEquals(b'x12346z', mod[b'ResourceRecordSet'][b'HealthCheckId'])
        rrset[b'HealthCheckId'] = None
        mod = geo.mod(b'DELETE', [])
        self.assertEquals(rrset, mod[b'ResourceRecordSet'])
        return

    def test_geo_delete(self):
        provider = DummyProvider()
        geo = _Route53GeoRecord(provider, self.record_a, b'NA-US', self.record_a.geo[b'NA-US'], False)
        rrset = {b'GeoLocation': {b'CountryCode': b'US'}, 
           b'HealthCheckId': b'x12346z', 
           b'Name': b'unit.tests.', 
           b'ResourceRecords': [
                              {b'Value': b'2.2.2.2'},
                              {b'Value': b'3.3.3.3'}], 
           b'SetIdentifier': b'NA-US', 
           b'TTL': 99, 
           b'Type': b'A'}
        candidates = [{},
         {b'SetIdentifier': b'not-a-match'},
         {b'Name': b'not-a-match', 
            b'SetIdentifier': b'x12346z'},
         rrset]
        mod = geo.mod(b'DELETE', candidates)
        self.assertEquals(b'x12346z', mod[b'ResourceRecordSet'][b'HealthCheckId'])
        del rrset[b'HealthCheckId']
        mod = geo.mod(b'DELETE', [])
        self.assertEquals(rrset, mod[b'ResourceRecordSet'])

    def test_new_dynamic(self):
        provider = Route53Provider(b'test', b'abc', b'123')
        stubber = Stubber(provider._conn)
        stubber.activate()
        provider._health_checks = {}
        provider.get_health_check_id = lambda r, v, c: b'hc42'
        zone = Zone(b'unit.tests.', [])
        record = Record.new(zone, b'', dynamic_record_data)
        route53_records = _Route53Record.new(provider, record, b'z45', creating=True)
        self.assertEquals(18, len(route53_records))
        expected_mods = [ r.mod(b'CREATE', []) for r in route53_records ]
        expected_mods.sort(key=_mod_keyer)
        self.assertEquals([
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'HealthCheckId': b'hc42', 
                                   b'Name': b'_octodns-ap-southeast-1-value.unit.tests.', 
                                   b'ResourceRecords': [{b'Value': b'1.4.1.1'}], b'SetIdentifier': b'ap-southeast-1-000', 
                                   b'TTL': 60, 
                                   b'Type': b'A', 
                                   b'Weight': 2}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'HealthCheckId': b'hc42', 
                                   b'Name': b'_octodns-ap-southeast-1-value.unit.tests.', 
                                   b'ResourceRecords': [{b'Value': b'1.4.1.2'}], b'SetIdentifier': b'ap-southeast-1-001', 
                                   b'TTL': 60, 
                                   b'Type': b'A', 
                                   b'Weight': 2}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'Name': b'_octodns-default-pool.unit.tests.', 
                                   b'ResourceRecords': [{b'Value': b'1.1.2.1'}, {b'Value': b'1.1.2.2'}], b'TTL': 60, 
                                   b'Type': b'A'}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'HealthCheckId': b'hc42', 
                                   b'Name': b'_octodns-eu-central-1-value.unit.tests.', 
                                   b'ResourceRecords': [{b'Value': b'1.3.1.1'}], b'SetIdentifier': b'eu-central-1-000', 
                                   b'TTL': 60, 
                                   b'Type': b'A', 
                                   b'Weight': 1}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'HealthCheckId': b'hc42', 
                                   b'Name': b'_octodns-eu-central-1-value.unit.tests.', 
                                   b'ResourceRecords': [{b'Value': b'1.3.1.2'}], b'SetIdentifier': b'eu-central-1-001', 
                                   b'TTL': 60, 
                                   b'Type': b'A', 
                                   b'Weight': 1}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'HealthCheckId': b'hc42', 
                                   b'Name': b'_octodns-us-east-1-value.unit.tests.', 
                                   b'ResourceRecords': [{b'Value': b'1.5.1.1'}], b'SetIdentifier': b'us-east-1-000', 
                                   b'TTL': 60, 
                                   b'Type': b'A', 
                                   b'Weight': 1}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'HealthCheckId': b'hc42', 
                                   b'Name': b'_octodns-us-east-1-value.unit.tests.', 
                                   b'ResourceRecords': [{b'Value': b'1.5.1.2'}], b'SetIdentifier': b'us-east-1-001', 
                                   b'TTL': 60, 
                                   b'Type': b'A', 
                                   b'Weight': 1}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'AliasTarget': {b'DNSName': b'_octodns-ap-southeast-1-value.unit.tests.', 
                                                    b'EvaluateTargetHealth': True, 
                                                    b'HostedZoneId': b'z45'}, 
                                   b'Failover': b'PRIMARY', 
                                   b'Name': b'_octodns-ap-southeast-1-pool.unit.tests.', 
                                   b'SetIdentifier': b'ap-southeast-1-Primary', 
                                   b'Type': b'A'}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'AliasTarget': {b'DNSName': b'_octodns-eu-central-1-value.unit.tests.', 
                                                    b'EvaluateTargetHealth': True, 
                                                    b'HostedZoneId': b'z45'}, 
                                   b'Failover': b'PRIMARY', 
                                   b'Name': b'_octodns-eu-central-1-pool.unit.tests.', 
                                   b'SetIdentifier': b'eu-central-1-Primary', 
                                   b'Type': b'A'}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'AliasTarget': {b'DNSName': b'_octodns-us-east-1-value.unit.tests.', 
                                                    b'EvaluateTargetHealth': True, 
                                                    b'HostedZoneId': b'z45'}, 
                                   b'Failover': b'PRIMARY', 
                                   b'Name': b'_octodns-us-east-1-pool.unit.tests.', 
                                   b'SetIdentifier': b'us-east-1-Primary', 
                                   b'Type': b'A'}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'AliasTarget': {b'DNSName': b'_octodns-us-east-1-pool.unit.tests.', 
                                                    b'EvaluateTargetHealth': True, 
                                                    b'HostedZoneId': b'z45'}, 
                                   b'Failover': b'SECONDARY', 
                                   b'Name': b'_octodns-ap-southeast-1-pool.unit.tests.', 
                                   b'SetIdentifier': b'ap-southeast-1-Secondary-us-east-1', 
                                   b'Type': b'A'}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'AliasTarget': {b'DNSName': b'_octodns-us-east-1-pool.unit.tests.', 
                                                    b'EvaluateTargetHealth': True, 
                                                    b'HostedZoneId': b'z45'}, 
                                   b'Failover': b'SECONDARY', 
                                   b'Name': b'_octodns-eu-central-1-pool.unit.tests.', 
                                   b'SetIdentifier': b'eu-central-1-Secondary-us-east-1', 
                                   b'Type': b'A'}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'AliasTarget': {b'DNSName': b'_octodns-default-pool.unit.tests.', 
                                                    b'EvaluateTargetHealth': True, 
                                                    b'HostedZoneId': b'z45'}, 
                                   b'Failover': b'SECONDARY', 
                                   b'Name': b'_octodns-us-east-1-pool.unit.tests.', 
                                   b'SetIdentifier': b'us-east-1-Secondary-default', 
                                   b'Type': b'A'}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'AliasTarget': {b'DNSName': b'_octodns-ap-southeast-1-pool.unit.tests.', 
                                                    b'EvaluateTargetHealth': True, 
                                                    b'HostedZoneId': b'z45'}, 
                                   b'GeoLocation': {b'CountryCode': b'CN'}, 
                                   b'Name': b'unit.tests.', 
                                   b'SetIdentifier': b'0-ap-southeast-1-AS-CN', 
                                   b'Type': b'A'}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'AliasTarget': {b'DNSName': b'_octodns-ap-southeast-1-pool.unit.tests.', 
                                                    b'EvaluateTargetHealth': True, 
                                                    b'HostedZoneId': b'z45'}, 
                                   b'GeoLocation': {b'CountryCode': b'JP'}, 
                                   b'Name': b'unit.tests.', 
                                   b'SetIdentifier': b'0-ap-southeast-1-AS-JP', 
                                   b'Type': b'A'}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'AliasTarget': {b'DNSName': b'_octodns-eu-central-1-pool.unit.tests.', 
                                                    b'EvaluateTargetHealth': True, 
                                                    b'HostedZoneId': b'z45'}, 
                                   b'GeoLocation': {b'ContinentCode': b'EU'}, 
                                   b'Name': b'unit.tests.', 
                                   b'SetIdentifier': b'1-eu-central-1-EU', 
                                   b'Type': b'A'}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'AliasTarget': {b'DNSName': b'_octodns-eu-central-1-pool.unit.tests.', 
                                                    b'EvaluateTargetHealth': True, 
                                                    b'HostedZoneId': b'z45'}, 
                                   b'GeoLocation': {b'CountryCode': b'US', 
                                                    b'SubdivisionCode': b'FL'}, 
                                   b'Name': b'unit.tests.', 
                                   b'SetIdentifier': b'1-eu-central-1-NA-US-FL', 
                                   b'Type': b'A'}},
         {b'Action': b'CREATE', 
            b'ResourceRecordSet': {b'AliasTarget': {b'DNSName': b'_octodns-us-east-1-pool.unit.tests.', 
                                                    b'EvaluateTargetHealth': True, 
                                                    b'HostedZoneId': b'z45'}, 
                                   b'GeoLocation': {b'CountryCode': b'*'}, 
                                   b'Name': b'unit.tests.', 
                                   b'SetIdentifier': b'2-us-east-1-None', 
                                   b'Type': b'A'}}], expected_mods)
        for route53_record in route53_records:
            route53_record.__repr__()


class TestModKeyer(TestCase):

    def test_mod_keyer(self):
        self.assertEquals((0, 0, 'something'), _mod_keyer({b'Action': b'DELETE', 
           b'ResourceRecordSet': {b'Name': b'something'}}))
        self.assertEquals((1, 0, 'another'), _mod_keyer({b'Action': b'CREATE', 
           b'ResourceRecordSet': {b'Name': b'another'}}))
        self.assertEquals((1, 0, 'last'), _mod_keyer({b'Action': b'UPSERT', 
           b'ResourceRecordSet': {b'Name': b'last'}}))
        self.assertEquals((0, -1, 'thing'), _mod_keyer({b'Action': b'DELETE', 
           b'ResourceRecordSet': {b'AliasTarget': b'some-target', 
                                  b'Failover': b'PRIMARY', 
                                  b'Name': b'thing'}}))
        self.assertEquals((1, 1, 'thing'), _mod_keyer({b'Action': b'UPSERT', 
           b'ResourceRecordSet': {b'AliasTarget': b'some-target', 
                                  b'Failover': b'PRIMARY', 
                                  b'Name': b'thing'}}))
        self.assertEquals((0, -2, 'thing'), _mod_keyer({b'Action': b'DELETE', 
           b'ResourceRecordSet': {b'AliasTarget': b'some-target', 
                                  b'Failover': b'SECONDARY', 
                                  b'Name': b'thing'}}))
        self.assertEquals((1, 2, 'thing'), _mod_keyer({b'Action': b'UPSERT', 
           b'ResourceRecordSet': {b'AliasTarget': b'some-target', 
                                  b'Failover': b'SECONDARY', 
                                  b'Name': b'thing'}}))
        self.assertEquals((0, -3, 'some-id'), _mod_keyer({b'Action': b'DELETE', 
           b'ResourceRecordSet': {b'GeoLocation': b'some-target', 
                                  b'SetIdentifier': b'some-id'}}))
        self.assertEquals((1, 3, 'some-id'), _mod_keyer({b'Action': b'UPSERT', 
           b'ResourceRecordSet': {b'GeoLocation': b'some-target', 
                                  b'SetIdentifier': b'some-id'}}))