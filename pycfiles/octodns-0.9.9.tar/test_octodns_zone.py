# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_zone.py
# Compiled at: 2019-10-18 13:06:59
from __future__ import absolute_import, division, print_function, unicode_literals
from unittest import TestCase
from six import text_type
from octodns.record import ARecord, AaaaRecord, Create, Delete, Record, Update
from octodns.zone import DuplicateRecordException, InvalidNodeException, SubzoneRecordException, Zone
from helpers import SimpleProvider

class TestZone(TestCase):

    def test_lowering(self):
        zone = Zone(b'UniT.TEsTs.', [])
        self.assertEquals(b'unit.tests.', zone.name)

    def test_hostname_from_fqdn(self):
        zone = Zone(b'unit.tests.', [])
        for hostname, fqdn in (
         ('', 'unit.tests.'),
         ('', 'unit.tests'),
         ('foo', 'foo.unit.tests.'),
         ('foo', 'foo.unit.tests'),
         ('foo.bar', 'foo.bar.unit.tests.'),
         ('foo.bar', 'foo.bar.unit.tests'),
         ('foo.unit.tests', 'foo.unit.tests.unit.tests.'),
         ('foo.unit.tests', 'foo.unit.tests.unit.tests')):
            self.assertEquals(hostname, zone.hostname_from_fqdn(fqdn))

    def test_add_record(self):
        zone = Zone(b'unit.tests.', [])
        a = ARecord(zone, b'a', {b'ttl': 42, b'value': b'1.1.1.1'})
        b = ARecord(zone, b'b', {b'ttl': 42, b'value': b'1.1.1.1'})
        c = ARecord(zone, b'a', {b'ttl': 43, b'value': b'2.2.2.2'})
        zone.add_record(a)
        self.assertEquals(zone.records, set([a]))
        with self.assertRaises(DuplicateRecordException) as (ctx):
            zone.add_record(a)
        self.assertEquals(b'Duplicate record a.unit.tests., type A', text_type(ctx.exception))
        self.assertEquals(zone.records, set([a]))
        zone.add_record(c, replace=True)
        self.assertEquals(b'2.2.2.2', list(zone.records)[0].values[0])
        zone.add_record(b)
        self.assertEquals(zone.records, set([a, b]))

    def test_changes(self):
        before = Zone(b'unit.tests.', [])
        a = ARecord(before, b'a', {b'ttl': 42, b'value': b'1.1.1.1'})
        before.add_record(a)
        b = AaaaRecord(before, b'b', {b'ttl': 42, b'value': b'1:1:1::1'})
        before.add_record(b)
        after = Zone(b'unit.tests.', [])
        after.add_record(a)
        after.add_record(b)
        target = SimpleProvider()
        self.assertFalse(before.changes(after, target))
        c = ARecord(before, b'c', {b'ttl': 42, b'value': b'1.1.1.1'})
        after.add_record(c)
        after._remove_record(b)
        self.assertEquals(after.records, set([a, c]))
        changes = before.changes(after, target)
        self.assertEquals(2, len(changes))
        for change in changes:
            if isinstance(change, Create):
                create = change
            elif isinstance(change, Delete):
                delete = change

        self.assertEquals(b, delete.existing)
        self.assertFalse(delete.new)
        self.assertEquals(c, create.new)
        self.assertFalse(create.existing)
        delete.__repr__()
        create.__repr__()
        after = Zone(b'unit.tests.', [])
        changed = ARecord(before, b'a', {b'ttl': 42, b'value': b'2.2.2.2'})
        after.add_record(changed)
        after.add_record(b)
        changes = before.changes(after, target)
        self.assertEquals(1, len(changes))
        update = changes[0]
        self.assertIsInstance(update, Update)
        self.assertFalse(a.changes(update.existing, target))
        self.assertFalse(changed.changes(update.new, target))
        update.__repr__()

    def test_unsupporting(self):

        class NoAaaaProvider(object):
            id = b'no-aaaa'
            SUPPORTS_GEO = False
            SUPPORTS_DYNAMIC = False

            def supports(self, record):
                return record._type != b'AAAA'

        current = Zone(b'unit.tests.', [])
        desired = Zone(b'unit.tests.', [])
        a = ARecord(desired, b'a', {b'ttl': 42, b'value': b'1.1.1.1'})
        desired.add_record(a)
        aaaa = AaaaRecord(desired, b'b', {b'ttl': 42, b'value': b'1:1:1::1'})
        desired.add_record(aaaa)
        changes = current.changes(desired, NoAaaaProvider())
        self.assertEquals(1, len(changes))
        self.assertIsInstance(changes[0], Create)
        changes = desired.changes(current, NoAaaaProvider())
        self.assertEquals(1, len(changes))
        self.assertIsInstance(changes[0], Delete)

    def test_missing_dot(self):
        with self.assertRaises(Exception) as (ctx):
            Zone(b'not.allowed', [])
        self.assertTrue(b'missing ending dot' in text_type(ctx.exception))

    def test_sub_zones(self):
        zone = Zone(b'unit.tests.', set([b'sub', b'barred']))
        record = Record.new(zone, b'sub', {b'ttl': 3600, 
           b'type': b'NS', 
           b'values': [
                     b'1.2.3.4.', b'2.3.4.5.']})
        zone.add_record(record)
        self.assertEquals(set([record]), zone.records)
        zone = Zone(b'unit.tests.', set([b'sub', b'barred']))
        record = Record.new(zone, b'sub', {b'ttl': 3600, 
           b'type': b'A', 
           b'values': [
                     b'1.2.3.4', b'2.3.4.5']})
        with self.assertRaises(SubzoneRecordException) as (ctx):
            zone.add_record(record)
        self.assertTrue(b'not of type NS', text_type(ctx.exception))
        zone.add_record(record, lenient=True)
        self.assertEquals(set([record]), zone.records)
        zone = Zone(b'unit.tests.', set([b'sub', b'barred']))
        record = Record.new(zone, b'foo.sub', {b'ttl': 3600, 
           b'type': b'NS', 
           b'values': [
                     b'1.2.3.4.', b'2.3.4.5.']})
        with self.assertRaises(SubzoneRecordException) as (ctx):
            zone.add_record(record)
        self.assertTrue(b'under a managed sub-zone', text_type(ctx.exception))
        zone.add_record(record, lenient=True)
        self.assertEquals(set([record]), zone.records)
        zone = Zone(b'unit.tests.', set([b'sub', b'barred']))
        record = Record.new(zone, b'foo.bar.sub', {b'ttl': 3600, 
           b'type': b'A', 
           b'values': [
                     b'1.2.3.4', b'2.3.4.5']})
        with self.assertRaises(SubzoneRecordException) as (ctx):
            zone.add_record(record)
        self.assertTrue(b'under a managed sub-zone', text_type(ctx.exception))
        zone.add_record(record, lenient=True)
        self.assertEquals(set([record]), zone.records)

    def test_ignored_records(self):
        zone_normal = Zone(b'unit.tests.', [])
        zone_ignored = Zone(b'unit.tests.', [])
        zone_missing = Zone(b'unit.tests.', [])
        normal = Record.new(zone_normal, b'www', {b'ttl': 60, 
           b'type': b'A', 
           b'value': b'9.9.9.9'})
        zone_normal.add_record(normal)
        ignored = Record.new(zone_ignored, b'www', {b'octodns': {b'ignored': True}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'value': b'9.9.9.9'})
        zone_ignored.add_record(ignored)
        provider = SimpleProvider()
        self.assertFalse(zone_normal.changes(zone_ignored, provider))
        self.assertTrue(zone_normal.changes(zone_missing, provider))
        self.assertFalse(zone_ignored.changes(zone_normal, provider))
        self.assertFalse(zone_ignored.changes(zone_missing, provider))
        self.assertTrue(zone_missing.changes(zone_normal, provider))
        self.assertFalse(zone_missing.changes(zone_ignored, provider))

    def test_cname_coexisting(self):
        zone = Zone(b'unit.tests.', [])
        a = Record.new(zone, b'www', {b'ttl': 60, 
           b'type': b'A', 
           b'value': b'9.9.9.9'})
        cname = Record.new(zone, b'www', {b'ttl': 60, 
           b'type': b'CNAME', 
           b'value': b'foo.bar.com.'})
        zone.add_record(a)
        with self.assertRaises(InvalidNodeException):
            zone.add_record(cname)
        self.assertEquals(set([a]), zone.records)
        zone.add_record(cname, lenient=True)
        self.assertEquals(set([a, cname]), zone.records)
        zone = Zone(b'unit.tests.', [])
        zone.add_record(cname)
        with self.assertRaises(InvalidNodeException):
            zone.add_record(a)
        self.assertEquals(set([cname]), zone.records)
        zone.add_record(a, lenient=True)
        self.assertEquals(set([a, cname]), zone.records)

    def test_excluded_records(self):
        zone_normal = Zone(b'unit.tests.', [])
        zone_excluded = Zone(b'unit.tests.', [])
        zone_missing = Zone(b'unit.tests.', [])
        normal = Record.new(zone_normal, b'www', {b'ttl': 60, 
           b'type': b'A', 
           b'value': b'9.9.9.9'})
        zone_normal.add_record(normal)
        excluded = Record.new(zone_excluded, b'www', {b'octodns': {b'excluded': [
                                    b'test']}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'value': b'9.9.9.9'})
        zone_excluded.add_record(excluded)
        provider = SimpleProvider()
        self.assertFalse(zone_normal.changes(zone_excluded, provider))
        self.assertTrue(zone_normal.changes(zone_missing, provider))
        self.assertFalse(zone_excluded.changes(zone_normal, provider))
        self.assertFalse(zone_excluded.changes(zone_missing, provider))
        self.assertTrue(zone_missing.changes(zone_normal, provider))
        self.assertFalse(zone_missing.changes(zone_excluded, provider))

    def test_included_records(self):
        zone_normal = Zone(b'unit.tests.', [])
        zone_included = Zone(b'unit.tests.', [])
        zone_missing = Zone(b'unit.tests.', [])
        normal = Record.new(zone_normal, b'www', {b'ttl': 60, 
           b'type': b'A', 
           b'value': b'9.9.9.9'})
        zone_normal.add_record(normal)
        included = Record.new(zone_included, b'www', {b'octodns': {b'included': [
                                    b'test']}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'value': b'9.9.9.9'})
        zone_included.add_record(included)
        provider = SimpleProvider()
        self.assertFalse(zone_normal.changes(zone_included, provider))
        self.assertTrue(zone_normal.changes(zone_missing, provider))
        self.assertFalse(zone_included.changes(zone_normal, provider))
        self.assertTrue(zone_included.changes(zone_missing, provider))
        self.assertTrue(zone_missing.changes(zone_normal, provider))
        self.assertTrue(zone_missing.changes(zone_included, provider))

    def test_not_included_records(self):
        zone_normal = Zone(b'unit.tests.', [])
        zone_included = Zone(b'unit.tests.', [])
        zone_missing = Zone(b'unit.tests.', [])
        normal = Record.new(zone_normal, b'www', {b'ttl': 60, 
           b'type': b'A', 
           b'value': b'9.9.9.9'})
        zone_normal.add_record(normal)
        included = Record.new(zone_included, b'www', {b'octodns': {b'included': [
                                    b'not-here']}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'value': b'9.9.9.9'})
        zone_included.add_record(included)
        provider = SimpleProvider()
        self.assertFalse(zone_normal.changes(zone_included, provider))
        self.assertTrue(zone_normal.changes(zone_missing, provider))
        self.assertFalse(zone_included.changes(zone_normal, provider))
        self.assertFalse(zone_included.changes(zone_missing, provider))
        self.assertTrue(zone_missing.changes(zone_normal, provider))
        self.assertFalse(zone_missing.changes(zone_included, provider))