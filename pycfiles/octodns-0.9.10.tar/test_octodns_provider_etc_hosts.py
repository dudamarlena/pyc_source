# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_etc_hosts.py
# Compiled at: 2019-03-28 16:58:28
from __future__ import absolute_import, division, print_function, unicode_literals
from os import path
from os.path import dirname, isfile
from unittest import TestCase
from octodns.provider.etc_hosts import EtcHostsProvider
from octodns.provider.plan import Plan
from octodns.record import Record
from octodns.zone import Zone
from helpers import TemporaryDirectory

class TestEtcHostsProvider(TestCase):

    def test_provider(self):
        source = EtcHostsProvider(b'test', path.join(dirname(__file__), b'config'))
        zone = Zone(b'unit.tests.', [])
        source.populate(zone, target=source)
        self.assertEquals(0, len(zone.records))
        source.populate(zone)
        self.assertEquals(0, len(zone.records))
        record = Record.new(zone, b'', {b'ttl': 60, 
           b'type': b'ALIAS', 
           b'value': b'www.unit.tests.'})
        zone.add_record(record)
        record = Record.new(zone, b'www', {b'ttl': 60, 
           b'type': b'AAAA', 
           b'value': b'2001:4860:4860::8888'})
        zone.add_record(record)
        record = Record.new(zone, b'www', {b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1', b'2.2.2.2']})
        zone.add_record(record)
        record = record.new(zone, b'v6', {b'ttl': 60, 
           b'type': b'AAAA', 
           b'value': b'2001:4860:4860::8844'})
        zone.add_record(record)
        record = record.new(zone, b'start', {b'ttl': 60, 
           b'type': b'CNAME', 
           b'value': b'middle.unit.tests.'})
        zone.add_record(record)
        record = record.new(zone, b'middle', {b'ttl': 60, 
           b'type': b'CNAME', 
           b'value': b'unit.tests.'})
        zone.add_record(record)
        record = record.new(zone, b'ext', {b'ttl': 60, 
           b'type': b'CNAME', 
           b'value': b'github.com.'})
        zone.add_record(record)
        record = record.new(zone, b'*', {b'ttl': 60, 
           b'type': b'A', 
           b'value': b'3.3.3.3'})
        zone.add_record(record)
        with TemporaryDirectory() as (td):
            directory = path.join(td.dirname, b'sub', b'dir')
            hosts_file = path.join(directory, b'unit.tests.hosts')
            target = EtcHostsProvider(b'test', directory)
            plan = target.plan(zone)
            self.assertEquals(len(zone.records), len(plan.changes))
            self.assertFalse(isfile(hosts_file))
            self.assertEquals(len(zone.records), target.apply(plan))
            self.assertTrue(isfile(hosts_file))
            with open(hosts_file) as (fh):
                data = fh.read()
                self.assertTrue(b'2001:4860:4860::8844\tv6.unit.tests' in data)
                self.assertTrue(b'1.1.1.1\twww.unit.tests' in data)
                self.assertTrue(b'# unit.tests -> www.unit.tests' in data)
                self.assertTrue(b'1.1.1.1\tunit.tests' in data)
                self.assertTrue(b'# start.unit.tests -> middle.unit.tests' in data)
                self.assertTrue(b'# middle.unit.tests -> unit.tests' in data)
                self.assertTrue(b'# unit.tests -> www.unit.tests' in data)
                self.assertTrue(b'1.1.1.1\tstart.unit.tests' in data)
            plan = Plan(zone, zone, [], True)
            self.assertEquals(0, target.apply(plan))

    def test_cname_loop(self):
        source = EtcHostsProvider(b'test', path.join(dirname(__file__), b'config'))
        zone = Zone(b'unit.tests.', [])
        source.populate(zone, target=source)
        self.assertEquals(0, len(zone.records))
        source.populate(zone)
        self.assertEquals(0, len(zone.records))
        record = Record.new(zone, b'start', {b'ttl': 60, 
           b'type': b'CNAME', 
           b'value': b'middle.unit.tests.'})
        zone.add_record(record)
        record = Record.new(zone, b'middle', {b'ttl': 60, 
           b'type': b'CNAME', 
           b'value': b'loop.unit.tests.'})
        zone.add_record(record)
        record = Record.new(zone, b'loop', {b'ttl': 60, 
           b'type': b'CNAME', 
           b'value': b'start.unit.tests.'})
        zone.add_record(record)
        with TemporaryDirectory() as (td):
            directory = path.join(td.dirname, b'sub', b'dir')
            hosts_file = path.join(directory, b'unit.tests.hosts')
            target = EtcHostsProvider(b'test', directory)
            plan = target.plan(zone)
            self.assertEquals(len(zone.records), len(plan.changes))
            self.assertFalse(isfile(hosts_file))
            self.assertEquals(len(zone.records), target.apply(plan))
            self.assertTrue(isfile(hosts_file))
            with open(hosts_file) as (fh):
                data = fh.read()
                self.assertTrue(b'# loop.unit.tests -> start.unit.tests **loop**' in data)
                self.assertTrue(b'# middle.unit.tests -> loop.unit.tests **loop**' in data)
                self.assertTrue(b'# start.unit.tests -> middle.unit.tests **loop**' in data)