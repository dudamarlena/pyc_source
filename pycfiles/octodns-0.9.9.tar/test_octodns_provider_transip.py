# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_transip.py
# Compiled at: 2019-10-18 13:06:59
from __future__ import absolute_import, division, print_function, unicode_literals
from os.path import dirname, join
from six import text_type
from suds import WebFault
from unittest import TestCase
from octodns.provider.transip import TransipProvider
from octodns.provider.yaml import YamlProvider
from octodns.zone import Zone
from transip.service.domain import DomainService
from transip.service.objects import DnsEntry

class MockFault(object):
    faultstring = b''
    faultcode = b''

    def __init__(self, code, string, *args, **kwargs):
        self.faultstring = string
        self.faultcode = code


class MockResponse(object):
    dnsEntries = []


class MockDomainService(DomainService):

    def __init__(self, *args, **kwargs):
        super(MockDomainService, self).__init__(b'MockDomainService', *args, **kwargs)
        self.mockupEntries = []

    def mockup(self, records):
        provider = TransipProvider(b'', b'', b'')
        _dns_entries = []
        for record in records:
            if record._type in provider.SUPPORTS:
                entries_for = getattr(provider, (b'_entries_for_{}').format(record._type))
                name = record.name
                if name == b'':
                    name = provider.ROOT_RECORD
                _dns_entries.extend(entries_for(name, record))
                _dns_entries.append(DnsEntry(b'@', b'3600', b'NS', b'ns01.transip.nl.'))

        self.mockupEntries = _dns_entries

    def get_info(self, domain_name):
        if str(domain_name) == str(b'notfound.unit.tests'):
            self.raiseZoneNotFound()
        result = MockResponse()
        result.dnsEntries = self.mockupEntries
        return result

    def set_dns_entries(self, domain_name, dns_entries):
        if str(domain_name) == str(b'failsetdns.unit.tests'):
            self.raiseSaveError()
        return True

    def raiseZoneNotFound(self):
        fault = MockFault(str(b'102'), b'102 is zone not found')
        document = {}
        raise WebFault(fault, document)

    def raiseInvalidAuth(self):
        fault = MockFault(str(b'200'), b'200 is invalid auth')
        document = {}
        raise WebFault(fault, document)

    def raiseSaveError(self):
        fault = MockFault(str(b'200'), b'202 random error')
        document = {}
        raise WebFault(fault, document)


class TestTransipProvider(TestCase):
    bogus_key = str(b'-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA0U5HGCkLrz423IyUf3u4cKN2WrNz1x5KNr6PvH2M/zxas+zB\nelbxkdT3AQ+wmfcIvOuTmFRTHv35q2um1aBrPxVw+2s+lWo28VwIRttwIB1vIeWu\nlSBnkEZQRLyPI2tH0i5QoMX4CVPf9rvij3Uslimi84jdzDfPFIh6jZ6C8nLipOTG\n0IMhge1ofVfB0oSy5H+7PYS2858QLAf5ruYbzbAxZRivS402wGmQ0d0Lc1KxraAj\nkiMM5yj/CkH/Vm2w9I6+tLFeASE4ub5HCP5G/ig4dbYtqZMQMpqyAbGxd5SOVtyn\nUHagAJUxf8DT3I8PyjEHjxdOPUsxNyRtepO/7QIDAQABAoIBAQC7fiZ7gxE/ezjD\n2n6PsHFpHVTBLS2gzzZl0dCKZeFvJk6ODJDImaeuHhrh7X8ifMNsEI9XjnojMhl8\nMGPzy88mZHugDNK0H8B19x5G8v1/Fz7dG5WHas660/HFkS+b59cfdXOugYiOOn9O\n08HBBpLZNRUOmVUuQfQTjapSwGLG8PocgpyRD4zx0LnldnJcqYCxwCdev+AAsPnq\nibNtOd/MYD37w9MEGcaxLE8wGgkv8yd97aTjkgE+tp4zsM4QE4Rag133tsLLNznT\n4Qr/of15M3NW/DXq/fgctyRcJjZpU66eCXLCz2iRTnLyyxxDC2nwlxKbubV+lcS0\nS4hbfd/BAoGBAO8jXxEaiybR0aIhhSR5esEc3ymo8R8vBN3ZMJ+vr5jEPXr/ZuFj\n/R4cZ2XV3VoQJG0pvIOYVPZ5DpJM7W+zSXtJ/7bLXy4Bnmh/rc+YYgC+AXQoLSil\niD2OuB2xAzRAK71DVSO0kv8gEEXCersPT2i6+vC2GIlJvLcYbOdRKWGxAoGBAOAQ\naJbRLtKujH+kMdoMI7tRlL8XwI+SZf0FcieEu//nFyerTePUhVgEtcE+7eQ7hyhG\nfIXUFx/wALySoqFzdJDLc8U8pTLhbUaoLOTjkwnCTKQVprhnISqQqqh/0U5u47IE\nRWzWKN6OHb0CezNTq80Dr6HoxmPCnJHBHn5LinT9AoGAQSpvZpbIIqz8pmTiBl2A\nQQ2gFpcuFeRXPClKYcmbXVLkuhbNL1BzEniFCLAt4LQTaRf9ghLJ3FyCxwVlkpHV\nzV4N6/8hkcTpKOraL38D/dXJSaEFJVVuee/hZl3tVJjEEpA9rDwx7ooLRSdJEJ6M\nciq55UyKBSdt4KssSiDI2RECgYBL3mJ7xuLy5bWfNsrGiVvD/rC+L928/5ZXIXPw\n26oI0Yfun7ulDH4GOroMcDF/GYT/Zzac3h7iapLlR0WYI47xxGI0A//wBZLJ3QIu\nkrxkDo2C9e3Y/NqnHgsbOQR3aWbiDT4wxydZjIeXS3LKA2fl6Hyc90PN3cTEOb8I\nhq2gRQKBgEt0SxhhtyB93SjgTzmUZZ7PiEf0YJatfM6cevmjWHexrZH+x31PB72s\nfH2BQyTKKzoCLB1k/6HRaMnZdrWyWSZ7JKz3AHJ8+58d0Hr8LTrzDM1L6BbjeDct\nN4OiVz1I3rbZGYa396lpxO6ku8yCglisL1yrSP6DdEUp66ntpKVd\n-----END RSA PRIVATE KEY-----')

    def make_expected(self):
        expected = Zone(b'unit.tests.', [])
        source = YamlProvider(b'test', join(dirname(__file__), b'config'))
        source.populate(expected)
        return expected

    def test_init(self):
        with self.assertRaises(Exception) as (ctx):
            TransipProvider(b'test', b'unittest')
        self.assertEquals(str(b'Missing `key` of `key_file` parameter in config'), str(ctx.exception))
        TransipProvider(b'test', b'unittest', key=self.bogus_key)
        TransipProvider(b'test', b'unittest', key_file=b'/fake/path')

    def test_populate(self):
        _expected = self.make_expected()
        with self.assertRaises(WebFault) as (ctx):
            provider = TransipProvider(b'test', b'unittest', self.bogus_key)
            zone = Zone(b'unit.tests.', [])
            provider.populate(zone, True)
        self.assertEquals(str(b'WebFault'), str(ctx.exception.__class__.__name__))
        self.assertEquals(str(b'200'), ctx.exception.fault.faultcode)
        with self.assertRaises(Exception) as (ctx):
            provider = TransipProvider(b'test', b'unittest', self.bogus_key)
            provider._client = MockDomainService(b'unittest', self.bogus_key)
            zone = Zone(b'notfound.unit.tests.', [])
            provider.populate(zone, True)
        self.assertEquals(str(b'TransipNewZoneException'), str(ctx.exception.__class__.__name__))
        self.assertEquals(b'populate: (102) Transip used as target' + b' for non-existing zone: notfound.unit.tests.', text_type(ctx.exception))
        provider = TransipProvider(b'test', b'unittest', self.bogus_key)
        provider._client = MockDomainService(b'unittest', self.bogus_key)
        zone = Zone(b'notfound.unit.tests.', [])
        provider.populate(zone, False)
        provider = TransipProvider(b'test', b'unittest', self.bogus_key)
        provider._client = MockDomainService(b'unittest', self.bogus_key)
        provider._client.mockup(_expected.records)
        zone = Zone(b'unit.tests.', [])
        provider.populate(zone, False)
        provider._currentZone = zone
        self.assertEquals(b'www.unit.tests.', provider._parse_to_fqdn(b'www'))
        self.assertEquals(b'www.unit.tests.', provider._parse_to_fqdn(b'www.unit.tests.'))
        self.assertEquals(b'www.sub.sub.sub.unit.tests.', provider._parse_to_fqdn(b'www.sub.sub.sub'))
        self.assertEquals(b'unit.tests.', provider._parse_to_fqdn(b'@'))
        provider = TransipProvider(b'test', b'unittest', self.bogus_key)
        provider._client = MockDomainService(b'unittest', self.bogus_key)
        zone = Zone(b'unit.tests.', [])
        exists = provider.populate(zone, True)
        self.assertTrue(exists, b'populate should return true')

    def test_plan(self):
        _expected = self.make_expected()
        provider = TransipProvider(b'test', b'unittest', self.bogus_key)
        provider._client = MockDomainService(b'unittest', self.bogus_key)
        plan = provider.plan(_expected)
        self.assertEqual(12, plan.change_counts[b'Create'])
        self.assertEqual(0, plan.change_counts[b'Update'])
        self.assertEqual(0, plan.change_counts[b'Delete'])

    def test_apply(self):
        _expected = self.make_expected()
        provider = TransipProvider(b'test', b'unittest', self.bogus_key)
        provider._client = MockDomainService(b'unittest', self.bogus_key)
        plan = provider.plan(_expected)
        self.assertEqual(12, len(plan.changes))
        changes = provider.apply(plan)
        self.assertEqual(changes, len(plan.changes))
        changes = []
        with self.assertRaises(Exception) as (ctx):
            provider = TransipProvider(b'test', b'unittest', self.bogus_key)
            provider._client = MockDomainService(b'unittest', self.bogus_key)
            plan = provider.plan(_expected)
            plan.desired.name = b'notfound.unit.tests.'
            changes = provider.apply(plan)
        self.assertEqual([], changes)
        self.assertEquals(str(b'WebFault'), str(ctx.exception.__class__.__name__))
        self.assertEquals(str(b'102'), ctx.exception.fault.faultcode)
        _expected = self.make_expected()
        changes = []
        with self.assertRaises(Exception) as (ctx):
            provider = TransipProvider(b'test', b'unittest', self.bogus_key)
            provider._client = MockDomainService(b'unittest', self.bogus_key)
            plan = provider.plan(_expected)
            plan.desired.name = b'failsetdns.unit.tests.'
            changes = provider.apply(plan)
        self.assertEqual([], changes)
        self.assertEquals(str(b'TransipException'), str(ctx.exception.__class__.__name__))