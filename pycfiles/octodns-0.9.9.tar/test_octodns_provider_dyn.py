# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_dyn.py
# Compiled at: 2019-10-18 13:06:59
from __future__ import absolute_import, division, print_function, unicode_literals
from dyn.tm.errors import DynectGetError
from dyn.tm.services.dsf import DSFResponsePool
from json import loads
from mock import MagicMock, call, patch
from unittest import TestCase
from octodns.record import Create, Delete, Record, Update
from octodns.provider.base import Plan
from octodns.provider.dyn import DynProvider, _CachingDynZone, DSFMonitor, _dynamic_value_sort_key
from octodns.zone import Zone
from helpers import SimpleProvider

class _DummyPool(object):

    def __init__(self, response_pool_id):
        self.response_pool_id = response_pool_id
        self.deleted = False

    def delete(self):
        self.deleted = True


class TestDynProvider(TestCase):
    expected = Zone(b'unit.tests.', [])
    for name, data in (
     (
      b'',
      {b'type': b'A', 
         b'ttl': 300, 
         b'values': [
                   b'1.2.3.4']}),
     (
      b'cname',
      {b'type': b'CNAME', 
         b'ttl': 301, 
         b'value': b'unit.tests.'}),
     (
      b'',
      {b'type': b'MX', 
         b'ttl': 302, 
         b'values': [
                   {b'preference': 10, 
                      b'exchange': b'smtp-1.unit.tests.'},
                   {b'preference': 20, 
                      b'exchange': b'smtp-2.unit.tests.'}]}),
     (
      b'naptr',
      {b'type': b'NAPTR', 
         b'ttl': 303, 
         b'values': [
                   {b'order': 100, 
                      b'preference': 101, 
                      b'flags': b'U', 
                      b'service': b'SIP+D2U', 
                      b'regexp': b'!^.*$!sip:info@foo.example.com!', 
                      b'replacement': b'.'},
                   {b'order': 200, 
                      b'preference': 201, 
                      b'flags': b'U', 
                      b'service': b'SIP+D2U', 
                      b'regexp': b'!^.*$!sip:info@bar.example.com!', 
                      b'replacement': b'.'}]}),
     (
      b'sub',
      {b'type': b'NS', 
         b'ttl': 3600, 
         b'values': [
                   b'ns3.p10.dynect.net.', b'ns3.p10.dynect.net.']}),
     (
      b'ptr',
      {b'type': b'PTR', 
         b'ttl': 304, 
         b'value': b'xx.unit.tests.'}),
     (
      b'spf',
      {b'type': b'SPF', 
         b'ttl': 305, 
         b'values': [
                   b'v=spf1 ip4:192.168.0.1/16-all', b'v=spf1 -all']}),
     (
      b'',
      {b'type': b'SSHFP', 
         b'ttl': 306, 
         b'value': {b'algorithm': 1, 
                    b'fingerprint_type': 1, 
                    b'fingerprint': b'bf6b6825d2977c511a475bbefb88aad54a92ac73'}}),
     (
      b'_srv._tcp',
      {b'type': b'SRV', 
         b'ttl': 307, 
         b'values': [
                   {b'priority': 11, 
                      b'weight': 12, 
                      b'port': 10, 
                      b'target': b'foo-1.unit.tests.'},
                   {b'priority': 21, 
                      b'weight': 22, 
                      b'port': 20, 
                      b'target': b'foo-2.unit.tests.'}]}),
     (
      b'',
      {b'type': b'CAA', 
         b'ttl': 308, 
         b'values': [
                   {b'flags': 0, 
                      b'tag': b'issue', 
                      b'value': b'ca.unit.tests'}]})):
        expected.add_record(Record.new(expected, name, data))

    @classmethod
    def setUpClass(self):
        with patch(b'dyn.core.SessionEngine.execute', return_value={b'status': b'success'}):
            provider = DynProvider(b'test', b'cust', b'user', b'pass')
            provider._check_dyn_sess()

    def setUp(self):
        _CachingDynZone.flush_zone(self.expected.name[:-1])

    @patch(b'dyn.core.SessionEngine.execute')
    def test_populate_non_existent(self, execute_mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass')
        execute_mock.side_effect = [
         DynectGetError(b'foo')]
        got = Zone(b'unit.tests.', [])
        provider.populate(got)
        execute_mock.assert_has_calls([
         call(b'/Zone/unit.tests/', b'GET', {})])
        self.assertEquals(set(), got.records)

    @patch(b'dyn.core.SessionEngine.execute')
    def test_populate(self, execute_mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass')
        execute_mock.side_effect = [{b'data': {}},
         {b'data': {b'a_records': [
                                   {b'fqdn': b'unit.tests', 
                                      b'rdata': {b'address': b'1.2.3.4'}, b'record_id': 1, 
                                      b'record_type': b'A', 
                                      b'ttl': 300, 
                                      b'zone': b'unit.tests'}], 
                      b'cname_records': [
                                       {b'fqdn': b'cname.unit.tests', 
                                          b'rdata': {b'cname': b'unit.tests.'}, b'record_id': 2, 
                                          b'record_type': b'CNAME', 
                                          b'ttl': 301, 
                                          b'zone': b'unit.tests'}], 
                      b'ns_records': [
                                    {b'fqdn': b'unit.tests', 
                                       b'rdata': {b'nsdname': b'ns1.p10.dynect.net.'}, b'record_id': 254597562, 
                                       b'record_type': b'NS', 
                                       b'service_class': b'', 
                                       b'ttl': 3600, 
                                       b'zone': b'unit.tests'},
                                    {b'fqdn': b'unit.tests', 
                                       b'rdata': {b'nsdname': b'ns2.p10.dynect.net.'}, b'record_id': 254597563, 
                                       b'record_type': b'NS', 
                                       b'service_class': b'', 
                                       b'ttl': 3600, 
                                       b'zone': b'unit.tests'},
                                    {b'fqdn': b'unit.tests', 
                                       b'rdata': {b'nsdname': b'ns3.p10.dynect.net.'}, b'record_id': 254597564, 
                                       b'record_type': b'NS', 
                                       b'service_class': b'', 
                                       b'ttl': 3600, 
                                       b'zone': b'unit.tests'},
                                    {b'fqdn': b'unit.tests', 
                                       b'rdata': {b'nsdname': b'ns4.p10.dynect.net.'}, b'record_id': 254597565, 
                                       b'record_type': b'NS', 
                                       b'service_class': b'', 
                                       b'ttl': 3600, 
                                       b'zone': b'unit.tests'},
                                    {b'fqdn': b'sub.unit.tests', 
                                       b'rdata': {b'nsdname': b'ns3.p10.dynect.net.'}, b'record_id': 254597564, 
                                       b'record_type': b'NS', 
                                       b'service_class': b'', 
                                       b'ttl': 3600, 
                                       b'zone': b'unit.tests'},
                                    {b'fqdn': b'sub.unit.tests', 
                                       b'rdata': {b'nsdname': b'ns3.p10.dynect.net.'}, b'record_id': 254597564, 
                                       b'record_type': b'NS', 
                                       b'service_class': b'', 
                                       b'ttl': 3600, 
                                       b'zone': b'unit.tests'}], 
                      b'mx_records': [
                                    {b'fqdn': b'unit.tests', 
                                       b'rdata': {b'exchange': b'smtp-1.unit.tests.', b'preference': 10}, 
                                       b'record_id': 3, 
                                       b'record_type': b'MX', 
                                       b'ttl': 302, 
                                       b'zone': b'unit.tests'},
                                    {b'fqdn': b'unit.tests', 
                                       b'rdata': {b'exchange': b'smtp-2.unit.tests.', b'preference': 20}, 
                                       b'record_id': 4, 
                                       b'record_type': b'MX', 
                                       b'ttl': 302, 
                                       b'zone': b'unit.tests'}], 
                      b'naptr_records': [
                                       {b'fqdn': b'naptr.unit.tests', 
                                          b'rdata': {b'flags': b'U', b'order': 100, 
                                                     b'preference': 101, 
                                                     b'regexp': b'!^.*$!sip:info@foo.example.com!', 
                                                     b'replacement': b'.', 
                                                     b'services': b'SIP+D2U'}, 
                                          b'record_id': 5, 
                                          b'record_type': b'MX', 
                                          b'ttl': 303, 
                                          b'zone': b'unit.tests'},
                                       {b'fqdn': b'naptr.unit.tests', 
                                          b'rdata': {b'flags': b'U', b'order': 200, 
                                                     b'preference': 201, 
                                                     b'regexp': b'!^.*$!sip:info@bar.example.com!', 
                                                     b'replacement': b'.', 
                                                     b'services': b'SIP+D2U'}, 
                                          b'record_id': 6, 
                                          b'record_type': b'MX', 
                                          b'ttl': 303, 
                                          b'zone': b'unit.tests'}], 
                      b'ptr_records': [
                                     {b'fqdn': b'ptr.unit.tests', 
                                        b'rdata': {b'ptrdname': b'xx.unit.tests.'}, b'record_id': 7, 
                                        b'record_type': b'PTR', 
                                        b'ttl': 304, 
                                        b'zone': b'unit.tests'}], 
                      b'soa_records': [
                                     {b'fqdn': b'unit.tests', 
                                        b'rdata': {b'txtdata': b'ns1.p16.dynect.net. hostmaster.unit.tests. 4 3600 600 604800 1800'}, b'record_id': 99, 
                                        b'record_type': b'SOA', 
                                        b'ttl': 299, 
                                        b'zone': b'unit.tests'}], 
                      b'spf_records': [
                                     {b'fqdn': b'spf.unit.tests', 
                                        b'rdata': {b'txtdata': b'v=spf1 ip4:192.168.0.1/16-all'}, b'record_id': 8, 
                                        b'record_type': b'SPF', 
                                        b'ttl': 305, 
                                        b'zone': b'unit.tests'},
                                     {b'fqdn': b'spf.unit.tests', 
                                        b'rdata': {b'txtdata': b'v=spf1 -all'}, b'record_id': 8, 
                                        b'record_type': b'SPF', 
                                        b'ttl': 305, 
                                        b'zone': b'unit.tests'}], 
                      b'sshfp_records': [
                                       {b'fqdn': b'unit.tests', 
                                          b'rdata': {b'algorithm': 1, b'fingerprint': b'bf6b6825d2977c511a475bbefb88aad54a92ac73', 
                                                     b'fptype': 1}, 
                                          b'record_id': 9, 
                                          b'record_type': b'SSHFP', 
                                          b'ttl': 306, 
                                          b'zone': b'unit.tests'}], 
                      b'srv_records': [
                                     {b'fqdn': b'_srv._tcp.unit.tests', 
                                        b'rdata': {b'port': 10, b'priority': 11, 
                                                   b'target': b'foo-1.unit.tests.', 
                                                   b'weight': 12}, 
                                        b'record_id': 10, 
                                        b'record_type': b'SRV', 
                                        b'ttl': 307, 
                                        b'zone': b'unit.tests'},
                                     {b'fqdn': b'_srv._tcp.unit.tests', 
                                        b'rdata': {b'port': 20, b'priority': 21, 
                                                   b'target': b'foo-2.unit.tests.', 
                                                   b'weight': 22}, 
                                        b'record_id': 11, 
                                        b'record_type': b'SRV', 
                                        b'ttl': 307, 
                                        b'zone': b'unit.tests'}], 
                      b'caa_records': [
                                     {b'fqdn': b'unit.tests', 
                                        b'rdata': {b'flags': 0, b'tag': b'issue', 
                                                   b'value': b'ca.unit.tests'}, 
                                        b'record_id': 12, 
                                        b'record_type': b'cAA', 
                                        b'ttl': 308, 
                                        b'zone': b'unit.tests'}]}}]
        got = Zone(b'unit.tests.', [])
        provider.populate(got)
        execute_mock.assert_has_calls([
         call(b'/Zone/unit.tests/', b'GET', {}),
         call(b'/AllRecord/unit.tests/unit.tests./', b'GET', {b'detail': b'Y'})])
        changes = self.expected.changes(got, SimpleProvider())
        self.assertEquals([], changes)

    @patch(b'dyn.core.SessionEngine.execute')
    def test_sync(self, execute_mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass')
        execute_mock.side_effect = [
         DynectGetError(b'foo'),
         DynectGetError(b'foo'), {b'data': {}},
         {b'data': {b'a_records': [
                                   {b'fqdn': b'unit.tests', 
                                      b'rdata': {b'address': b'1.2.3.4'}, b'record_id': 1, 
                                      b'record_type': b'A', 
                                      b'ttl': 30, 
                                      b'zone': b'unit.tests'},
                                   {b'fqdn': b'a.unit.tests', 
                                      b'rdata': {b'address': b'2.3.4.5'}, b'record_id': 2, 
                                      b'record_type': b'A', 
                                      b'ttl': 30, 
                                      b'zone': b'unit.tests'}], 
                      b'cname_records': [
                                       {b'fqdn': b'cname.unit.tests', 
                                          b'rdata': {b'cname': b'unit.tests.'}, b'record_id': 3, 
                                          b'record_type': b'CNAME', 
                                          b'ttl': 30, 
                                          b'zone': b'unit.tests'}], 
                      b'ptr_records': [
                                     {b'fqdn': b'ptr.unit.tests', 
                                        b'rdata': {b'ptrdname': b'xx.unit.tests.'}, b'record_id': 4, 
                                        b'record_type': b'PTR', 
                                        b'ttl': 30, 
                                        b'zone': b'unit.tests'}], 
                      b'srv_records': [
                                     {b'fqdn': b'_srv._tcp.unit.tests', 
                                        b'rdata': {b'port': 10, b'priority': 11, 
                                                   b'target': b'foo-1.unit.tests.', 
                                                   b'weight': 12}, 
                                        b'record_id': 5, 
                                        b'record_type': b'SRV', 
                                        b'ttl': 30, 
                                        b'zone': b'unit.tests'},
                                     {b'fqdn': b'_srv._tcp.unit.tests', 
                                        b'rdata': {b'port': 20, b'priority': 21, 
                                                   b'target': b'foo-2.unit.tests.', 
                                                   b'weight': 22}, 
                                        b'record_id': 6, 
                                        b'record_type': b'SRV', 
                                        b'ttl': 30, 
                                        b'zone': b'unit.tests'}]}}]
        with patch(b'dyn.tm.zones.Zone.add_record') as (add_mock):
            with patch(b'dyn.tm.zones.Zone._update') as (update_mock):
                plan = provider.plan(self.expected)
                update_mock.assert_not_called()
                provider.apply(plan)
                update_mock.assert_called()
                self.assertFalse(plan.exists)
            add_mock.assert_called()
            self.assertEquals(15, len(add_mock.call_args_list))
        execute_mock.assert_has_calls([call(b'/Zone/unit.tests/', b'GET', {}),
         call(b'/Zone/unit.tests/', b'GET', {})])
        self.assertEquals(10, len(plan.changes))
        execute_mock.reset_mock()
        new = Zone(b'unit.tests.', [])
        for name, data in (
         (
          b'a',
          {b'type': b'A', 
             b'ttl': 30, 
             b'value': b'2.3.4.5'}),
         (
          b'ptr',
          {b'type': b'PTR', 
             b'ttl': 30, 
             b'value': b'xx.unit.tests.'}),
         (
          b'_srv._tcp',
          {b'type': b'SRV', 
             b'ttl': 30, 
             b'values': [
                       {b'priority': 31, 
                          b'weight': 12, 
                          b'port': 10, 
                          b'target': b'foo-1.unit.tests.'},
                       {b'priority': 21, 
                          b'weight': 22, 
                          b'port': 20, 
                          b'target': b'foo-2.unit.tests.'}]})):
            new.add_record(Record.new(new, name, data))

        with patch(b'dyn.tm.zones.Zone.add_record') as (add_mock):
            with patch(b'dyn.tm.records.DNSRecord.delete') as (delete_mock):
                with patch(b'dyn.tm.zones.Zone._update') as (update_mock):
                    plan = provider.plan(new)
                    provider.apply(plan)
                    update_mock.assert_called()
                    self.assertTrue(plan.exists)
                self.assertEquals(4, len(delete_mock.call_args_list))
            self.assertEquals(2, len(add_mock.call_args_list))
        execute_mock.assert_has_calls([
         call(b'/AllRecord/unit.tests/unit.tests./', b'GET', {b'detail': b'Y'})])
        self.assertEquals(3, len(plan.changes))


class TestDynProviderGeo(TestCase):
    with open(b'./tests/fixtures/dyn-traffic-director-get.json') as (fh):
        traffic_director_response = loads(fh.read())

    @property
    def traffic_directors_response(self):
        return {b'data': [
                   {b'active': b'Y', 
                      b'label': b'unit.tests.:A', 
                      b'nodes': [], b'notifiers': [], b'pending_change': b'', 
                      b'rulesets': [], b'service_id': b'2ERWXQNsb_IKG2YZgYqkPvk0PBM', 
                      b'ttl': b'300'},
                   {b'active': b'Y', 
                      b'label': b'some.other.:A', 
                      b'nodes': [], b'notifiers': [], b'pending_change': b'', 
                      b'rulesets': [], b'service_id': b'3ERWXQNsb_IKG2YZgYqkPvk0PBM', 
                      b'ttl': b'300'},
                   {b'active': b'Y', 
                      b'label': b'other format', 
                      b'nodes': [], b'notifiers': [], b'pending_change': b'', 
                      b'rulesets': [], b'service_id': b'4ERWXQNsb_IKG2YZgYqkPvk0PBM', 
                      b'ttl': b'300'}]}

    @property
    def records_response(self):
        return {b'data': {b'a_records': [
                                  {b'fqdn': b'unit.tests', 
                                     b'rdata': {b'address': b'1.2.3.4'}, b'record_id': 1, 
                                     b'record_type': b'A', 
                                     b'ttl': 301, 
                                     b'zone': b'unit.tests'}]}}

    monitor_id = b'42a'
    monitors_response = {b'data': [
               {b'active': b'Y', 
                  b'agent_scheme': b'geo', 
                  b'dsf_monitor_id': monitor_id, 
                  b'endpoints': [], b'label': b'unit.tests.:A', 
                  b'notifier': [], b'expected': b'', 
                  b'header': b'User-Agent: Dyn Monitor', 
                  b'host': b'unit.tests', 
                  b'path': b'/_dns', 
                  b'port': b'443', 
                  b'timeout': b'10', 
                  b'probe_interval': b'60', 
                  b'protocol': b'HTTPS', 
                  b'response_count': b'2', 
                  b'retries': b'2', 
                  b'services': [
                              b'12311']},
               {b'active': b'Y', 
                  b'agent_scheme': b'geo', 
                  b'dsf_monitor_id': b'b52', 
                  b'endpoints': [], b'label': b'old-label.unit.tests.', 
                  b'notifier': [], b'expected': b'', 
                  b'header': b'User-Agent: Dyn Monitor', 
                  b'host': b'old-label.unit.tests', 
                  b'path': b'/_dns', 
                  b'port': b'443', 
                  b'timeout': b'10', 
                  b'probe_interval': b'60', 
                  b'protocol': b'HTTPS', 
                  b'response_count': b'2', 
                  b'retries': b'2', 
                  b'services': [
                              b'12312']}], 
       b'job_id': 3376281406, 
       b'msgs': [
               {b'ERR_CD': None, 
                  b'INFO': b'DSFMonitor_get: Here are your monitors', 
                  b'LVL': b'INFO', 
                  b'SOURCE': b'BLL'}], 
       b'status': b'success'}
    expected_geo = Zone(b'unit.tests.', [])
    geo_record = Record.new(expected_geo, b'', {b'geo': {b'AF': [
                      b'2.2.3.4', b'2.2.3.5'], 
                b'AS-JP': [
                         b'3.2.3.4', b'3.2.3.5'], 
                b'NA-US': [
                         b'4.2.3.4', b'4.2.3.5'], 
                b'NA-US-CA': [
                            b'5.2.3.4', b'5.2.3.5']}, 
       b'ttl': 300, 
       b'type': b'A', 
       b'values': [
                 b'1.2.3.4', b'1.2.3.5']})
    expected_geo.add_record(geo_record)
    expected_regular = Zone(b'unit.tests.', [])
    regular_record = Record.new(expected_regular, b'', {b'ttl': 301, 
       b'type': b'A', 
       b'value': b'1.2.3.4'})
    expected_regular.add_record(regular_record)

    def setUp(self):
        _CachingDynZone.flush_zone(b'unit.tests')

    @patch(b'dyn.core.SessionEngine.execute')
    def test_traffic_directors(self, mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', True)
        provider._dyn_sess = True
        provider.log.warn = MagicMock()
        mock.side_effect = [{b'data': []}]
        self.assertEquals({}, provider.traffic_directors)
        response = {b'data': [
                   {b'active': b'Y', 
                      b'label': b'unit.tests.:A', 
                      b'nodes': [], b'notifiers': [], b'pending_change': b'', 
                      b'rulesets': [], b'service_id': b'2ERWXQNsb_IKG2YZgYqkPvk0PBM', 
                      b'ttl': b'300'},
                   {b'active': b'Y', 
                      b'label': b'geo.unit.tests.:A', 
                      b'nodes': [], b'notifiers': [], b'pending_change': b'', 
                      b'rulesets': [], b'service_id': b'3ERWXQNsb_IKG2YZgYqkPvk0PBM', 
                      b'ttl': b'300'},
                   {b'active': b'Y', 
                      b'label': b'something else', 
                      b'nodes': [], b'notifiers': [], b'pending_change': b'', 
                      b'rulesets': [], b'service_id': b'4ERWXQNsb_IKG2YZgYqkPvk0PBM', 
                      b'ttl': b'300'}], 
           b'job_id': 3376164583, 
           b'status': b'success'}
        mock.side_effect = [
         response]
        self.assertEquals({}, provider.traffic_directors)
        provider._traffic_directors = None
        tds = provider.traffic_directors
        self.assertEquals(set([b'unit.tests.', b'geo.unit.tests.']), set(tds.keys()))
        self.assertEquals([b'A'], list(tds[b'unit.tests.'].keys()))
        self.assertEquals([b'A'], list(tds[b'geo.unit.tests.'].keys()))
        provider.log.warn.assert_called_with(b"Unsupported TrafficDirector '%s'", b'something else')
        return

    @patch(b'dyn.core.SessionEngine.execute')
    def test_traffic_director_monitor(self, mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', True)
        provider._dyn_sess = True
        existing = Zone(b'unit.tests.', [])
        geo_monitor_id = b'42x'
        mock.side_effect = [self.monitors_response,
         {b'data': {b'active': b'Y', 
                      b'dsf_monitor_id': geo_monitor_id, 
                      b'endpoints': [], b'label': b'geo.unit.tests.:A', 
                      b'notifier': b'', 
                      b'expected': b'', 
                      b'header': b'User-Agent: Dyn Monitor', 
                      b'host': b'geo.unit.tests.', 
                      b'path': b'/_dns', 
                      b'port': b'443', 
                      b'timeout': b'10', 
                      b'probe_interval': b'60', 
                      b'protocol': b'HTTPS', 
                      b'response_count': b'2', 
                      b'retries': b'2'}, 
            b'job_id': 3376259461, 
            b'msgs': [
                    {b'ERR_CD': None, b'INFO': b'add: Here is the new monitor', 
                       b'LVL': b'INFO', 
                       b'SOURCE': b'BLL'}], 
            b'status': b'success'}]
        record = Record.new(existing, b'geo', {b'ttl': 60, 
           b'type': b'A', 
           b'value': b'1.2.3.4', 
           b'octodns': {b'healthcheck': {b'host': b'foo.bar', 
                                         b'path': b'/_ready'}}})
        monitor = provider._traffic_director_monitor(record)
        self.assertEquals(geo_monitor_id, monitor.dsf_monitor_id)
        mock.assert_has_calls([
         call(b'/DSFMonitor/', b'GET', {b'detail': b'Y'}),
         call(b'/DSFMonitor/', b'POST', {b'retries': 2, 
            b'protocol': b'HTTPS', 
            b'response_count': 2, 
            b'label': b'geo.unit.tests.:A', 
            b'probe_interval': 60, 
            b'active': b'Y', 
            b'options': {b'path': b'/_ready', 
                         b'host': b'foo.bar', 
                         b'header': b'User-Agent: Dyn Monitor', 
                         b'port': 443, 
                         b'timeout': 10}})])
        self.assertTrue(b'geo.unit.tests.:A' in provider._traffic_director_monitors)
        self.assertTrue(b'unit.tests.:A' in provider._traffic_director_monitors)
        record = Record.new(existing, b'', {b'ttl': 60, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        mock.reset_mock()
        monitor = provider._traffic_director_monitor(record)
        self.assertEquals(self.monitor_id, monitor.dsf_monitor_id)
        mock.assert_not_called()
        record = Record.new(existing, b'', {b'octodns': {b'healthcheck': {b'host': b'bleep.bloop', 
                                         b'path': b'/_nope', 
                                         b'protocol': b'HTTP', 
                                         b'port': 8080}}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        mock.reset_mock()
        mock.side_effect = [
         {b'data': {b'active': b'Y', 
                      b'dsf_monitor_id': self.monitor_id, 
                      b'endpoints': [], b'label': b'unit.tests.:A', 
                      b'notifier': b'', 
                      b'expected': b'', 
                      b'header': b'User-Agent: Dyn Monitor', 
                      b'host': b'bleep.bloop', 
                      b'path': b'/_nope', 
                      b'port': b'8080', 
                      b'timeout': b'10', 
                      b'probe_interval': b'60', 
                      b'protocol': b'HTTP', 
                      b'response_count': b'2', 
                      b'retries': b'2'}, 
            b'job_id': 3376259461, 
            b'msgs': [
                    {b'ERR_CD': None, b'INFO': b'add: Here is the new monitor', 
                       b'LVL': b'INFO', 
                       b'SOURCE': b'BLL'}], 
            b'status': b'success'}]
        monitor = provider._traffic_director_monitor(record)
        self.assertEquals(self.monitor_id, monitor.dsf_monitor_id)
        mock.assert_has_calls([
         call(b'/DSFMonitor/42a/', b'PUT', {b'protocol': b'HTTP', 
            b'options': {b'path': b'/_nope', 
                         b'host': b'bleep.bloop', 
                         b'header': b'User-Agent: Dyn Monitor', 
                         b'port': 8080, 
                         b'timeout': 10}})])
        self.assertTrue(b'unit.tests.:A' in provider._traffic_director_monitors)
        monitor = provider._traffic_director_monitors[b'unit.tests.:A']
        self.assertEquals(b'bleep.bloop', monitor.host)
        self.assertEquals(b'/_nope', monitor.path)
        self.assertEquals(b'HTTP', monitor.protocol)
        self.assertEquals(b'8080', monitor.port)
        record = Record.new(existing, b'old-label', {b'ttl': 60, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        mock.reset_mock()
        mock.side_effect = [
         {b'data': {b'active': b'Y', 
                      b'dsf_monitor_id': self.monitor_id, 
                      b'endpoints': [], b'label': b'old-label.unit.tests.:A', 
                      b'notifier': b'', 
                      b'expected': b'', 
                      b'header': b'User-Agent: Dyn Monitor', 
                      b'host': b'old-label.unit.tests', 
                      b'path': b'/_dns', 
                      b'port': b'443', 
                      b'timeout': b'10', 
                      b'probe_interval': b'60', 
                      b'protocol': b'HTTPS', 
                      b'response_count': b'2', 
                      b'retries': b'2'}, 
            b'job_id': 3376259461, 
            b'msgs': [
                    {b'ERR_CD': None, b'INFO': b'add: Here is the new monitor', 
                       b'LVL': b'INFO', 
                       b'SOURCE': b'BLL'}], 
            b'status': b'success'}]
        monitor = provider._traffic_director_monitor(record)
        self.assertEquals(self.monitor_id, monitor.dsf_monitor_id)
        mock.assert_has_calls([
         call(b'/DSFMonitor/b52/', b'PUT', {b'label': b'old-label.unit.tests.:A'})])
        self.assertTrue(b'old-label.unit.tests.:A' in provider._traffic_director_monitors)
        return

    @patch(b'dyn.core.SessionEngine.execute')
    def test_extra_changes(self, mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', True)
        provider._dyn_sess = True
        mock.side_effect = [
         self.monitors_response]
        desired = Zone(b'unit.tests.', [])
        record = Record.new(desired, b'', {b'ttl': 60, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        desired.add_record(record)
        extra = provider._extra_changes(desired=desired, changes=[
         Create(record)])
        self.assertEquals(0, len(extra))
        desired = Zone(b'unit.tests.', [])
        record = Record.new(desired, b'', {b'geo': {b'NA': [
                          b'1.2.3.4']}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        desired.add_record(record)
        extra = provider._extra_changes(desired=desired, changes=[
         Create(record)])
        self.assertEquals(0, len(extra))
        extra = provider._extra_changes(desired=desired, changes=[])
        self.assertEquals(0, len(extra))
        mock.assert_called_once()
        desired = Zone(b'unit.tests.', [])
        record = Record.new(desired, b'', {b'geo': {b'NA': [
                          b'1.2.3.4']}, 
           b'octodns': {b'healthcheck': {b'host': b'foo.bar', 
                                         b'path': b'/_ready'}}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        desired.add_record(record)
        extra = provider._extra_changes(desired=desired, changes=[])
        self.assertEquals(1, len(extra))
        extra = extra[0]
        self.assertIsInstance(extra, Update)
        self.assertEquals(record, extra.record)
        desired = Zone(b'unit.tests.', [])
        record = Record.new(desired, b'geo', {b'geo': {b'NA': [
                          b'1.2.3.4']}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        desired.add_record(record)
        extra = provider._extra_changes(desired=desired, changes=[])
        self.assertEquals(1, len(extra))
        extra = extra[0]
        self.assertIsInstance(extra, Update)
        self.assertEquals(record, extra.record)

    @patch(b'dyn.core.SessionEngine.execute')
    def test_populate_traffic_directors_empty(self, mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        mock.side_effect = [{b'data': []}, {b'data': {}}, {b'data': {}}]
        got = Zone(b'unit.tests.', [])
        provider.populate(got)
        self.assertEquals(0, len(got.records))
        mock.assert_has_calls([
         call(b'/DSF/', b'GET', {b'detail': b'Y'}),
         call(b'/Zone/unit.tests/', b'GET', {}),
         call(b'/AllRecord/unit.tests/unit.tests./', b'GET', {b'detail': b'Y'})])

    @patch(b'dyn.core.SessionEngine.execute')
    def test_populate_traffic_directors_td(self, mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        got = Zone(b'unit.tests.', [])
        zone_name = got.name[:-1]
        mock.side_effect = [
         self.traffic_directors_response, {b'data': [{b'fqdn': zone_name, b'zone': zone_name}]},
         self.traffic_director_response, {b'data': [{b'fqdn': b'other', b'zone': b'other'}]}, {b'data': {}}, {b'data': {}}]
        provider.populate(got)
        self.assertEquals(1, len(got.records))
        self.assertFalse(self.expected_geo.changes(got, provider))
        mock.assert_has_calls([
         call(b'/DSF/', b'GET', {b'detail': b'Y'}),
         call(b'/DSFNode/2ERWXQNsb_IKG2YZgYqkPvk0PBM', b'GET', {}),
         call(b'/DSF/2ERWXQNsb_IKG2YZgYqkPvk0PBM/', b'GET', {b'pending_changes': b'Y'}),
         call(b'/DSFNode/3ERWXQNsb_IKG2YZgYqkPvk0PBM', b'GET', {}),
         call(b'/Zone/unit.tests/', b'GET', {}),
         call(b'/AllRecord/unit.tests/unit.tests./', b'GET', {b'detail': b'Y'})])

    @patch(b'dyn.core.SessionEngine.execute')
    def test_populate_traffic_directors_regular(self, mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        mock.side_effect = [{b'data': []}, {b'data': {}},
         self.records_response]
        got = Zone(b'unit.tests.', [])
        provider.populate(got)
        self.assertEquals(1, len(got.records))
        self.assertFalse(self.expected_regular.changes(got, provider))
        mock.assert_has_calls([
         call(b'/DSF/', b'GET', {b'detail': b'Y'}),
         call(b'/Zone/unit.tests/', b'GET', {}),
         call(b'/AllRecord/unit.tests/unit.tests./', b'GET', {b'detail': b'Y'})])

    @patch(b'dyn.core.SessionEngine.execute')
    def test_populate_traffic_directors_both(self, mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        mock.side_effect = [
         self.traffic_directors_response, {b'data': [{b'fqdn': b'unit.tests', b'zone': b'unit.tests'}]},
         self.traffic_director_response, {b'data': [{b'fqdn': b'other', b'zone': b'other'}]}, {b'data': {}},
         self.records_response]
        got = Zone(b'unit.tests.', [])
        provider.populate(got)
        self.assertEquals(1, len(got.records))
        self.assertFalse(self.expected_geo.changes(got, provider))
        mock.assert_has_calls([
         call(b'/DSF/', b'GET', {b'detail': b'Y'}),
         call(b'/DSFNode/2ERWXQNsb_IKG2YZgYqkPvk0PBM', b'GET', {}),
         call(b'/DSF/2ERWXQNsb_IKG2YZgYqkPvk0PBM/', b'GET', {b'pending_changes': b'Y'}),
         call(b'/DSFNode/3ERWXQNsb_IKG2YZgYqkPvk0PBM', b'GET', {}),
         call(b'/Zone/unit.tests/', b'GET', {}),
         call(b'/AllRecord/unit.tests/unit.tests./', b'GET', {b'detail': b'Y'})])

    @patch(b'dyn.core.SessionEngine.execute')
    def test_populate_traffic_director_busted(self, mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        busted_traffic_director_response = {b'status': b'success', 
           b'data': {b'notifiers': [], b'rulesets': [], b'ttl': b'300', 
                     b'active': b'Y', 
                     b'service_id': b'oIRZ4lM-W64NUelJGuzuVziZ4MI', 
                     b'nodes': [
                              {b'fqdn': b'unit.tests', 
                                 b'zone': b'unit.tests'}], 
                     b'pending_change': b'', 
                     b'label': b'unit.tests.:A'}, 
           b'job_id': 3376642606, 
           b'msgs': [
                   {b'INFO': b'detail: Here is your service', 
                      b'LVL': b'INFO', 
                      b'ERR_CD': None, 
                      b'SOURCE': b'BLL'}]}
        mock.side_effect = [
         self.traffic_directors_response, {b'data': [{b'fqdn': b'unit.tests', b'zone': b'unit.tests'}]},
         busted_traffic_director_response, {b'data': [{b'fqdn': b'other', b'zone': b'other'}]}, {b'data': {}}, {b'data': {}}]
        got = Zone(b'unit.tests.', [])
        provider.populate(got)
        self.assertEquals(1, len(got.records))
        self.assertEquals(self.expected_geo.records, got.records)
        mock.assert_has_calls([
         call(b'/DSF/', b'GET', {b'detail': b'Y'}),
         call(b'/DSFNode/2ERWXQNsb_IKG2YZgYqkPvk0PBM', b'GET', {}),
         call(b'/DSF/2ERWXQNsb_IKG2YZgYqkPvk0PBM/', b'GET', {b'pending_changes': b'Y'}),
         call(b'/DSFNode/3ERWXQNsb_IKG2YZgYqkPvk0PBM', b'GET', {}),
         call(b'/Zone/unit.tests/', b'GET', {}),
         call(b'/AllRecord/unit.tests/unit.tests./', b'GET', {b'detail': b'Y'})])
        return

    @patch(b'dyn.core.SessionEngine.execute')
    def test_apply_traffic_director(self, mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        provider._mod_geo_Create = MagicMock()
        provider._mod_geo_Update = MagicMock()
        provider._mod_geo_Delete = MagicMock()
        provider._mod_Create = MagicMock()
        provider._mod_Update = MagicMock()
        provider._mod_Delete = MagicMock()
        mock.side_effect = [{b'data': {}}, {b'data': {}}]
        desired = Zone(b'unit.tests.', [])
        geo = self.geo_record
        regular = self.regular_record
        changes = [
         Create(geo),
         Create(regular),
         Update(geo, geo),
         Update(regular, regular),
         Delete(geo),
         Delete(regular)]
        plan = Plan(None, desired, changes, True)
        provider._apply(plan)
        mock.assert_has_calls([
         call(b'/Zone/unit.tests/', b'GET', {}),
         call(b'/Zone/unit.tests/', b'PUT', {b'publish': True})])
        provider._mod_geo_Create.assert_called_once()
        provider._mod_geo_Update.assert_called_once()
        provider._mod_geo_Delete.assert_called_once()
        provider._mod_Create.assert_called_once()
        provider._mod_Update.assert_called_once()
        provider._mod_Delete.assert_called_once()
        return

    @patch(b'dyn.core.SessionEngine.execute')
    def test_mod_geo_create(self, mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        provider._mod_geo_rulesets = MagicMock()
        mock.side_effect = [
         self.traffic_director_response,
         self.traffic_directors_response]
        provider._mod_geo_Create(None, Create(self.geo_record))
        self.assertTrue(b'A' in provider.traffic_directors[b'unit.tests.'])
        provider._mod_geo_rulesets.assert_called_once()
        return

    def test_mod_geo_update_geo_geo(self):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        provider._traffic_directors = {b'unit.tests.': {b'A': 42}}
        provider._mod_geo_rulesets = MagicMock()
        geo = self.geo_record
        change = Update(geo, geo)
        provider._mod_geo_Update(None, change)
        self.assertTrue(b'A' in provider.traffic_directors[b'unit.tests.'])
        provider._mod_geo_rulesets.assert_called_once_with(42, change)
        return

    @patch(b'dyn.core.SessionEngine.execute')
    def test_mod_geo_update_geo_regular(self, _):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        provider._mod_Create = MagicMock()
        provider._mod_geo_Delete = MagicMock()
        change = Update(self.geo_record, self.regular_record)
        provider._mod_geo_Update(42, change)
        provider._mod_Create.assert_called_once_with(42, change)
        provider._mod_geo_Delete.assert_called_once_with(42, change)

    @patch(b'dyn.core.SessionEngine.execute')
    def test_mod_geo_update_regular_geo(self, _):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        provider._mod_geo_Create = MagicMock()
        provider._mod_Delete = MagicMock()
        change = Update(self.regular_record, self.geo_record)
        provider._mod_geo_Update(42, change)
        provider._mod_geo_Create.assert_called_once_with(42, change)
        provider._mod_Delete.assert_called_once_with(42, change)

    @patch(b'dyn.core.SessionEngine.execute')
    def test_mod_geo_delete(self, mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        td_mock = MagicMock()
        provider._traffic_directors = {b'unit.tests.': {b'A': td_mock}}
        provider._mod_geo_Delete(None, Delete(self.geo_record))
        td_mock.delete.assert_called_once()
        self.assertFalse(b'A' in provider.traffic_directors[b'unit.tests.'])
        return

    @patch(b'dyn.tm.services.DSFResponsePool.create')
    def test_find_or_create_geo_pool(self, mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        td = 42
        values = [
         b'1.2.3.4', b'1.2.3.5']
        pool = provider._find_or_create_geo_pool(td, [], b'default', b'A', values)
        self.assertIsInstance(pool, DSFResponsePool)
        self.assertEquals(1, len(pool.rs_chains))
        records = pool.rs_chains[0].record_sets[0].records
        self.assertEquals(values, [ r.address for r in records ])
        mock.assert_called_once_with(td)
        mock.reset_mock()
        pools = [pool]
        cached = provider._find_or_create_geo_pool(td, pools, b'default', b'A', values)
        self.assertEquals(pool, cached)
        mock.assert_not_called()
        mock.reset_mock()
        miss = provider._find_or_create_geo_pool(td, pools, b'NA-US-CA', b'A', values)
        self.assertNotEquals(pool, miss)
        self.assertEquals(b'NA-US-CA', miss.label)
        mock.assert_called_once_with(td)
        mock.reset_mock()
        values = [b'2.2.3.4.', b'2.2.3.5']
        miss = provider._find_or_create_geo_pool(td, pools, b'default', b'A', values)
        self.assertNotEquals(pool, miss)
        mock.assert_called_once_with(td)

    @patch(b'dyn.tm.services.DSFRuleset.add_response_pool')
    @patch(b'dyn.tm.services.DSFRuleset.create')
    @patch(b'dyn.tm.services.DSFResponsePool.create')
    def test_mod_geo_rulesets_create(self, _, ruleset_create_mock, add_response_pool_mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        td_mock = MagicMock()
        td_mock._rulesets = []
        provider._traffic_director_monitor = MagicMock()
        provider._find_or_create_geo_pool = MagicMock()
        td_mock.all_response_pools = []
        provider._find_or_create_geo_pool.side_effect = [
         _DummyPool(b'default'),
         _DummyPool(1),
         _DummyPool(2),
         _DummyPool(3),
         _DummyPool(4)]
        change = Create(self.geo_record)
        provider._mod_geo_rulesets(td_mock, change)
        ruleset_create_mock.assert_has_calls((
         call(td_mock, index=0),
         call(td_mock, index=0),
         call(td_mock, index=0),
         call(td_mock, index=0),
         call(td_mock, index=0)))
        add_response_pool_mock.assert_has_calls((
         call(b'default'),
         call(1),
         call(b'default', index=999),
         call(2),
         call(b'default', index=999),
         call(3),
         call(b'default', index=999),
         call(4),
         call(3, index=999),
         call(b'default', index=999)))

    @patch(b'octodns.provider.dyn.get_response_pool')
    @patch(b'dyn.tm.services.DSFRuleset.add_response_pool')
    @patch(b'dyn.tm.services.DSFRuleset.create')
    @patch(b'dyn.tm.services.DSFResponsePool.create')
    def test_mod_geo_rulesets_existing(self, _, ruleset_create_mock, add_response_pool_mock, get_response_pool_mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        ruleset_mock = MagicMock()
        ruleset_mock.response_pools = [_DummyPool(3)]
        td_mock = MagicMock()
        td_mock._rulesets = [
         ruleset_mock]
        provider._traffic_director_monitor = MagicMock()
        provider._find_or_create_geo_pool = MagicMock()
        unused_pool = _DummyPool(b'unused')
        td_mock.all_response_pools = ruleset_mock.response_pools + [unused_pool]
        get_response_pool_mock.return_value = unused_pool
        provider._find_or_create_geo_pool.side_effect = [
         _DummyPool(b'default'),
         _DummyPool(1),
         _DummyPool(2),
         ruleset_mock.response_pools[0],
         _DummyPool(4)]
        change = Create(self.geo_record)
        provider._mod_geo_rulesets(td_mock, change)
        ruleset_create_mock.assert_has_calls((
         call(td_mock, index=2),
         call(td_mock, index=2),
         call(td_mock, index=2),
         call(td_mock, index=2),
         call(td_mock, index=2)))
        add_response_pool_mock.assert_has_calls((
         call(b'default'),
         call(1),
         call(b'default', index=999),
         call(2),
         call(b'default', index=999),
         call(3),
         call(b'default', index=999),
         call(4),
         call(3, index=999),
         call(b'default', index=999)))
        self.assertTrue(unused_pool.deleted)
        ruleset_mock.delete.assert_called_once()


class TestDynProviderAlias(TestCase):
    expected = Zone(b'unit.tests.', [])
    for name, data in (
     (
      b'',
      {b'type': b'ALIAS', 
         b'ttl': 300, 
         b'value': b'www.unit.tests.'}),
     (
      b'www',
      {b'type': b'A', 
         b'ttl': 300, 
         b'values': [
                   b'1.2.3.4']})):
        expected.add_record(Record.new(expected, name, data))

    def setUp(self):
        _CachingDynZone.flush_zone(self.expected.name[:-1])

    @patch(b'dyn.core.SessionEngine.execute')
    def test_populate(self, execute_mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass')
        execute_mock.side_effect = [{b'data': {}},
         {b'data': {b'a_records': [
                                   {b'fqdn': b'www.unit.tests', 
                                      b'rdata': {b'address': b'1.2.3.4'}, b'record_id': 1, 
                                      b'record_type': b'A', 
                                      b'ttl': 300, 
                                      b'zone': b'unit.tests'}], 
                      b'alias_records': [
                                       {b'fqdn': b'unit.tests', 
                                          b'rdata': {b'alias': b'www.unit.tests.'}, b'record_id': 2, 
                                          b'record_type': b'ALIAS', 
                                          b'ttl': 300, 
                                          b'zone': b'unit.tests'}]}}]
        got = Zone(b'unit.tests.', [])
        provider.populate(got)
        execute_mock.assert_has_calls([
         call(b'/Zone/unit.tests/', b'GET', {}),
         call(b'/AllRecord/unit.tests/unit.tests./', b'GET', {b'detail': b'Y'})])
        changes = self.expected.changes(got, SimpleProvider())
        self.assertEquals([], changes)

    @patch(b'dyn.core.SessionEngine.execute')
    def test_sync(self, execute_mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass')
        execute_mock.side_effect = [
         DynectGetError(b'foo'),
         DynectGetError(b'foo'), {b'data': {}},
         {b'data': {b'a_records': [
                                   {b'fqdn': b'www.unit.tests', 
                                      b'rdata': {b'address': b'1.2.3.4'}, b'record_id': 1, 
                                      b'record_type': b'A', 
                                      b'ttl': 300, 
                                      b'zone': b'unit.tests'}], 
                      b'alias_records': [
                                       {b'fqdn': b'unit.tests', 
                                          b'rdata': {b'alias': b'www.unit.tests.'}, b'record_id': 2, 
                                          b'record_type': b'ALIAS', 
                                          b'ttl': 300, 
                                          b'zone': b'unit.tests'}]}}]
        with patch(b'dyn.tm.zones.Zone.add_record') as (add_mock):
            with patch(b'dyn.tm.zones.Zone._update') as (update_mock):
                plan = provider.plan(self.expected)
                update_mock.assert_not_called()
                provider.apply(plan)
                update_mock.assert_called()
            add_mock.assert_called()
            self.assertEquals(2, len(add_mock.call_args_list))
        execute_mock.assert_has_calls([call(b'/Zone/unit.tests/', b'GET', {}),
         call(b'/Zone/unit.tests/', b'GET', {})])
        self.assertEquals(2, len(plan.changes))


class DummyDSFMonitor(DSFMonitor):

    def __init__(self, host=None, path=None, protocol=None, port=None, options_host=None, options_path=None, options_protocol=None, options_port=None):
        self._host = host
        self._path = path
        self._protocol = protocol
        self._port = port
        if options_host:
            self._options = {b'host': options_host, b'path': options_path, 
               b'protocol': options_protocol, 
               b'port': options_port}
        else:
            self._options = None
        return


class TestDSFMonitorMonkeyPatching(TestCase):

    def test_host(self):
        monitor = DummyDSFMonitor(host=b'host.com', path=b'/path', protocol=b'HTTP', port=8080)
        self.assertEquals(b'host.com', monitor.host)
        self.assertEquals(b'/path', monitor.path)
        self.assertEquals(b'HTTP', monitor.protocol)
        self.assertEquals(8080, monitor.port)
        monitor = DummyDSFMonitor(options_host=b'host.com', options_path=b'/path', options_protocol=b'HTTP', options_port=8080)
        self.assertEquals(b'host.com', monitor.host)
        self.assertEquals(b'/path', monitor.path)
        monitor.host = b'other.com'
        self.assertEquals(b'other.com', monitor.host)
        monitor.path = b'/other-path'
        self.assertEquals(b'/other-path', monitor.path)
        monitor.protocol = b'HTTPS'
        self.assertEquals(b'HTTPS', monitor.protocol)
        monitor.port = 8081
        self.assertEquals(8081, monitor.port)
        monitor = DummyDSFMonitor()
        monitor.host = b'other.com'
        self.assertEquals(b'other.com', monitor.host)
        monitor = DummyDSFMonitor()
        monitor.path = b'/other-path'
        self.assertEquals(b'/other-path', monitor.path)
        monitor.protocol = b'HTTP'
        self.assertEquals(b'HTTP', monitor.protocol)
        monitor.port = 8080
        self.assertEquals(8080, monitor.port)
        monitor = DummyDSFMonitor()
        monitor.protocol = b'HTTP'
        self.assertEquals(b'HTTP', monitor.protocol)
        monitor = DummyDSFMonitor()
        monitor.port = 8080
        self.assertEquals(8080, monitor.port)


class DummyRecord(object):

    def __init__(self, address, weight, ttl):
        self.address = address
        self.weight = weight
        self.ttl = ttl


class DummyRecordSets(object):

    def __init__(self, records):
        self.records = records


class DummyRsChains(object):

    def __init__(self, records):
        self.record_sets = [
         DummyRecordSets(records)]


class DummyResponsePool(object):

    def __init__(self, label, records=[]):
        self.label = label
        if records:
            self.rs_chains = [
             DummyRsChains(records)]
        else:
            self.rs_chains = []

    def refresh(self):
        pass


class DummyRuleset(object):

    def __init__(self, label, response_pools=[], criteria_type=b'always', criteria={}):
        self.label = label
        self.response_pools = response_pools
        self.criteria_type = criteria_type
        self.criteria = criteria


class DummyTrafficDirector(object):

    def __init__(self, zone_name, rulesets=[], response_pools=[], ttl=42):
        self.label = b'dummy:abcdef1234567890'
        self.rulesets = rulesets
        self.all_response_pools = response_pools
        self.ttl = ttl
        self.nodes = [{b'zone': zone_name[:-1]}]


class TestDynProviderDynamic(TestCase):

    def test_value_for_address(self):
        provider = DynProvider(b'test', b'cust', b'user', b'pass')

        class DummyRecord(object):

            def __init__(self, address, weight):
                self.address = address
                self.weight = weight

        record = DummyRecord(b'1.2.3.4', 32)
        self.assertEquals({b'value': record.address, 
           b'weight': record.weight}, provider._value_for_A(b'A', record))
        record = DummyRecord(b'2601:644:500:e210:62f8:1dff:feb8:947a', 32)
        self.assertEquals({b'value': record.address, 
           b'weight': record.weight}, provider._value_for_AAAA(b'AAAA', record))

    def test_value_for_CNAME(self):
        provider = DynProvider(b'test', b'cust', b'user', b'pass')

        class DummyRecord(object):

            def __init__(self, cname, weight):
                self.cname = cname
                self.weight = weight

        record = DummyRecord(b'foo.unit.tests.', 32)
        self.assertEquals({b'value': record.cname, 
           b'weight': record.weight}, provider._value_for_CNAME(b'CNAME', record))

    def test_populate_dynamic_pools(self):
        provider = DynProvider(b'test', b'cust', b'user', b'pass')
        default, pools = provider._populate_dynamic_pools(b'A', [], [])
        self.assertEquals({}, default)
        self.assertEquals({}, pools)
        records_a = [
         DummyRecord(b'1.2.3.4', 32, 60)]
        default_a = DummyResponsePool(b'default', records_a)
        response_pools = [
         default_a]
        default, pools = provider._populate_dynamic_pools(b'A', [], response_pools)
        self.assertEquals({b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.2.3.4']}, default)
        self.assertEquals({}, pools)
        multi_a = [
         DummyRecord(b'1.2.3.5', 42, 90),
         DummyRecord(b'1.2.3.6', 43, 90),
         DummyRecord(b'1.2.3.7', 44, 90)]
        example_a = DummyResponsePool(b'example', multi_a)
        response_pools = [
         example_a]
        default, pools = provider._populate_dynamic_pools(b'A', [], response_pools)
        self.assertEquals({}, default)
        self.assertEquals({b'example': {b'values': [
                                  {b'value': b'1.2.3.5', 
                                     b'weight': 42},
                                  {b'value': b'1.2.3.6', 
                                     b'weight': 43},
                                  {b'value': b'1.2.3.7', 
                                     b'weight': 44}]}}, pools)
        response_pools = [
         example_a, example_a]
        default, pools = provider._populate_dynamic_pools(b'A', [], response_pools)
        self.assertEquals({}, default)
        self.assertEquals({b'example': {b'values': [
                                  {b'value': b'1.2.3.5', 
                                     b'weight': 42},
                                  {b'value': b'1.2.3.6', 
                                     b'weight': 43},
                                  {b'value': b'1.2.3.7', 
                                     b'weight': 44}]}}, pools)
        response_pools = [
         example_a, default_a, example_a]
        default, pools = provider._populate_dynamic_pools(b'A', [], response_pools)
        self.assertEquals({b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.2.3.4']}, default)
        self.assertEquals({b'example': {b'values': [
                                  {b'value': b'1.2.3.5', 
                                     b'weight': 42},
                                  {b'value': b'1.2.3.6', 
                                     b'weight': 43},
                                  {b'value': b'1.2.3.7', 
                                     b'weight': 44}]}}, pools)
        empty_a = DummyResponsePool(b'empty')
        response_pools = [empty_a]
        default, pools = provider._populate_dynamic_pools(b'A', [], response_pools)
        self.assertEquals({}, default)
        self.assertEquals({}, pools)

    def test_populate_dynamic_rules(self):
        provider = DynProvider(b'test', b'cust', b'user', b'pass')
        rulesets = []
        pools = {}
        rules = provider._populate_dynamic_rules(rulesets, pools)
        self.assertEquals([], rules)
        rulesets = [
         DummyRuleset(b'default:')]
        pools = {}
        rules = provider._populate_dynamic_rules(rulesets, pools)
        self.assertEquals([], rules)
        rulesets = [
         DummyRuleset(b'0:abcdefg')]
        pools = {}
        rules = provider._populate_dynamic_rules(rulesets, pools)
        self.assertEquals([], rules)
        rulesets = [
         DummyRuleset(b'0:abcdefg', [
          DummyResponsePool(b'some-pool')])]
        pools = {}
        rules = provider._populate_dynamic_rules(rulesets, pools)
        self.assertEquals([
         {b'pool': b'some-pool'}], rules)
        rulesets = [
         DummyRuleset(b'0:abcdefg', [
          DummyResponsePool(b'some-pool'),
          DummyResponsePool(b'default')])]
        pools = {}
        rules = provider._populate_dynamic_rules(rulesets, pools)
        self.assertEquals([
         {b'pool': b'some-pool'}], rules)
        rulesets = [
         DummyRuleset(b'0:abcdefg', [
          DummyResponsePool(b'some-pool'),
          DummyResponsePool(b'some-fallback')])]
        pools = {b'some-pool': {}}
        rules = provider._populate_dynamic_rules(rulesets, pools)
        self.assertEquals([
         {b'pool': b'some-pool'}], rules)
        self.assertEquals({b'some-pool': {b'fallback': b'some-fallback'}}, pools)
        rulesets = [
         DummyRuleset(b'0:abcdefg', [
          DummyResponsePool(b'some-pool')], b'unsupported')]
        pools = {}
        rules = provider._populate_dynamic_rules(rulesets, pools)
        self.assertEquals([], rules)
        response_pools = [
         DummyResponsePool(b'some-pool')]
        criteria = {b'geoip': {b'country': [
                                 b'US'], 
                      b'province': [
                                  b'or'], 
                      b'region': [
                                14]}}
        ruleset = DummyRuleset(b'0:abcdefg', response_pools, b'geoip', criteria)
        rulesets = [ruleset]
        pools = {}
        rules = provider._populate_dynamic_rules(rulesets, pools)
        self.assertEquals([
         {b'geos': [
                    b'AF', b'NA-US', b'NA-US-OR'], 
            b'pool': b'some-pool'}], rules)

    def test_populate_dynamic_traffic_director(self):
        provider = DynProvider(b'test', b'cust', b'user', b'pass')
        fqdn = b'dynamic.unit.tests.'
        multi_a = [
         DummyRecord(b'1.2.3.5', 1, 90),
         DummyRecord(b'1.2.3.6', 1, 90),
         DummyRecord(b'1.2.3.7', 1, 90)]
        default_response_pool = DummyResponsePool(b'default', multi_a)
        pool1_response_pool = DummyResponsePool(b'pool1', multi_a)
        rulesets = [
         DummyRuleset(b'default', [default_response_pool]),
         DummyRuleset(b'0:abcdef', [pool1_response_pool], b'geoip', {b'geoip': {b'country': [
                                  b'US'], 
                       b'province': [
                                   b'or'], 
                       b'region': [
                                 14]}})]
        zone = Zone(b'unit.tests.', [])
        td = DummyTrafficDirector(zone.name, rulesets, [
         default_response_pool, pool1_response_pool])
        record = provider._populate_dynamic_traffic_director(zone, fqdn, b'A', td, rulesets, True)
        self.assertTrue(record)
        self.assertEquals(b'A', record._type)
        self.assertEquals(90, record.ttl)
        self.assertEquals([
         b'1.2.3.5',
         b'1.2.3.6',
         b'1.2.3.7'], record.values)
        self.assertTrue(b'pool1' in record.dynamic.pools)
        self.assertEquals({b'fallback': None, 
           b'values': [
                     {b'value': b'1.2.3.5', 
                        b'weight': 1},
                     {b'value': b'1.2.3.6', 
                        b'weight': 1},
                     {b'value': b'1.2.3.7', 
                        b'weight': 1}]}, record.dynamic.pools[b'pool1'].data)
        self.assertEquals(2, len(record.dynamic.rules))
        self.assertEquals({b'pool': b'default'}, record.dynamic.rules[0].data)
        self.assertEquals({b'pool': b'pool1', 
           b'geos': [
                   b'AF', b'NA-US', b'NA-US-OR']}, record.dynamic.rules[1].data)
        provider._traffic_directors = {b'dynamic.unit.tests.': {b'A': td}}
        zone = Zone(b'unit.tests.', [])
        records = provider._populate_traffic_directors(zone, lenient=True)
        self.assertEquals(1, len(records))
        return

    def test_dynamic_records_for_A(self):
        provider = DynProvider(b'test', b'cust', b'user', b'pass')
        records = provider._dynamic_records_for_A([], {})
        self.assertEquals([], records)
        values = [
         {b'value': b'1.2.3.4'},
         {b'value': b'1.2.3.5', 
            b'weight': 42}]
        records = provider._dynamic_records_for_A(values, {})
        self.assertEquals(2, len(records))
        record = records[0]
        self.assertEquals(b'1.2.3.4', record.address)
        self.assertEquals(1, record.weight)
        record = records[1]
        self.assertEquals(b'1.2.3.5', record.address)
        self.assertEquals(42, record.weight)
        records = provider._dynamic_records_for_A(values, {b'automation': b'manual', 
           b'eligible': True})
        self.assertEquals(2, len(records))
        record = records[0]
        self.assertEquals(b'1.2.3.4', record.address)
        self.assertEquals(1, record.weight)
        self.assertEquals(b'manual', record._automation)
        self.assertTrue(record.eligible)

    def test_dynamic_records_for_AAAA(self):
        provider = DynProvider(b'test', b'cust', b'user', b'pass')
        records = provider._dynamic_records_for_AAAA([], {})
        self.assertEquals([], records)
        values = [
         {b'value': b'2601:644:500:e210:62f8:1dff:feb8:947a'},
         {b'value': b'2601:644:500:e210:62f8:1dff:feb8:947b', 
            b'weight': 42}]
        records = provider._dynamic_records_for_AAAA(values, {})
        self.assertEquals(2, len(records))
        record = records[0]
        self.assertEquals(b'2601:644:500:e210:62f8:1dff:feb8:947a', record.address)
        self.assertEquals(1, record.weight)
        record = records[1]
        self.assertEquals(b'2601:644:500:e210:62f8:1dff:feb8:947b', record.address)
        self.assertEquals(42, record.weight)
        records = provider._dynamic_records_for_AAAA(values, {b'automation': b'manual', 
           b'eligible': True})
        self.assertEquals(2, len(records))
        record = records[0]
        self.assertEquals(b'2601:644:500:e210:62f8:1dff:feb8:947a', record.address)
        self.assertEquals(1, record.weight)
        self.assertEquals(b'manual', record._automation)
        self.assertTrue(record.eligible)

    def test_dynamic_records_for_CNAME(self):
        provider = DynProvider(b'test', b'cust', b'user', b'pass')
        records = provider._dynamic_records_for_CNAME([], {})
        self.assertEquals([], records)
        values = [
         {b'value': b'target-1.unit.tests.'},
         {b'value': b'target-2.unit.tests.', 
            b'weight': 42}]
        records = provider._dynamic_records_for_CNAME(values, {})
        self.assertEquals(2, len(records))
        record = records[0]
        self.assertEquals(b'target-1.unit.tests.', record.cname)
        self.assertEquals(1, record.weight)
        record = records[1]
        self.assertEquals(b'target-2.unit.tests.', record.cname)
        self.assertEquals(42, record.weight)
        records = provider._dynamic_records_for_CNAME(values, {b'automation': b'manual', 
           b'eligible': True})
        self.assertEquals(2, len(records))
        record = records[0]
        self.assertEquals(b'target-1.unit.tests.', record.cname)
        self.assertEquals(1, record.weight)
        self.assertEquals(b'manual', record._automation)
        self.assertTrue(record.eligible)

    def test_dynamic_value_sort_key(self):
        values = [
         {b'value': b'1.2.3.1'},
         {b'value': b'1.2.3.27'},
         {b'value': b'1.2.3.127'},
         {b'value': b'1.2.3.2'}]
        self.assertEquals([
         {b'value': b'1.2.3.1'},
         {b'value': b'1.2.3.127'},
         {b'value': b'1.2.3.2'},
         {b'value': b'1.2.3.27'}], sorted(values, key=_dynamic_value_sort_key))

    @patch(b'dyn.tm.services.DSFResponsePool.create')
    def test_find_or_create_dynamic_pools(self, mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass')
        td = 42
        label = b'foo'
        values = [
         {b'value': b'1.2.3.1'},
         {b'value': b'1.2.3.127'},
         {b'value': b'1.2.3.2'},
         {b'value': b'1.2.3.27'}]
        pools = []
        pool = provider._find_or_create_dynamic_pool(td, pools, label, b'A', values)
        self.assertIsInstance(pool, DSFResponsePool)
        self.assertEquals(1, len(pool.rs_chains))
        self.assertEquals(1, len(pool.rs_chains[0].record_sets))
        records = pool.rs_chains[0].record_sets[0].records
        self.assertEquals(4, len(records))
        self.assertEquals([ v[b'value'] for v in values ], [ r.address for r in records ])
        self.assertEquals([ 1 for r in records ], [ r.weight for r in records ])
        mock.assert_called_once_with(td)
        mock.reset_mock()
        pools = [pool]
        cached = provider._find_or_create_dynamic_pool(td, pools, label, b'A', values)
        self.assertEquals(pool, cached)
        mock.assert_not_called()
        mock.reset_mock()
        invalid = DSFResponsePool(label, rs_chains=[])
        pools = [invalid, pool]
        cached = provider._find_or_create_dynamic_pool(td, pools, label, b'A', values)
        self.assertEquals(pool, cached)
        mock.assert_not_called()
        mock.reset_mock()
        pools = [pool]
        other = provider._find_or_create_dynamic_pool(td, pools, b'other', b'A', values)
        self.assertEquals(b'other', other.label)
        mock.assert_called_once_with(td)
        values = [
         {b'value': b'1.2.3.44'}]
        mock.reset_mock()
        pools = [pool]
        new = provider._find_or_create_dynamic_pool(td, pools, label, b'A', values)
        self.assertEquals(label, new.label)
        self.assertEquals(1, len(new.rs_chains))
        self.assertEquals(1, len(new.rs_chains[0].record_sets))
        records = new.rs_chains[0].record_sets[0].records
        self.assertEquals(1, len(records))
        self.assertEquals([ v[b'value'] for v in values ], [ r.address for r in records ])
        self.assertEquals([ 1 for r in records ], [ r.weight for r in records ])
        mock.assert_called_once_with(td)

    zone = Zone(b'unit.tests.', [])
    dynamic_a_record = Record.new(zone, b'', {b'dynamic': {b'pools': {b'one': {b'values': [
                                                  {b'value': b'3.3.3.3'}]}, 
                               b'two': {b'values': [
                                                  {b'value': b'5.5.5.5'},
                                                  {b'value': b'4.4.4.4'}]}, 
                               b'three': {b'fallback': b'two', 
                                          b'values': [
                                                    {b'weight': 10, 
                                                       b'value': b'4.4.4.4'},
                                                    {b'weight': 12, 
                                                       b'value': b'5.5.5.5'}]}}, 
                    b'rules': [
                             {b'geos': [
                                        b'AF', b'EU', b'AS-JP'], 
                                b'pool': b'three'},
                             {b'geos': [
                                        b'NA-US-CA'], 
                                b'pool': b'two'},
                             {b'pool': b'one'}]}, 
       b'type': b'A', 
       b'ttl': 60, 
       b'values': [
                 b'1.1.1.1',
                 b'2.2.2.2']})
    geo_a_record = Record.new(zone, b'', {b'geo': {b'AF': [
                      b'2.2.3.4', b'2.2.3.5'], 
                b'AS-JP': [
                         b'3.2.3.4', b'3.2.3.5'], 
                b'NA-US': [
                         b'4.2.3.4', b'4.2.3.5'], 
                b'NA-US-CA': [
                            b'5.2.3.4', b'5.2.3.5']}, 
       b'ttl': 300, 
       b'type': b'A', 
       b'values': [
                 b'1.2.3.4', b'1.2.3.5']})
    regular_a_record = Record.new(zone, b'', {b'ttl': 301, 
       b'type': b'A', 
       b'value': b'1.2.3.4'})
    dynamic_cname_record = Record.new(zone, b'www', {b'dynamic': {b'pools': {b'one': {b'values': [
                                                  {b'value': b'target-0.unit.tests.'}]}, 
                               b'two': {b'values': [
                                                  {b'value': b'target-1.unit.tests.'},
                                                  {b'value': b'target-2.unit.tests.'}]}, 
                               b'three': {b'values': [
                                                    {b'weight': 10, 
                                                       b'value': b'target-3.unit.tests.'},
                                                    {b'weight': 12, 
                                                       b'value': b'target-4.unit.tests.'}]}}, 
                    b'rules': [
                             {b'geos': [
                                        b'AF', b'EU', b'AS-JP'], 
                                b'pool': b'three'},
                             {b'geos': [
                                        b'NA-US-CA'], 
                                b'pool': b'two'},
                             {b'pool': b'one'}]}, 
       b'type': b'CNAME', 
       b'ttl': 60, 
       b'value': b'target.unit.tests.'})
    dynamic_fallback_loop = Record.new(zone, b'', {b'dynamic': {b'pools': {b'one': {b'values': [
                                                  {b'value': b'3.3.3.3'}]}, 
                               b'two': {b'fallback': b'three', 
                                        b'values': [
                                                  {b'value': b'5.5.5.5'},
                                                  {b'value': b'4.4.4.4'}]}, 
                               b'three': {b'fallback': b'two', 
                                          b'values': [
                                                    {b'weight': 10, 
                                                       b'value': b'4.4.4.4'},
                                                    {b'weight': 12, 
                                                       b'value': b'5.5.5.5'}]}}, 
                    b'rules': [
                             {b'geos': [
                                        b'AF', b'EU', b'AS-JP'], 
                                b'pool': b'three'},
                             {b'geos': [
                                        b'NA-US-CA'], 
                                b'pool': b'two'},
                             {b'pool': b'one'}]}, 
       b'type': b'A', 
       b'ttl': 60, 
       b'values': [
                 b'1.1.1.1',
                 b'2.2.2.2']}, lenient=True)

    @patch(b'dyn.tm.services.DSFRuleset.add_response_pool')
    @patch(b'dyn.tm.services.DSFRuleset.create')
    @patch(b'dyn.tm.services.DSFResponsePool.create')
    def test_mod_dynamic_rulesets_create_CNAME(self, _, ruleset_create_mock, add_response_pool_mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        td_mock = MagicMock()
        td_mock._rulesets = []
        provider._traffic_director_monitor = MagicMock()
        provider._find_or_create_dynamic_pool = MagicMock()
        td_mock.all_response_pools = []
        provider._find_or_create_dynamic_pool.side_effect = [
         _DummyPool(b'default'),
         _DummyPool(b'one'),
         _DummyPool(b'two'),
         _DummyPool(b'three')]
        change = Create(self.dynamic_cname_record)
        provider._mod_dynamic_rulesets(td_mock, change)
        add_response_pool_mock.assert_has_calls((
         call(b'default'),
         call(b'one'),
         call(b'default', index=999),
         call(b'three'),
         call(b'default', index=999),
         call(b'two'),
         call(b'default', index=999)))
        ruleset_create_mock.assert_has_calls((
         call(td_mock, index=0),
         call(td_mock, index=0),
         call(td_mock, index=0),
         call(td_mock, index=0)))

    @patch(b'octodns.provider.dyn.get_response_pool')
    @patch(b'dyn.tm.services.DSFRuleset.add_response_pool')
    @patch(b'dyn.tm.services.DSFRuleset.create')
    @patch(b'dyn.tm.services.DSFResponsePool.create')
    def test_mod_dynamic_rulesets_existing(self, _, ruleset_create_mock, add_response_pool_mock, get_response_pool_mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        ruleset_mock = MagicMock()
        ruleset_mock.response_pools = [_DummyPool(b'three')]
        td_mock = MagicMock()
        td_mock._rulesets = [
         ruleset_mock]
        provider._traffic_director_monitor = MagicMock()
        provider._find_or_create_dynamic_pool = MagicMock()
        td_mock.ttl = self.dynamic_a_record.ttl
        unused_pool = _DummyPool(b'unused')
        td_mock.all_response_pools = ruleset_mock.response_pools + [unused_pool]
        get_response_pool_mock.return_value = unused_pool
        provider._find_or_create_dynamic_pool.side_effect = [
         _DummyPool(b'default'),
         _DummyPool(b'one'),
         _DummyPool(b'two'),
         ruleset_mock.response_pools[0]]
        change = Create(self.dynamic_a_record)
        provider._mod_dynamic_rulesets(td_mock, change)
        add_response_pool_mock.assert_has_calls((
         call(b'default'),
         call(b'one'),
         call(b'default', index=999),
         call(b'three'),
         call(b'default', index=999),
         call(b'two'),
         call(b'three', index=999),
         call(b'default', index=999)))
        ruleset_create_mock.assert_has_calls((
         call(td_mock, index=2),
         call(td_mock, index=2),
         call(td_mock, index=2),
         call(td_mock, index=2)))
        self.assertTrue(unused_pool.deleted)
        ruleset_mock.delete.assert_called_once()

    @patch(b'octodns.provider.dyn.get_response_pool')
    @patch(b'dyn.tm.services.DSFRuleset.add_response_pool')
    @patch(b'dyn.tm.services.DSFRuleset.create')
    @patch(b'dyn.tm.services.DSFResponsePool.create')
    def test_mod_dynamic_rulesets_fallback_loop(self, _, ruleset_create_mock, add_response_pool_mock, get_response_pool_mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        ruleset_mock = MagicMock()
        ruleset_mock.response_pools = [_DummyPool(b'three')]
        td_mock = MagicMock()
        td_mock._rulesets = [
         ruleset_mock]
        provider._traffic_director_monitor = MagicMock()
        provider._find_or_create_dynamic_pool = MagicMock()
        td_mock.ttl = self.dynamic_fallback_loop.ttl
        unused_pool = _DummyPool(b'unused')
        td_mock.all_response_pools = ruleset_mock.response_pools + [unused_pool]
        get_response_pool_mock.return_value = unused_pool
        provider._find_or_create_dynamic_pool.side_effect = [
         _DummyPool(b'default'),
         _DummyPool(b'one'),
         _DummyPool(b'two'),
         ruleset_mock.response_pools[0]]
        change = Create(self.dynamic_fallback_loop)
        provider._mod_dynamic_rulesets(td_mock, change)
        add_response_pool_mock.assert_has_calls((
         call(b'default'),
         call(b'one'),
         call(b'default', index=999),
         call(b'three'),
         call(b'two', index=999),
         call(b'default', index=999),
         call(b'two'),
         call(b'three', index=999),
         call(b'default', index=999)))
        ruleset_create_mock.assert_has_calls((
         call(td_mock, index=2),
         call(td_mock, index=2),
         call(td_mock, index=2),
         call(td_mock, index=2)))
        self.assertTrue(unused_pool.deleted)
        ruleset_mock.delete.assert_called_once()

    with open(b'./tests/fixtures/dyn-traffic-director-get.json') as (fh):
        traffic_director_response = loads(fh.read())

    @property
    def traffic_directors_response(self):
        return {b'data': [
                   {b'active': b'Y', 
                      b'label': b'unit.tests.:A', 
                      b'nodes': [], b'notifiers': [], b'pending_change': b'', 
                      b'rulesets': [], b'service_id': b'2ERWXQNsb_IKG2YZgYqkPvk0PBM', 
                      b'ttl': b'300'},
                   {b'active': b'Y', 
                      b'label': b'some.other.:A', 
                      b'nodes': [], b'notifiers': [], b'pending_change': b'', 
                      b'rulesets': [], b'service_id': b'3ERWXQNsb_IKG2YZgYqkPvk0PBM', 
                      b'ttl': b'300'},
                   {b'active': b'Y', 
                      b'label': b'other format', 
                      b'nodes': [], b'notifiers': [], b'pending_change': b'', 
                      b'rulesets': [], b'service_id': b'4ERWXQNsb_IKG2YZgYqkPvk0PBM', 
                      b'ttl': b'300'}]}

    @patch(b'dyn.core.SessionEngine.execute')
    def test_mod_dynamic_create(self, mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        provider._mod_dynamic_rulesets = MagicMock()
        mock.side_effect = [
         self.traffic_director_response,
         self.traffic_directors_response]
        provider._mod_dynamic_Create(None, Create(self.dynamic_a_record))
        self.assertTrue(b'A' in provider.traffic_directors[b'unit.tests.'])
        provider._mod_dynamic_rulesets.assert_called_once()
        return

    def test_mod_dynamic_update_dynamic_dynamic(self):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        provider._traffic_directors = {b'unit.tests.': {b'A': 42}}
        provider._mod_dynamic_rulesets = MagicMock()
        dyn = self.dynamic_a_record
        change = Update(dyn, dyn)
        provider._mod_dynamic_Update(None, change)
        self.assertTrue(b'A' in provider.traffic_directors[b'unit.tests.'])
        provider._mod_dynamic_rulesets.assert_called_once_with(42, change)
        return

    @patch(b'dyn.core.SessionEngine.execute')
    def test_mod_dynamic_update_dynamic_geo(self, _):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        provider._mod_geo_Update = MagicMock()
        change = Update(self.dynamic_a_record, self.geo_a_record)
        provider._mod_dynamic_Update(42, change)
        provider._mod_geo_Update.assert_called_once_with(42, change)

    @patch(b'dyn.core.SessionEngine.execute')
    def test_mod_dynamic_update_dynamic_regular(self, _):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        provider._mod_Create = MagicMock()
        provider._mod_dynamic_Delete = MagicMock()
        change = Update(self.dynamic_a_record, self.regular_a_record)
        provider._mod_dynamic_Update(42, change)
        provider._mod_Create.assert_called_once_with(42, change)
        provider._mod_dynamic_Delete.assert_called_once_with(42, change)

    @patch(b'dyn.core.SessionEngine.execute')
    def test_mod_dynamic_update_geo_dynamic(self, _):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        provider._traffic_directors = {b'unit.tests.': {b'A': 42}}
        provider._mod_dynamic_rulesets = MagicMock()
        change = Update(self.geo_a_record, self.dynamic_a_record)
        provider._mod_dynamic_Update(None, change)
        self.assertTrue(b'A' in provider.traffic_directors[b'unit.tests.'])
        provider._mod_dynamic_rulesets.assert_called_once_with(42, change)
        return

    @patch(b'dyn.core.SessionEngine.execute')
    def test_mod_dynamic_update_regular_dynamic(self, _):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        provider._mod_dynamic_Create = MagicMock()
        provider._mod_Delete = MagicMock()
        change = Update(self.regular_a_record, self.dynamic_a_record)
        provider._mod_dynamic_Update(42, change)
        provider._mod_dynamic_Create.assert_called_once_with(42, change)
        provider._mod_Delete.assert_called_once_with(42, change)

    @patch(b'dyn.core.SessionEngine.execute')
    def test_mod_dynamic_delete(self, mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        td_mock = MagicMock()
        provider._traffic_directors = {b'unit.tests.': {b'A': td_mock}}
        provider._mod_dynamic_Delete(None, Delete(self.dynamic_a_record))
        td_mock.delete.assert_called_once()
        self.assertFalse(b'A' in provider.traffic_directors[b'unit.tests.'])
        return

    @patch(b'dyn.core.SessionEngine.execute')
    def test_apply_traffic_directors_dynamic(self, mock):
        provider = DynProvider(b'test', b'cust', b'user', b'pass', traffic_directors_enabled=True)
        provider._mod_dynamic_Create = MagicMock()
        changes = [
         Create(self.dynamic_a_record)]
        provider._apply_traffic_directors(self.zone, changes, None)
        provider._mod_dynamic_Create.assert_called_once()
        return