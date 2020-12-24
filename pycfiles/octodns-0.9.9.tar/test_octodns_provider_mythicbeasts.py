# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_mythicbeasts.py
# Compiled at: 2019-10-18 13:06:59
from __future__ import absolute_import, division, print_function, unicode_literals
from os.path import dirname, join
from requests_mock import ANY, mock as requests_mock
from six import text_type
from unittest import TestCase
from octodns.provider.mythicbeasts import MythicBeastsProvider, add_trailing_dot, remove_trailing_dot
from octodns.provider.yaml import YamlProvider
from octodns.zone import Zone
from octodns.record import Create, Update, Delete, Record

class TestMythicBeastsProvider(TestCase):
    expected = Zone(b'unit.tests.', [])
    source = YamlProvider(b'test_expected', join(dirname(__file__), b'config'))
    source.populate(expected)
    for record in list(expected.records):
        if record._type not in MythicBeastsProvider.SUPPORTS:
            expected._remove_record(record)

    def test_trailing_dot(self):
        with self.assertRaises(AssertionError) as (err):
            add_trailing_dot(b'unit.tests.')
        self.assertEquals(b'Value already has trailing dot', text_type(err.exception))
        with self.assertRaises(AssertionError) as (err):
            remove_trailing_dot(b'unit.tests')
        self.assertEquals(b'Value already missing trailing dot', text_type(err.exception))
        self.assertEquals(add_trailing_dot(b'unit.tests'), b'unit.tests.')
        self.assertEquals(remove_trailing_dot(b'unit.tests.'), b'unit.tests')

    def test_data_for_single(self):
        test_data = {b'raw_values': [{b'value': b'a:a::c', b'ttl': 0}], b'zone': b'unit.tests.'}
        test_single = MythicBeastsProvider._data_for_single(b'', test_data)
        self.assertTrue(isinstance(test_single, dict))
        self.assertEquals(b'a:a::c', test_single[b'value'])

    def test_data_for_multiple(self):
        test_data = {b'raw_values': [{b'value': b'b:b::d', b'ttl': 60}, {b'value': b'a:a::c', b'ttl': 60}], b'zone': b'unit.tests.'}
        test_multiple = MythicBeastsProvider._data_for_multiple(b'', test_data)
        self.assertTrue(isinstance(test_multiple, dict))
        self.assertEquals(2, len(test_multiple[b'values']))

    def test_data_for_txt(self):
        test_data = {b'raw_values': [{b'value': b'v=DKIM1; k=rsa; p=prawf', b'ttl': 60}, {b'value': b'prawf prawf dyma prawf', b'ttl': 300}], b'zone': b'unit.tests.'}
        test_txt = MythicBeastsProvider._data_for_TXT(b'', test_data)
        self.assertTrue(isinstance(test_txt, dict))
        self.assertEquals(2, len(test_txt[b'values']))
        self.assertEquals(b'v=DKIM1\\; k=rsa\\; p=prawf', test_txt[b'values'][0])

    def test_data_for_MX(self):
        test_data = {b'raw_values': [{b'value': b'10 un.unit', b'ttl': 60}, {b'value': b'20 dau.unit', b'ttl': 60}, {b'value': b'30 tri.unit', b'ttl': 60}], b'zone': b'unit.tests.'}
        test_MX = MythicBeastsProvider._data_for_MX(b'', test_data)
        self.assertTrue(isinstance(test_MX, dict))
        self.assertEquals(3, len(test_MX[b'values']))
        with self.assertRaises(AssertionError) as (err):
            test_MX = MythicBeastsProvider._data_for_MX(b'', {b'raw_values': [{b'value': b'', b'ttl': 0}]})
        self.assertEquals(b'Unable to parse MX data', text_type(err.exception))

    def test_data_for_CNAME(self):
        test_data = {b'raw_values': [{b'value': b'cname', b'ttl': 60}], b'zone': b'unit.tests.'}
        test_cname = MythicBeastsProvider._data_for_CNAME(b'', test_data)
        self.assertTrue(isinstance(test_cname, dict))
        self.assertEquals(b'cname.unit.tests.', test_cname[b'value'])

    def test_data_for_ANAME(self):
        test_data = {b'raw_values': [{b'value': b'aname', b'ttl': 60}], b'zone': b'unit.tests.'}
        test_aname = MythicBeastsProvider._data_for_ANAME(b'', test_data)
        self.assertTrue(isinstance(test_aname, dict))
        self.assertEquals(b'aname', test_aname[b'value'])

    def test_data_for_SRV(self):
        test_data = {b'raw_values': [{b'value': b'10 20 30 un.srv.unit', b'ttl': 60}, {b'value': b'20 30 40 dau.srv.unit', b'ttl': 60}, {b'value': b'30 30 50 tri.srv.unit', b'ttl': 60}], b'zone': b'unit.tests.'}
        test_SRV = MythicBeastsProvider._data_for_SRV(b'', test_data)
        self.assertTrue(isinstance(test_SRV, dict))
        self.assertEquals(3, len(test_SRV[b'values']))
        with self.assertRaises(AssertionError) as (err):
            test_SRV = MythicBeastsProvider._data_for_SRV(b'', {b'raw_values': [{b'value': b'', b'ttl': 0}]})
        self.assertEquals(b'Unable to parse SRV data', text_type(err.exception))

    def test_data_for_SSHFP(self):
        test_data = {b'raw_values': [{b'value': b'1 1 0123456789abcdef', b'ttl': 60}, {b'value': b'1 2 0123456789abcdef', b'ttl': 60}, {b'value': b'2 3 0123456789abcdef', b'ttl': 60}], b'zone': b'unit.tests.'}
        test_SSHFP = MythicBeastsProvider._data_for_SSHFP(b'', test_data)
        self.assertTrue(isinstance(test_SSHFP, dict))
        self.assertEquals(3, len(test_SSHFP[b'values']))
        with self.assertRaises(AssertionError) as (err):
            test_SSHFP = MythicBeastsProvider._data_for_SSHFP(b'', {b'raw_values': [{b'value': b'', b'ttl': 0}]})
        self.assertEquals(b'Unable to parse SSHFP data', text_type(err.exception))

    def test_data_for_CAA(self):
        test_data = {b'raw_values': [{b'value': b'1 issue letsencrypt.org', b'ttl': 60}], b'zone': b'unit.tests.'}
        test_CAA = MythicBeastsProvider._data_for_CAA(b'', test_data)
        self.assertTrue(isinstance(test_CAA, dict))
        self.assertEquals(3, len(test_CAA[b'value']))
        with self.assertRaises(AssertionError) as (err):
            test_CAA = MythicBeastsProvider._data_for_CAA(b'', {b'raw_values': [{b'value': b'', b'ttl': 0}]})
        self.assertEquals(b'Unable to parse CAA data', text_type(err.exception))

    def test_command_generation(self):
        zone = Zone(b'unit.tests.', [])
        zone.add_record(Record.new(zone, b'prawf-alias', {b'ttl': 60, 
           b'type': b'ALIAS', 
           b'value': b'alias.unit.tests.'}))
        zone.add_record(Record.new(zone, b'prawf-ns', {b'ttl': 300, 
           b'type': b'NS', 
           b'values': [
                     b'alias.unit.tests.',
                     b'alias2.unit.tests.']}))
        zone.add_record(Record.new(zone, b'prawf-a', {b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.2.3.4',
                     b'5.6.7.8']}))
        zone.add_record(Record.new(zone, b'prawf-aaaa', {b'ttl': 60, 
           b'type': b'AAAA', 
           b'values': [
                     b'a:a::a',
                     b'b:b::b',
                     b'c:c::c:c']}))
        zone.add_record(Record.new(zone, b'prawf-txt', {b'ttl': 60, 
           b'type': b'TXT', 
           b'value': b'prawf prawf dyma prawf'}))
        zone.add_record(Record.new(zone, b'prawf-txt2', {b'ttl': 60, 
           b'type': b'TXT', 
           b'value': b'v=DKIM1\\; k=rsa\\; p=prawf'}))
        with requests_mock() as (mock):
            mock.post(ANY, status_code=200, text=b'')
            provider = MythicBeastsProvider(b'test', {b'unit.tests.': b'mypassword'})
            plan = provider.plan(zone)
            changes = plan.changes
            generated_commands = []
            for change in changes:
                generated_commands.extend(provider._compile_commands(b'ADD', change.new))

            expected_commands = [
             b'ADD prawf-alias.unit.tests 60 ANAME alias.unit.tests.',
             b'ADD prawf-ns.unit.tests 300 NS alias.unit.tests.',
             b'ADD prawf-ns.unit.tests 300 NS alias2.unit.tests.',
             b'ADD prawf-a.unit.tests 60 A 1.2.3.4',
             b'ADD prawf-a.unit.tests 60 A 5.6.7.8',
             b'ADD prawf-aaaa.unit.tests 60 AAAA a:a::a',
             b'ADD prawf-aaaa.unit.tests 60 AAAA b:b::b',
             b'ADD prawf-aaaa.unit.tests 60 AAAA c:c::c:c',
             b'ADD prawf-txt.unit.tests 60 TXT prawf prawf dyma prawf',
             b'ADD prawf-txt2.unit.tests 60 TXT v=DKIM1; k=rsa; p=prawf']
            generated_commands.sort()
            expected_commands.sort()
            self.assertEquals(generated_commands, expected_commands)
            existing = b'prawf-txt 300 TXT prawf prawf dyma prawf\nprawf-txt2 300 TXT v=DKIM1; k=rsa; p=prawf\nprawf-a 60 A 1.2.3.4'
            with requests_mock() as (mock):
                mock.post(ANY, status_code=200, text=existing)
                wanted = Zone(b'unit.tests.', [])
                plan = provider.plan(wanted)
                changes = plan.changes
                generated_commands = []
                for change in changes:
                    generated_commands.extend(provider._compile_commands(b'DELETE', change.existing))

            expected_commands = [
             b'DELETE prawf-a.unit.tests 60 A 1.2.3.4',
             b'DELETE prawf-txt.unit.tests 300 TXT prawf prawf dyma prawf',
             b'DELETE prawf-txt2.unit.tests 300 TXT v=DKIM1; k=rsa; p=prawf']
            generated_commands.sort()
            expected_commands.sort()
            self.assertEquals(generated_commands, expected_commands)

    def test_fake_command_generation(self):

        class FakeChangeRecord(object):

            def __init__(self):
                self.__fqdn = b'prawf.unit.tests.'
                self._type = b'NOOP'
                self.value = b'prawf'
                self.ttl = 60

            @property
            def record(self):
                return self

            @property
            def fqdn(self):
                return self.__fqdn

        with requests_mock() as (mock):
            mock.post(ANY, status_code=200, text=b'')
            provider = MythicBeastsProvider(b'test', {b'unit.tests.': b'mypassword'})
            record = FakeChangeRecord()
            command = provider._compile_commands(b'ADD', record)
            self.assertEquals([], command)

    def test_populate(self):
        provider = None
        with self.assertRaises(AssertionError) as (err):
            provider = MythicBeastsProvider(b'test', None)
        self.assertEquals(b'Passwords must be a dictionary', text_type(err.exception))
        with requests_mock() as (mock):
            mock.post(ANY, status_code=401, text=b'ERR Not authenticated')
            with self.assertRaises(AssertionError) as (err):
                provider = MythicBeastsProvider(b'test', dict())
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
            self.assertEquals(b'Missing password for domain: unit.tests', text_type(err.exception))
        with requests_mock() as (mock):
            mock.post(ANY, status_code=401, text=b'ERR Not authenticated')
            with self.assertRaises(Exception) as (err):
                provider = MythicBeastsProvider(b'test', {b'unit.tests.': b'mypassword'})
                zone = Zone(b'unit.tests.', [])
                provider.populate(zone)
            self.assertEquals(b'Mythic Beasts unauthorized for zone: unit.tests', err.exception.message)
        test_data = b'This should not match'
        with requests_mock() as (mock):
            mock.post(ANY, status_code=200, text=test_data)
            provider = MythicBeastsProvider(b'test', {b'unit.tests.': b'mypassword'})
            zone = Zone(b'unit.tests.', [])
            provider.populate(zone)
            self.assertEquals(0, len(zone.records))
        test_data = b'@ 60 NOOP prawf\n@ 60 SPF prawf prawf prawf'
        with requests_mock() as (mock):
            mock.post(ANY, status_code=200, text=test_data)
            provider = MythicBeastsProvider(b'test', {b'unit.tests.': b'mypassword'})
            zone = Zone(b'unit.tests.', [])
            provider.populate(zone)
            self.assertEquals(0, len(zone.records))
        with requests_mock() as (mock):
            with open(b'tests/fixtures/mythicbeasts-list.txt') as (file_handle):
                mock.post(ANY, status_code=200, text=file_handle.read())
            provider = MythicBeastsProvider(b'test', {b'unit.tests.': b'mypassword'})
            zone = Zone(b'unit.tests.', [])
            provider.populate(zone)
            self.assertEquals(15, len(zone.records))
            self.assertEquals(15, len(self.expected.records))
            changes = self.expected.changes(zone, provider)
            self.assertEquals(0, len(changes))
        return

    def test_apply(self):
        provider = MythicBeastsProvider(b'test', {b'unit.tests.': b'mypassword'})
        zone = Zone(b'unit.tests.', [])
        with requests_mock() as (mock):
            mock.post(ANY, status_code=200, text=b'')
            provider.populate(zone)
        self.assertEquals(0, len(zone.records))
        with requests_mock() as (mock):
            mock.post(ANY, status_code=200, text=b'')
            provider.populate(zone)
            zone.add_record(Record.new(zone, b'prawf', {b'ttl': 300, 
               b'type': b'TXT', 
               b'value': b'prawf'}))
            plan = provider.plan(zone)
        with requests_mock() as (mock):
            mock.post(ANY, status_code=400, text=b'NADD 300 TXT prawf')
            with self.assertRaises(Exception) as (err):
                provider.apply(plan)
            self.assertEquals(b'Mythic Beasts could not action command: unit.tests ADD prawf.unit.tests 300 TXT prawf', err.exception.message)
        existing = b'prawf 300 TXT prawf prawf prawf\ndileu 300 TXT dileu'
        with requests_mock() as (mock):
            mock.post(ANY, status_code=200, text=existing)
            wanted = Zone(b'unit.tests.', [])
            for record in list(self.expected.records):
                data = {b'type': record._type}
                data.update(record.data)
                wanted.add_record(Record.new(wanted, record.name, data))

            wanted.add_record(Record.new(wanted, b'prawf', {b'ttl': 60, 
               b'type': b'TXT', 
               b'value': b'prawf yw e'}))
            plan = provider.plan(wanted)
            self.assertEquals(1, len([ c for c in plan.changes if isinstance(c, Update)
                                     ]))
            self.assertEquals(1, len([ c for c in plan.changes if isinstance(c, Delete)
                                     ]))
            self.assertEquals(14, len([ c for c in plan.changes if isinstance(c, Create)
                                      ]))
            self.assertEquals(16, provider.apply(plan))
            self.assertTrue(plan.exists)