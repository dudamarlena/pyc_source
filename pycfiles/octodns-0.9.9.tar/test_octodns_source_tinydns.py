# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_source_tinydns.py
# Compiled at: 2019-04-27 17:13:19
from __future__ import absolute_import, division, print_function, unicode_literals
from unittest import TestCase
from octodns.record import Record
from octodns.source.tinydns import TinyDnsFileSource
from octodns.zone import Zone
from helpers import SimpleProvider

class TestTinyDnsFileSource(TestCase):
    source = TinyDnsFileSource(b'test', b'./tests/zones/tinydns')

    def test_populate_normal(self):
        got = Zone(b'example.com.', [])
        self.source.populate(got)
        self.assertEquals(17, len(got.records))
        expected = Zone(b'example.com.', [])
        for name, data in (
         (
          b'',
          {b'type': b'A', 
             b'ttl': 30, 
             b'values': [
                       b'10.2.3.4', b'10.2.3.5']}),
         (
          b'sub',
          {b'type': b'NS', 
             b'ttl': 30, 
             b'values': [
                       b'ns1.ns.com.', b'ns2.ns.com.']}),
         (
          b'www',
          {b'type': b'A', 
             b'ttl': 3600, 
             b'value': b'10.2.3.6'}),
         (
          b'cname',
          {b'type': b'CNAME', 
             b'ttl': 3600, 
             b'value': b'www.example.com.'}),
         (
          b'some-host-abc123',
          {b'type': b'A', 
             b'ttl': 1800, 
             b'value': b'10.2.3.7'}),
         (
          b'has-dup-def123',
          {b'type': b'A', 
             b'ttl': 3600, 
             b'value': b'10.2.3.8'}),
         (
          b'www.sub',
          {b'type': b'A', 
             b'ttl': 3600, 
             b'value': b'1.2.3.4'}),
         (
          b'has-dup-def456',
          {b'type': b'A', 
             b'ttl': 3600, 
             b'value': b'10.2.3.8'}),
         (
          b'',
          {b'type': b'MX', 
             b'ttl': 3600, 
             b'values': [
                       {b'preference': 10, 
                          b'exchange': b'smtp-1-host.example.com.'},
                       {b'preference': 20, 
                          b'exchange': b'smtp-2-host.example.com.'}]}),
         (
          b'smtp',
          {b'type': b'MX', 
             b'ttl': 1800, 
             b'values': [
                       {b'preference': 30, 
                          b'exchange': b'smtp-1-host.example.com.'},
                       {b'preference': 40, 
                          b'exchange': b'smtp-2-host.example.com.'}]}),
         (
          b'',
          {b'type': b'TXT', 
             b'ttl': 300, 
             b'value': b'test TXT'}),
         (
          b'colon',
          {b'type': b'TXT', 
             b'ttl': 300, 
             b'value': b'test : TXT'}),
         (
          b'nottl',
          {b'type': b'TXT', 
             b'ttl': 3600, 
             b'value': b'nottl test TXT'}),
         (
          b'ipv6-3',
          {b'type': b'AAAA', 
             b'ttl': 300, 
             b'value': b'2a02:1348:017c:d5d0:0024:19ff:fef3:5742'}),
         (
          b'ipv6-6',
          {b'type': b'AAAA', 
             b'ttl': 3600, 
             b'value': b'2a02:1348:017c:d5d0:0024:19ff:fef3:5743'}),
         (
          b'semicolon',
          {b'type': b'TXT', 
             b'ttl': 300, 
             b'value': b'v=DKIM1\\; k=rsa\\; p=blah'})):
            record = Record.new(expected, name, data)
            expected.add_record(record)

        changes = expected.changes(got, SimpleProvider())
        self.assertEquals([], changes)

    def test_populate_normal_sub1(self):
        got = Zone(b'asdf.subtest.com.', [])
        self.source.populate(got)
        self.assertEquals(1, len(got.records))
        expected = Zone(b'asdf.subtest.com.', [])
        for name, data in (
         (
          b'a3',
          {b'type': b'A', 
             b'ttl': 3600, 
             b'values': [
                       b'10.2.3.7']}),):
            record = Record.new(expected, name, data)
            expected.add_record(record)

        changes = expected.changes(got, SimpleProvider())
        self.assertEquals([], changes)

    def test_populate_normal_sub2(self):
        got = Zone(b'blah-asdf.subtest.com.', [])
        self.source.populate(got)
        self.assertEquals(2, len(got.records))
        expected = Zone(b'sub-asdf.subtest.com.', [])
        for name, data in (
         (
          b'a1',
          {b'type': b'A', 
             b'ttl': 3600, 
             b'values': [
                       b'10.2.3.5']}),
         (
          b'a2',
          {b'type': b'A', 
             b'ttl': 3600, 
             b'values': [
                       b'10.2.3.6']})):
            record = Record.new(expected, name, data)
            expected.add_record(record)

        changes = expected.changes(got, SimpleProvider())
        self.assertEquals([], changes)

    def test_populate_in_addr_arpa(self):
        got = Zone(b'3.2.10.in-addr.arpa.', [])
        self.source.populate(got)
        expected = Zone(b'3.2.10.in-addr.arpa.', [])
        for name, data in (
         (
          b'10',
          {b'type': b'PTR', 
             b'ttl': 3600, 
             b'value': b'a-ptr.example.com.'}),
         (
          b'11',
          {b'type': b'PTR', 
             b'ttl': 30, 
             b'value': b'a-ptr-2.example.com.'}),
         (
          b'8',
          {b'type': b'PTR', 
             b'ttl': 3600, 
             b'value': b'has-dup-def123.example.com.'}),
         (
          b'7',
          {b'type': b'PTR', 
             b'ttl': 1800, 
             b'value': b'some-host-abc123.example.com.'})):
            record = Record.new(expected, name, data)
            expected.add_record(record)

        changes = expected.changes(got, SimpleProvider())
        self.assertEquals([], changes)

    def test_ignores_subs(self):
        got = Zone(b'example.com.', [b'sub'])
        self.source.populate(got)
        self.assertEquals(16, len(got.records))