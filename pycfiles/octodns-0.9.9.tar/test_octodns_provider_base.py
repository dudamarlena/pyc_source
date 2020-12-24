# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_base.py
# Compiled at: 2019-10-18 13:06:59
from __future__ import absolute_import, division, print_function, unicode_literals
from logging import getLogger
from six import text_type
from unittest import TestCase
from octodns.record import Create, Delete, Record, Update
from octodns.provider.base import BaseProvider
from octodns.provider.plan import Plan, UnsafePlan
from octodns.zone import Zone

class HelperProvider(BaseProvider):
    log = getLogger(b'HelperProvider')
    SUPPORTS = set(('A', ))
    id = b'test'

    def __init__(self, extra_changes, apply_disabled=False, include_change_callback=None):
        self.__extra_changes = extra_changes
        self.apply_disabled = apply_disabled
        self.include_change_callback = include_change_callback
        self.update_pcent_threshold = Plan.MAX_SAFE_UPDATE_PCENT
        self.delete_pcent_threshold = Plan.MAX_SAFE_DELETE_PCENT

    def populate(self, zone, target=False, lenient=False):
        pass

    def _include_change(self, change):
        return not self.include_change_callback or self.include_change_callback(change)

    def _extra_changes(self, **kwargs):
        return self.__extra_changes

    def _apply(self, plan):
        pass


class TestBaseProvider(TestCase):

    def test_base_provider(self):
        with self.assertRaises(NotImplementedError) as (ctx):
            BaseProvider(b'base')
        self.assertEquals(b'Abstract base class, log property missing', text_type(ctx.exception))

        class HasLog(BaseProvider):
            log = getLogger(b'HasLog')

        with self.assertRaises(NotImplementedError) as (ctx):
            HasLog(b'haslog')
        self.assertEquals(b'Abstract base class, SUPPORTS_GEO property missing', text_type(ctx.exception))

        class HasSupportsGeo(HasLog):
            SUPPORTS_GEO = False

        zone = Zone(b'unit.tests.', [b'sub'])
        with self.assertRaises(NotImplementedError) as (ctx):
            HasSupportsGeo(b'hassupportsgeo').populate(zone)
        self.assertEquals(b'Abstract base class, SUPPORTS property missing', text_type(ctx.exception))

        class HasSupports(HasSupportsGeo):
            SUPPORTS = set(('A', ))

        with self.assertRaises(NotImplementedError) as (ctx):
            HasSupports(b'hassupports').populate(zone)
        self.assertEquals(b'Abstract base class, populate method missing', text_type(ctx.exception))
        self.assertFalse(HasSupports(b'hassupports').SUPPORTS_DYNAMIC)

        class HasSupportsDyanmic(HasSupports):
            SUPPORTS_DYNAMIC = True

        self.assertTrue(HasSupportsDyanmic(b'hassupportsdynamic').SUPPORTS_DYNAMIC)

        class HasPopulate(HasSupports):

            def populate(self, zone, target=False, lenient=False):
                zone.add_record(Record.new(zone, b'', {b'ttl': 60, 
                   b'type': b'A', 
                   b'value': b'2.3.4.5'}), lenient=lenient)
                zone.add_record(Record.new(zone, b'going', {b'ttl': 60, 
                   b'type': b'A', 
                   b'value': b'3.4.5.6'}), lenient=lenient)
                zone.add_record(Record.new(zone, b'foo.sub', {b'ttl': 61, 
                   b'type': b'A', 
                   b'value': b'4.5.6.7'}), lenient=lenient)

        zone.add_record(Record.new(zone, b'', {b'ttl': 60, 
           b'type': b'A', 
           b'value': b'1.2.3.4'}))
        self.assertTrue(HasSupports(b'hassupportsgeo').supports(list(zone.records)[0]))
        plan = HasPopulate(b'haspopulate').plan(zone)
        self.assertEquals(3, len(plan.changes))
        with self.assertRaises(NotImplementedError) as (ctx):
            HasPopulate(b'haspopulate').apply(plan)
        self.assertEquals(b'Abstract base class, _apply method missing', text_type(ctx.exception))

    def test_plan(self):
        ignored = Zone(b'unit.tests.', [])
        provider = HelperProvider([])
        self.assertEquals(None, provider.plan(ignored))
        record = Record.new(ignored, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        provider = HelperProvider([Create(record)])
        plan = provider.plan(ignored)
        self.assertTrue(plan)
        self.assertEquals(1, len(plan.changes))
        return

    def test_apply(self):
        ignored = Zone(b'unit.tests.', [])
        record = Record.new(ignored, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        provider = HelperProvider([Create(record)], apply_disabled=True)
        plan = provider.plan(ignored)
        provider.apply(plan)
        provider.apply_disabled = False
        self.assertEquals(1, provider.apply(plan))

    def test_include_change(self):
        zone = Zone(b'unit.tests.', [])
        record = Record.new(zone, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        zone.add_record(record)
        provider = HelperProvider([], include_change_callback=lambda c: False)
        plan = provider.plan(zone)
        self.assertFalse(plan)

    def test_safe_none(self):
        Plan(None, None, [], True).raise_if_unsafe()
        return

    def test_safe_creates(self):
        zone = Zone(b'unit.tests.', [])
        record = Record.new(zone, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        Plan(zone, zone, [ Create(record) for i in range(10) ], True).raise_if_unsafe()

    def test_safe_min_existing_creates(self):
        zone = Zone(b'unit.tests.', [])
        record = Record.new(zone, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        for i in range(int(Plan.MIN_EXISTING_RECORDS)):
            zone.add_record(Record.new(zone, text_type(i), {b'ttl': 60, 
               b'type': b'A', 
               b'value': b'2.3.4.5'}))

        Plan(zone, zone, [ Create(record) for i in range(10) ], True).raise_if_unsafe()

    def test_safe_no_existing(self):
        zone = Zone(b'unit.tests.', [])
        record = Record.new(zone, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        updates = [
         Update(record, record), Update(record, record)]
        Plan(zone, zone, updates, True).raise_if_unsafe()

    def test_safe_updates_min_existing(self):
        zone = Zone(b'unit.tests.', [])
        record = Record.new(zone, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        for i in range(int(Plan.MIN_EXISTING_RECORDS)):
            zone.add_record(Record.new(zone, text_type(i), {b'ttl': 60, 
               b'type': b'A', 
               b'value': b'2.3.4.5'}))

        changes = [ Update(record, record) for i in range(int(Plan.MIN_EXISTING_RECORDS * Plan.MAX_SAFE_UPDATE_PCENT) + 1)
                  ]
        with self.assertRaises(UnsafePlan) as (ctx):
            Plan(zone, zone, changes, True).raise_if_unsafe()
        self.assertTrue(b'Too many updates' in text_type(ctx.exception))

    def test_safe_updates_min_existing_pcent(self):
        zone = Zone(b'unit.tests.', [])
        record = Record.new(zone, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        for i in range(int(Plan.MIN_EXISTING_RECORDS)):
            zone.add_record(Record.new(zone, text_type(i), {b'ttl': 60, 
               b'type': b'A', 
               b'value': b'2.3.4.5'}))

        changes = [ Update(record, record) for i in range(int(Plan.MIN_EXISTING_RECORDS * Plan.MAX_SAFE_UPDATE_PCENT))
                  ]
        Plan(zone, zone, changes, True).raise_if_unsafe()

    def test_safe_deletes_min_existing(self):
        zone = Zone(b'unit.tests.', [])
        record = Record.new(zone, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        for i in range(int(Plan.MIN_EXISTING_RECORDS)):
            zone.add_record(Record.new(zone, text_type(i), {b'ttl': 60, 
               b'type': b'A', 
               b'value': b'2.3.4.5'}))

        changes = [ Delete(record) for i in range(int(Plan.MIN_EXISTING_RECORDS * Plan.MAX_SAFE_DELETE_PCENT) + 1)
                  ]
        with self.assertRaises(UnsafePlan) as (ctx):
            Plan(zone, zone, changes, True).raise_if_unsafe()
        self.assertTrue(b'Too many deletes' in text_type(ctx.exception))

    def test_safe_deletes_min_existing_pcent(self):
        zone = Zone(b'unit.tests.', [])
        record = Record.new(zone, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        for i in range(int(Plan.MIN_EXISTING_RECORDS)):
            zone.add_record(Record.new(zone, text_type(i), {b'ttl': 60, 
               b'type': b'A', 
               b'value': b'2.3.4.5'}))

        changes = [ Delete(record) for i in range(int(Plan.MIN_EXISTING_RECORDS * Plan.MAX_SAFE_DELETE_PCENT))
                  ]
        Plan(zone, zone, changes, True).raise_if_unsafe()

    def test_safe_updates_min_existing_override(self):
        safe_pcent = 0.4
        zone = Zone(b'unit.tests.', [])
        record = Record.new(zone, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        for i in range(int(Plan.MIN_EXISTING_RECORDS)):
            zone.add_record(Record.new(zone, text_type(i), {b'ttl': 60, 
               b'type': b'A', 
               b'value': b'2.3.4.5'}))

        changes = [ Update(record, record) for i in range(int(Plan.MIN_EXISTING_RECORDS * safe_pcent) + 1)
                  ]
        with self.assertRaises(UnsafePlan) as (ctx):
            Plan(zone, zone, changes, True, update_pcent_threshold=safe_pcent).raise_if_unsafe()
        self.assertTrue(b'Too many updates' in text_type(ctx.exception))

    def test_safe_deletes_min_existing_override(self):
        safe_pcent = 0.4
        zone = Zone(b'unit.tests.', [])
        record = Record.new(zone, b'a', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        for i in range(int(Plan.MIN_EXISTING_RECORDS)):
            zone.add_record(Record.new(zone, text_type(i), {b'ttl': 60, 
               b'type': b'A', 
               b'value': b'2.3.4.5'}))

        changes = [ Delete(record) for i in range(int(Plan.MIN_EXISTING_RECORDS * safe_pcent) + 1)
                  ]
        with self.assertRaises(UnsafePlan) as (ctx):
            Plan(zone, zone, changes, True, delete_pcent_threshold=safe_pcent).raise_if_unsafe()
        self.assertTrue(b'Too many deletes' in text_type(ctx.exception))