# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_plan.py
# Compiled at: 2020-01-06 16:40:45
from __future__ import absolute_import, division, print_function, unicode_literals
from logging import getLogger
from six import StringIO, text_type
from unittest import TestCase
from octodns.provider.plan import Plan, PlanHtml, PlanLogger, PlanMarkdown
from octodns.record import Create, Delete, Record, Update
from octodns.zone import Zone
from helpers import SimpleProvider
simple = SimpleProvider()
zone = Zone(b'unit.tests.', [])
existing = Record.new(zone, b'a', {b'ttl': 300, 
   b'type': b'A', 
   b'values': [
             b'1.1.1.1', b'2.2.2.2']})
new = Record.new(zone, b'a', {b'geo': {b'AF': [
                  b'5.5.5.5'], 
            b'NA-US': [
                     b'6.6.6.6']}, 
   b'ttl': 300, 
   b'type': b'A', 
   b'values': [
             b'2.2.2.2', b'3.3.3.3', b'4.4.4.4']}, simple)
create = Create(Record.new(zone, b'b', {b'ttl': 60, 
   b'type': b'CNAME', 
   b'value': b'foo.unit.tests.'}, simple))
create2 = Create(Record.new(zone, b'c', {b'ttl': 60, 
   b'type': b'CNAME', 
   b'value': b'foo.unit.tests.'}))
update = Update(existing, new)
delete = Delete(new)
changes = [create, create2, delete, update]
plans = [
 (
  simple, Plan(zone, zone, changes, True)),
 (
  simple, Plan(zone, zone, changes, False))]

class TestPlanLogger(TestCase):

    def test_invalid_level(self):
        with self.assertRaises(Exception) as (ctx):
            PlanLogger(b'invalid', b'not-a-level')
        self.assertEquals(b'Unsupported level: not-a-level', text_type(ctx.exception))

    def test_create(self):

        class MockLogger(object):

            def __init__(self):
                self.out = StringIO()

            def log(self, level, msg):
                self.out.write(msg)

        log = MockLogger()
        PlanLogger(b'logger').run(log, plans)
        out = log.out.getvalue()
        self.assertTrue(b'Summary: Creates=2, Updates=1, Deletes=1, Existing Records=0' in out)


class TestPlanHtml(TestCase):
    log = getLogger(b'TestPlanHtml')

    def test_empty(self):
        out = StringIO()
        PlanHtml(b'html').run([], fh=out)
        self.assertEquals(b'<b>No changes were planned</b>', out.getvalue())

    def test_simple(self):
        out = StringIO()
        PlanHtml(b'html').run(plans, fh=out)
        out = out.getvalue()
        self.assertTrue(b'    <td colspan=6>Summary: Creates=2, Updates=1, Deletes=1, Existing Records=0</td>' in out)


class TestPlanMarkdown(TestCase):
    log = getLogger(b'TestPlanMarkdown')

    def test_empty(self):
        out = StringIO()
        PlanMarkdown(b'markdown').run([], fh=out)
        self.assertEquals(b'## No changes were planned\n', out.getvalue())

    def test_simple(self):
        out = StringIO()
        PlanMarkdown(b'markdown').run(plans, fh=out)
        out = out.getvalue()
        self.assertTrue(b'## unit.tests.' in out)
        self.assertTrue(b'Create | b | CNAME | 60 | foo.unit.tests.' in out)
        self.assertTrue(b'Update | a | A | 300 | 1.1.1.1;' in out)
        self.assertTrue(b'NA-US: 6.6.6.6 | test' in out)
        self.assertTrue(b'Delete | a | A | 300 | 2.2.2.2;' in out)