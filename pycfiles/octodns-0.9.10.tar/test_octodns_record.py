# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_record.py
# Compiled at: 2020-04-03 09:42:50
from __future__ import absolute_import, division, print_function, unicode_literals
from six import text_type
from unittest import TestCase
from octodns.record import ARecord, AaaaRecord, AliasRecord, CaaRecord, CaaValue, CnameRecord, Create, Delete, GeoValue, MxRecord, MxValue, NaptrRecord, NaptrValue, NsRecord, PtrRecord, Record, SshfpRecord, SshfpValue, SpfRecord, SrvRecord, SrvValue, TxtRecord, Update, ValidationError, _Dynamic, _DynamicPool, _DynamicRule
from octodns.zone import Zone
from helpers import DynamicProvider, GeoProvider, SimpleProvider

class TestRecord(TestCase):
    zone = Zone(b'unit.tests.', [])

    def test_lowering(self):
        record = ARecord(self.zone, b'MiXeDcAsE', {b'ttl': 30, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        self.assertEquals(b'mixedcase', record.name)

    def test_alias_lowering_value(self):
        upper_record = AliasRecord(self.zone, b'aliasUppwerValue', {b'ttl': 30, 
           b'type': b'ALIAS', 
           b'value': b'GITHUB.COM'})
        lower_record = AliasRecord(self.zone, b'aliasLowerValue', {b'ttl': 30, 
           b'type': b'ALIAS', 
           b'value': b'github.com'})
        self.assertEquals(upper_record.value, lower_record.value)

    def test_cname_lowering_value(self):
        upper_record = CnameRecord(self.zone, b'CnameUppwerValue', {b'ttl': 30, 
           b'type': b'CNAME', 
           b'value': b'GITHUB.COM'})
        lower_record = CnameRecord(self.zone, b'CnameLowerValue', {b'ttl': 30, 
           b'type': b'CNAME', 
           b'value': b'github.com'})
        self.assertEquals(upper_record.value, lower_record.value)

    def test_ptr_lowering_value(self):
        upper_record = PtrRecord(self.zone, b'PtrUppwerValue', {b'ttl': 30, 
           b'type': b'PTR', 
           b'value': b'GITHUB.COM'})
        lower_record = PtrRecord(self.zone, b'PtrLowerValue', {b'ttl': 30, 
           b'type': b'PTR', 
           b'value': b'github.com'})
        self.assertEquals(upper_record.value, lower_record.value)

    def test_a_and_record(self):
        a_values = [
         b'1.2.3.4', b'2.2.3.4']
        a_data = {b'ttl': 30, b'values': a_values}
        a = ARecord(self.zone, b'a', a_data)
        self.assertEquals(b'a', a.name)
        self.assertEquals(b'a.unit.tests.', a.fqdn)
        self.assertEquals(30, a.ttl)
        self.assertEquals(a_values, a.values)
        self.assertEquals(a_data, a.data)
        b_value = b'3.2.3.4'
        b_data = {b'ttl': 30, b'value': b_value}
        b = ARecord(self.zone, b'b', b_data)
        self.assertEquals([b_value], b.values)
        self.assertEquals(b_data, b.data)
        data = {b'ttl': 30, b'value': b'4.2.3.4'}
        self.assertEquals(self.zone.name, ARecord(self.zone, b'', data).fqdn)
        self.assertEquals(self.zone.name, ARecord(self.zone, None, data).fqdn)
        self.assertTrue(a == a)
        self.assertFalse(a == b)
        self.assertTrue(a == ARecord(self.zone, b'a', {b'ttl': 31, b'values': a_values}))
        self.assertTrue(a == ARecord(self.zone, b'a', {b'ttl': 30, b'value': b_value}))
        target = SimpleProvider()
        self.assertFalse(a.changes(a, target))
        other = ARecord(self.zone, b'a', {b'ttl': 30, b'values': a_values})
        self.assertFalse(a.changes(other, target))
        other.ttl = 31
        update = a.changes(other, target)
        self.assertEquals(a, update.existing)
        self.assertEquals(other, update.new)
        other.ttl = a.ttl
        other.values = [b'4.4.4.4']
        update = a.changes(other, target)
        self.assertEquals(a, update.existing)
        self.assertEquals(other, update.new)
        records = set()
        records.add(a)
        self.assertTrue(a in records)
        self.assertFalse(b in records)
        records.add(b)
        self.assertTrue(b in records)
        a.__repr__()
        with self.assertRaises(NotImplementedError):

            class DummyRecord(Record):

                def __init__(self):
                    pass

            DummyRecord().__repr__()
        return

    def test_values_mixin_data(self):
        a = ARecord(self.zone, b'', {b'type': b'A', 
           b'ttl': 600, 
           b'values': []})
        self.assertNotIn(b'values', a.data)
        b = ARecord(self.zone, b'', {b'type': b'A', 
           b'ttl': 600, 
           b'values': [
                     b'']})
        self.assertNotIn(b'value', b.data)
        c = ARecord(self.zone, b'', {b'type': b'A', 
           b'ttl': 600, 
           b'values': [
                     b'', None]})
        self.assertNotIn(b'values', c.data)
        c = ARecord(self.zone, b'', {b'type': b'A', 
           b'ttl': 600, 
           b'values': [
                     b'', None, b'10.10.10.10']})
        self.assertNotIn(b'values', c.data)
        self.assertEqual(b'10.10.10.10', c.data[b'value'])
        return

    def test_value_mixin_data(self):
        a = AliasRecord(self.zone, b'', {b'type': b'ALIAS', 
           b'ttl': 600, 
           b'value': None})
        self.assertNotIn(b'value', a.data)
        a = AliasRecord(self.zone, b'', {b'type': b'ALIAS', 
           b'ttl': 600, 
           b'value': b''})
        self.assertNotIn(b'value', a.data)
        return

    def test_geo(self):
        geo_data = {b'ttl': 42, b'values': [b'5.2.3.4', b'6.2.3.4'], b'geo': {b'AF': [b'1.1.1.1'], b'AS-JP': [
                             b'2.2.2.2', b'3.3.3.3'], 
                    b'NA-US': [
                             b'4.4.4.4', b'5.5.5.5'], 
                    b'NA-US-CA': [
                                b'6.6.6.6', b'7.7.7.7']}}
        geo = ARecord(self.zone, b'geo', geo_data)
        self.assertEquals(geo_data, geo.data)
        other_data = {b'ttl': 42, b'values': [b'5.2.3.4', b'6.2.3.4'], b'geo': {b'AF': [b'1.1.1.1'], b'AS-JP': [
                             b'2.2.2.2', b'3.3.3.3'], 
                    b'NA-US': [
                             b'4.4.4.4', b'5.5.5.5'], 
                    b'NA-US-CA': [
                                b'6.6.6.6', b'7.7.7.7']}}
        other = ARecord(self.zone, b'geo', other_data)
        self.assertEquals(other_data, other.data)
        simple_target = SimpleProvider()
        geo_target = GeoProvider()
        self.assertFalse(geo.changes(geo, geo_target))
        other.geo[b'AF'].values = [
         b'9.9.9.9']
        self.assertTrue(geo == other)
        self.assertFalse(geo.changes(other, simple_target))
        self.assertTrue(geo.changes(other, geo_target))
        other.geo = {}
        self.assertTrue(geo == other)
        self.assertFalse(geo.changes(other, simple_target))
        self.assertTrue(geo.changes(other, geo_target))
        geo.__repr__()

    def assertMultipleValues(self, _type, a_values, b_value):
        a_data = {b'ttl': 30, b'values': a_values}
        a = _type(self.zone, b'a', a_data)
        self.assertEquals(b'a', a.name)
        self.assertEquals(b'a.unit.tests.', a.fqdn)
        self.assertEquals(30, a.ttl)
        self.assertEquals(a_values, a.values)
        self.assertEquals(a_data, a.data)
        b_data = {b'ttl': 30, b'value': b_value}
        b = _type(self.zone, b'b', b_data)
        self.assertEquals([b_value], b.values)
        self.assertEquals(b_data, b.data)

    def test_aaaa(self):
        a_values = [
         b'2001:0db8:3c4d:0015:0000:0000:1a2f:1a2b',
         b'2001:0db8:3c4d:0015:0000:0000:1a2f:1a3b']
        b_value = b'2001:0db8:3c4d:0015:0000:0000:1a2f:1a4b'
        self.assertMultipleValues(AaaaRecord, a_values, b_value)

    def assertSingleValue(self, _type, a_value, b_value):
        a_data = {b'ttl': 30, b'value': a_value}
        a = _type(self.zone, b'a', a_data)
        self.assertEquals(b'a', a.name)
        self.assertEquals(b'a.unit.tests.', a.fqdn)
        self.assertEquals(30, a.ttl)
        self.assertEquals(a_value, a.value)
        self.assertEquals(a_data, a.data)
        b_data = {b'ttl': 30, b'value': b_value}
        b = _type(self.zone, b'b', b_data)
        self.assertEquals(b_value, b.value)
        self.assertEquals(b_data, b.data)
        target = SimpleProvider()
        self.assertFalse(a.changes(a, target))
        other = _type(self.zone, b'a', {b'ttl': 30, b'value': b_value})
        change = a.changes(other, target)
        self.assertEqual(change.existing, a)
        self.assertEqual(change.new, other)
        a.__repr__()

    def test_alias(self):
        a_data = {b'ttl': 0, b'value': b'www.unit.tests.'}
        a = AliasRecord(self.zone, b'', a_data)
        self.assertEquals(b'', a.name)
        self.assertEquals(b'unit.tests.', a.fqdn)
        self.assertEquals(0, a.ttl)
        self.assertEquals(a_data[b'value'], a.value)
        self.assertEquals(a_data, a.data)
        target = SimpleProvider()
        self.assertFalse(a.changes(a, target))
        other = AliasRecord(self.zone, b'a', a_data)
        other.value = b'foo.unit.tests.'
        change = a.changes(other, target)
        self.assertEqual(change.existing, a)
        self.assertEqual(change.new, other)
        a.__repr__()

    def test_caa(self):
        a_values = [
         {b'flags': 0, 
            b'tag': b'issue', 
            b'value': b'ca.example.net'},
         {b'flags': 128, 
            b'tag': b'iodef', 
            b'value': b'mailto:security@example.com'}]
        a_data = {b'ttl': 30, b'values': a_values}
        a = CaaRecord(self.zone, b'a', a_data)
        self.assertEquals(b'a', a.name)
        self.assertEquals(b'a.unit.tests.', a.fqdn)
        self.assertEquals(30, a.ttl)
        self.assertEquals(a_values[0][b'flags'], a.values[0].flags)
        self.assertEquals(a_values[0][b'tag'], a.values[0].tag)
        self.assertEquals(a_values[0][b'value'], a.values[0].value)
        self.assertEquals(a_values[1][b'flags'], a.values[1].flags)
        self.assertEquals(a_values[1][b'tag'], a.values[1].tag)
        self.assertEquals(a_values[1][b'value'], a.values[1].value)
        self.assertEquals(a_data, a.data)
        b_value = {b'tag': b'iodef', 
           b'value': b'http://iodef.example.com/'}
        b_data = {b'ttl': 30, b'value': b_value}
        b = CaaRecord(self.zone, b'b', b_data)
        self.assertEquals(0, b.values[0].flags)
        self.assertEquals(b_value[b'tag'], b.values[0].tag)
        self.assertEquals(b_value[b'value'], b.values[0].value)
        b_data[b'value'][b'flags'] = 0
        self.assertEquals(b_data, b.data)
        target = SimpleProvider()
        self.assertFalse(a.changes(a, target))
        other = CaaRecord(self.zone, b'a', {b'ttl': 30, b'values': a_values})
        other.values[0].flags = 128
        change = a.changes(other, target)
        self.assertEqual(change.existing, a)
        self.assertEqual(change.new, other)
        other.values[0].flags = a.values[0].flags
        other.values[0].tag = b'foo'
        change = a.changes(other, target)
        self.assertEqual(change.existing, a)
        self.assertEqual(change.new, other)
        other.values[0].tag = a.values[0].tag
        other.values[0].value = b'bar'
        change = a.changes(other, target)
        self.assertEqual(change.existing, a)
        self.assertEqual(change.new, other)
        a.__repr__()

    def test_cname(self):
        self.assertSingleValue(CnameRecord, b'target.foo.com.', b'other.foo.com.')

    def test_mx(self):
        a_values = [
         {b'preference': 10, 
            b'exchange': b'smtp1.'},
         {b'priority': 20, 
            b'value': b'smtp2.'}]
        a_data = {b'ttl': 30, b'values': a_values}
        a = MxRecord(self.zone, b'a', a_data)
        self.assertEquals(b'a', a.name)
        self.assertEquals(b'a.unit.tests.', a.fqdn)
        self.assertEquals(30, a.ttl)
        self.assertEquals(a_values[0][b'preference'], a.values[0].preference)
        self.assertEquals(a_values[0][b'exchange'], a.values[0].exchange)
        self.assertEquals(a_values[1][b'priority'], a.values[1].preference)
        self.assertEquals(a_values[1][b'value'], a.values[1].exchange)
        a_data[b'values'][1] = {b'preference': 20, 
           b'exchange': b'smtp2.'}
        self.assertEquals(a_data, a.data)
        b_value = {b'preference': 0, 
           b'exchange': b'smtp3.'}
        b_data = {b'ttl': 30, b'value': b_value}
        b = MxRecord(self.zone, b'b', b_data)
        self.assertEquals(b_value[b'preference'], b.values[0].preference)
        self.assertEquals(b_value[b'exchange'], b.values[0].exchange)
        self.assertEquals(b_data, b.data)
        a_upper_values = [
         {b'preference': 10, 
            b'exchange': b'SMTP1.'},
         {b'priority': 20, 
            b'value': b'SMTP2.'}]
        a_upper_data = {b'ttl': 30, b'values': a_upper_values}
        a_upper = MxRecord(self.zone, b'a', a_upper_data)
        self.assertEquals(a_upper.data, a.data)
        target = SimpleProvider()
        self.assertFalse(a.changes(a, target))
        other = MxRecord(self.zone, b'a', {b'ttl': 30, b'values': a_values})
        other.values[0].preference = 22
        change = a.changes(other, target)
        self.assertEqual(change.existing, a)
        self.assertEqual(change.new, other)
        other.values[0].preference = a.values[0].preference
        other.values[0].exchange = b'smtpX'
        change = a.changes(other, target)
        self.assertEqual(change.existing, a)
        self.assertEqual(change.new, other)
        a.__repr__()

    def test_naptr(self):
        a_values = [
         {b'order': 10, 
            b'preference': 11, 
            b'flags': b'X', 
            b'service': b'Y', 
            b'regexp': b'Z', 
            b'replacement': b'.'},
         {b'order': 20, 
            b'preference': 21, 
            b'flags': b'A', 
            b'service': b'B', 
            b'regexp': b'C', 
            b'replacement': b'foo.com'}]
        a_data = {b'ttl': 30, b'values': a_values}
        a = NaptrRecord(self.zone, b'a', a_data)
        self.assertEquals(b'a', a.name)
        self.assertEquals(b'a.unit.tests.', a.fqdn)
        self.assertEquals(30, a.ttl)
        for i in (0, 1):
            for k in a_values[0].keys():
                self.assertEquals(a_values[i][k], getattr(a.values[i], k))

        self.assertEquals(a_data, a.data)
        b_value = {b'order': 30, 
           b'preference': 31, 
           b'flags': b'M', 
           b'service': b'N', 
           b'regexp': b'O', 
           b'replacement': b'x'}
        b_data = {b'ttl': 30, b'value': b_value}
        b = NaptrRecord(self.zone, b'b', b_data)
        for k in a_values[0].keys():
            self.assertEquals(b_value[k], getattr(b.values[0], k))

        self.assertEquals(b_data, b.data)
        target = SimpleProvider()
        self.assertFalse(a.changes(a, target))
        other = NaptrRecord(self.zone, b'a', {b'ttl': 30, b'values': a_values})
        other.values[0].order = 22
        change = a.changes(other, target)
        self.assertEqual(change.existing, a)
        self.assertEqual(change.new, other)
        other.values[0].order = a.values[0].order
        other.values[0].replacement = b'smtpX'
        change = a.changes(other, target)
        self.assertEqual(change.existing, a)
        self.assertEqual(change.new, other)
        b_naptr_value = b.values[0]
        self.assertTrue(b_naptr_value == b_naptr_value)
        self.assertFalse(b_naptr_value != b_naptr_value)
        self.assertTrue(b_naptr_value <= b_naptr_value)
        self.assertTrue(b_naptr_value >= b_naptr_value)
        self.assertTrue(b_naptr_value > NaptrValue({b'order': 10, 
           b'preference': 31, 
           b'flags': b'M', 
           b'service': b'N', 
           b'regexp': b'O', 
           b'replacement': b'x'}))
        self.assertTrue(b_naptr_value < NaptrValue({b'order': 40, 
           b'preference': 31, 
           b'flags': b'M', 
           b'service': b'N', 
           b'regexp': b'O', 
           b'replacement': b'x'}))
        self.assertTrue(b_naptr_value > NaptrValue({b'order': 30, 
           b'preference': 10, 
           b'flags': b'M', 
           b'service': b'N', 
           b'regexp': b'O', 
           b'replacement': b'x'}))
        self.assertTrue(b_naptr_value < NaptrValue({b'order': 30, 
           b'preference': 40, 
           b'flags': b'M', 
           b'service': b'N', 
           b'regexp': b'O', 
           b'replacement': b'x'}))
        self.assertTrue(b_naptr_value > NaptrValue({b'order': 30, 
           b'preference': 31, 
           b'flags': b'A', 
           b'service': b'N', 
           b'regexp': b'O', 
           b'replacement': b'x'}))
        self.assertTrue(b_naptr_value < NaptrValue({b'order': 30, 
           b'preference': 31, 
           b'flags': b'Z', 
           b'service': b'N', 
           b'regexp': b'O', 
           b'replacement': b'x'}))
        self.assertTrue(b_naptr_value > NaptrValue({b'order': 30, 
           b'preference': 31, 
           b'flags': b'M', 
           b'service': b'A', 
           b'regexp': b'O', 
           b'replacement': b'x'}))
        self.assertTrue(b_naptr_value < NaptrValue({b'order': 30, 
           b'preference': 31, 
           b'flags': b'M', 
           b'service': b'Z', 
           b'regexp': b'O', 
           b'replacement': b'x'}))
        self.assertTrue(b_naptr_value > NaptrValue({b'order': 30, 
           b'preference': 31, 
           b'flags': b'M', 
           b'service': b'N', 
           b'regexp': b'A', 
           b'replacement': b'x'}))
        self.assertTrue(b_naptr_value < NaptrValue({b'order': 30, 
           b'preference': 31, 
           b'flags': b'M', 
           b'service': b'N', 
           b'regexp': b'Z', 
           b'replacement': b'x'}))
        self.assertTrue(b_naptr_value > NaptrValue({b'order': 30, 
           b'preference': 31, 
           b'flags': b'M', 
           b'service': b'N', 
           b'regexp': b'O', 
           b'replacement': b'a'}))
        self.assertTrue(b_naptr_value < NaptrValue({b'order': 30, 
           b'preference': 31, 
           b'flags': b'M', 
           b'service': b'N', 
           b'regexp': b'O', 
           b'replacement': b'z'}))
        a.__repr__()
        v = NaptrValue({b'order': 30, 
           b'preference': 31, 
           b'flags': b'M', 
           b'service': b'N', 
           b'regexp': b'O', 
           b'replacement': b'z'})
        o = NaptrValue({b'order': 30, 
           b'preference': 32, 
           b'flags': b'M', 
           b'service': b'N', 
           b'regexp': b'O', 
           b'replacement': b'z'})
        values = set()
        values.add(v)
        self.assertTrue(v in values)
        self.assertFalse(o in values)
        values.add(o)
        self.assertTrue(o in values)

    def test_ns(self):
        a_values = [
         b'5.6.7.8.', b'6.7.8.9.', b'7.8.9.0.']
        a_data = {b'ttl': 30, b'values': a_values}
        a = NsRecord(self.zone, b'a', a_data)
        self.assertEquals(b'a', a.name)
        self.assertEquals(b'a.unit.tests.', a.fqdn)
        self.assertEquals(30, a.ttl)
        self.assertEquals(a_values, a.values)
        self.assertEquals(a_data, a.data)
        b_value = b'9.8.7.6.'
        b_data = {b'ttl': 30, b'value': b_value}
        b = NsRecord(self.zone, b'b', b_data)
        self.assertEquals([b_value], b.values)
        self.assertEquals(b_data, b.data)

    def test_sshfp(self):
        a_values = [
         {b'algorithm': 10, 
            b'fingerprint_type': 11, 
            b'fingerprint': b'abc123'},
         {b'algorithm': 20, 
            b'fingerprint_type': 21, 
            b'fingerprint': b'def456'}]
        a_data = {b'ttl': 30, b'values': a_values}
        a = SshfpRecord(self.zone, b'a', a_data)
        self.assertEquals(b'a', a.name)
        self.assertEquals(b'a.unit.tests.', a.fqdn)
        self.assertEquals(30, a.ttl)
        self.assertEquals(a_values[0][b'algorithm'], a.values[0].algorithm)
        self.assertEquals(a_values[0][b'fingerprint_type'], a.values[0].fingerprint_type)
        self.assertEquals(a_values[0][b'fingerprint'], a.values[0].fingerprint)
        self.assertEquals(a_data, a.data)
        b_value = {b'algorithm': 30, 
           b'fingerprint_type': 31, 
           b'fingerprint': b'ghi789'}
        b_data = {b'ttl': 30, b'value': b_value}
        b = SshfpRecord(self.zone, b'b', b_data)
        self.assertEquals(b_value[b'algorithm'], b.values[0].algorithm)
        self.assertEquals(b_value[b'fingerprint_type'], b.values[0].fingerprint_type)
        self.assertEquals(b_value[b'fingerprint'], b.values[0].fingerprint)
        self.assertEquals(b_data, b.data)
        target = SimpleProvider()
        self.assertFalse(a.changes(a, target))
        other = SshfpRecord(self.zone, b'a', {b'ttl': 30, b'values': a_values})
        other.values[0].algorithm = 22
        change = a.changes(other, target)
        self.assertEqual(change.existing, a)
        self.assertEqual(change.new, other)
        other = SshfpRecord(self.zone, b'a', {b'ttl': 30, b'values': a_values})
        other.values[0].algorithm = a.values[0].algorithm
        other.values[0].fingerprint_type = 22
        change = a.changes(other, target)
        self.assertEqual(change.existing, a)
        self.assertEqual(change.new, other)
        other = SshfpRecord(self.zone, b'a', {b'ttl': 30, b'values': a_values})
        other.values[0].fingerprint_type = a.values[0].fingerprint_type
        other.values[0].fingerprint = 22
        change = a.changes(other, target)
        self.assertEqual(change.existing, a)
        self.assertEqual(change.new, other)
        a.__repr__()

    def test_spf(self):
        a_values = [
         b'spf1 -all', b'spf1 -hrm']
        b_value = b'spf1 -other'
        self.assertMultipleValues(SpfRecord, a_values, b_value)

    def test_srv(self):
        a_values = [
         {b'priority': 10, 
            b'weight': 11, 
            b'port': 12, 
            b'target': b'server1'},
         {b'priority': 20, 
            b'weight': 21, 
            b'port': 22, 
            b'target': b'server2'}]
        a_data = {b'ttl': 30, b'values': a_values}
        a = SrvRecord(self.zone, b'_a._tcp', a_data)
        self.assertEquals(b'_a._tcp', a.name)
        self.assertEquals(b'_a._tcp.unit.tests.', a.fqdn)
        self.assertEquals(30, a.ttl)
        self.assertEquals(a_values[0][b'priority'], a.values[0].priority)
        self.assertEquals(a_values[0][b'weight'], a.values[0].weight)
        self.assertEquals(a_values[0][b'port'], a.values[0].port)
        self.assertEquals(a_values[0][b'target'], a.values[0].target)
        self.assertEquals(a_data, a.data)
        b_value = {b'priority': 30, 
           b'weight': 31, 
           b'port': 32, 
           b'target': b'server3'}
        b_data = {b'ttl': 30, b'value': b_value}
        b = SrvRecord(self.zone, b'_b._tcp', b_data)
        self.assertEquals(b_value[b'priority'], b.values[0].priority)
        self.assertEquals(b_value[b'weight'], b.values[0].weight)
        self.assertEquals(b_value[b'port'], b.values[0].port)
        self.assertEquals(b_value[b'target'], b.values[0].target)
        self.assertEquals(b_data, b.data)
        target = SimpleProvider()
        self.assertFalse(a.changes(a, target))
        other = SrvRecord(self.zone, b'_a._icmp', {b'ttl': 30, b'values': a_values})
        other.values[0].priority = 22
        change = a.changes(other, target)
        self.assertEqual(change.existing, a)
        self.assertEqual(change.new, other)
        other.values[0].priority = a.values[0].priority
        other.values[0].weight = 33
        change = a.changes(other, target)
        self.assertEqual(change.existing, a)
        self.assertEqual(change.new, other)
        other.values[0].weight = a.values[0].weight
        other.values[0].port = 44
        change = a.changes(other, target)
        self.assertEqual(change.existing, a)
        self.assertEqual(change.new, other)
        other.values[0].port = a.values[0].port
        other.values[0].target = b'serverX'
        change = a.changes(other, target)
        self.assertEqual(change.existing, a)
        self.assertEqual(change.new, other)
        a.__repr__()

    def test_txt(self):
        a_values = [
         b'a one', b'a two']
        b_value = b'b other'
        self.assertMultipleValues(TxtRecord, a_values, b_value)

    def test_record_new(self):
        txt = Record.new(self.zone, b'txt', {b'ttl': 44, 
           b'type': b'TXT', 
           b'value': b'some text'})
        self.assertIsInstance(txt, TxtRecord)
        self.assertEquals(b'TXT', txt._type)
        self.assertEquals([b'some text'], txt.values)
        with self.assertRaises(Exception) as (ctx):
            Record.new(self.zone, b'unknown', {})
        self.assertTrue(b'missing type' in text_type(ctx.exception))
        with self.assertRaises(Exception) as (ctx):
            Record.new(self.zone, b'unknown', {b'type': b'XXX'})
        self.assertTrue(b'Unknown record type' in text_type(ctx.exception))

    def test_change(self):
        existing = Record.new(self.zone, b'txt', {b'ttl': 44, 
           b'type': b'TXT', 
           b'value': b'some text'})
        new = Record.new(self.zone, b'txt', {b'ttl': 44, 
           b'type': b'TXT', 
           b'value': b'some change'})
        create = Create(new)
        self.assertEquals(new.values, create.record.values)
        update = Update(existing, new)
        self.assertEquals(new.values, update.record.values)
        delete = Delete(existing)
        self.assertEquals(existing.values, delete.record.values)

    def test_geo_value(self):
        code = b'NA-US-CA'
        values = [b'1.2.3.4']
        geo = GeoValue(code, values)
        self.assertEquals(code, geo.code)
        self.assertEquals(b'NA', geo.continent_code)
        self.assertEquals(b'US', geo.country_code)
        self.assertEquals(b'CA', geo.subdivision_code)
        self.assertEquals(values, geo.values)
        self.assertEquals([b'NA-US', b'NA'], list(geo.parents))
        a = GeoValue(b'NA-US-CA', values)
        b = GeoValue(b'AP-JP', values)
        c = GeoValue(b'NA-US-CA', [b'2.3.4.5'])
        self.assertEqual(a, a)
        self.assertEqual(b, b)
        self.assertEqual(c, c)
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(b, a)
        self.assertNotEqual(b, c)
        self.assertNotEqual(c, a)
        self.assertNotEqual(c, b)
        self.assertTrue(a > b)
        self.assertTrue(a < c)
        self.assertTrue(b < a)
        self.assertTrue(b < c)
        self.assertTrue(c > a)
        self.assertTrue(c > b)
        self.assertTrue(a >= a)
        self.assertTrue(a >= b)
        self.assertTrue(a <= c)
        self.assertTrue(b <= a)
        self.assertTrue(b <= b)
        self.assertTrue(b <= c)
        self.assertTrue(c > a)
        self.assertTrue(c > b)
        self.assertTrue(c >= b)

    def test_healthcheck(self):
        new = Record.new(self.zone, b'a', {b'ttl': 44, 
           b'type': b'A', 
           b'value': b'1.2.3.4', 
           b'octodns': {b'healthcheck': {b'path': b'/_ready', 
                                         b'host': b'bleep.bloop', 
                                         b'protocol': b'HTTP', 
                                         b'port': 8080}}})
        self.assertEquals(b'/_ready', new.healthcheck_path)
        self.assertEquals(b'bleep.bloop', new.healthcheck_host)
        self.assertEquals(b'HTTP', new.healthcheck_protocol)
        self.assertEquals(8080, new.healthcheck_port)
        new = Record.new(self.zone, b'a', {b'ttl': 44, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        self.assertEquals(b'/_dns', new.healthcheck_path)
        self.assertEquals(b'a.unit.tests', new.healthcheck_host)
        self.assertEquals(b'HTTPS', new.healthcheck_protocol)
        self.assertEquals(443, new.healthcheck_port)

    def test_inored(self):
        new = Record.new(self.zone, b'txt', {b'ttl': 44, 
           b'type': b'TXT', 
           b'value': b'some change', 
           b'octodns': {b'ignored': True}})
        self.assertTrue(new.ignored)
        new = Record.new(self.zone, b'txt', {b'ttl': 44, 
           b'type': b'TXT', 
           b'value': b'some change', 
           b'octodns': {b'ignored': False}})
        self.assertFalse(new.ignored)
        new = Record.new(self.zone, b'txt', {b'ttl': 44, 
           b'type': b'TXT', 
           b'value': b'some change'})
        self.assertFalse(new.ignored)

    def test_ordering_functions(self):
        a = Record.new(self.zone, b'a', {b'ttl': 44, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        b = Record.new(self.zone, b'b', {b'ttl': 44, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        c = Record.new(self.zone, b'c', {b'ttl': 44, 
           b'type': b'A', 
           b'value': b'1.2.3.4'})
        aaaa = Record.new(self.zone, b'a', {b'ttl': 44, 
           b'type': b'AAAA', 
           b'value': b'2601:644:500:e210:62f8:1dff:feb8:947a'})
        self.assertEquals(a, a)
        self.assertEquals(b, b)
        self.assertEquals(c, c)
        self.assertEquals(aaaa, aaaa)
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, aaaa)
        self.assertNotEqual(b, a)
        self.assertNotEqual(b, c)
        self.assertNotEqual(b, aaaa)
        self.assertNotEqual(c, a)
        self.assertNotEqual(c, b)
        self.assertNotEqual(c, aaaa)
        self.assertNotEqual(aaaa, a)
        self.assertNotEqual(aaaa, b)
        self.assertNotEqual(aaaa, c)
        self.assertTrue(a < b)
        self.assertTrue(a < c)
        self.assertTrue(a < aaaa)
        self.assertTrue(b > a)
        self.assertTrue(b < c)
        self.assertTrue(b > aaaa)
        self.assertTrue(c > a)
        self.assertTrue(c > b)
        self.assertTrue(c > aaaa)
        self.assertTrue(aaaa > a)
        self.assertTrue(aaaa < b)
        self.assertTrue(aaaa < c)
        self.assertTrue(a <= a)
        self.assertTrue(a <= b)
        self.assertTrue(a <= c)
        self.assertTrue(a <= aaaa)
        self.assertTrue(b >= a)
        self.assertTrue(b >= b)
        self.assertTrue(b <= c)
        self.assertTrue(b >= aaaa)
        self.assertTrue(c >= a)
        self.assertTrue(c >= b)
        self.assertTrue(c >= c)
        self.assertTrue(c >= aaaa)
        self.assertTrue(aaaa >= a)
        self.assertTrue(aaaa <= b)
        self.assertTrue(aaaa <= c)
        self.assertTrue(aaaa <= aaaa)

    def test_caa_value(self):
        a = CaaValue({b'flags': 0, b'tag': b'a', b'value': b'v'})
        b = CaaValue({b'flags': 1, b'tag': b'a', b'value': b'v'})
        c = CaaValue({b'flags': 0, b'tag': b'c', b'value': b'v'})
        d = CaaValue({b'flags': 0, b'tag': b'a', b'value': b'z'})
        self.assertEqual(a, a)
        self.assertEqual(b, b)
        self.assertEqual(c, c)
        self.assertEqual(d, d)
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, d)
        self.assertNotEqual(b, a)
        self.assertNotEqual(b, c)
        self.assertNotEqual(b, d)
        self.assertNotEqual(c, a)
        self.assertNotEqual(c, b)
        self.assertNotEqual(c, d)
        self.assertTrue(a < b)
        self.assertTrue(a < c)
        self.assertTrue(a < d)
        self.assertTrue(b > a)
        self.assertTrue(b > c)
        self.assertTrue(b > d)
        self.assertTrue(c > a)
        self.assertTrue(c < b)
        self.assertTrue(c > d)
        self.assertTrue(d > a)
        self.assertTrue(d < b)
        self.assertTrue(d < c)
        self.assertTrue(a <= b)
        self.assertTrue(a <= c)
        self.assertTrue(a <= d)
        self.assertTrue(a <= a)
        self.assertTrue(a >= a)
        self.assertTrue(b >= a)
        self.assertTrue(b >= c)
        self.assertTrue(b >= d)
        self.assertTrue(b >= b)
        self.assertTrue(b <= b)
        self.assertTrue(c >= a)
        self.assertTrue(c <= b)
        self.assertTrue(c >= d)
        self.assertTrue(c >= c)
        self.assertTrue(c <= c)
        self.assertTrue(d >= a)
        self.assertTrue(d <= b)
        self.assertTrue(d <= c)
        self.assertTrue(d >= d)
        self.assertTrue(d <= d)

    def test_mx_value(self):
        a = MxValue({b'preference': 0, b'priority': b'a', b'exchange': b'v', b'value': b'1'})
        b = MxValue({b'preference': 10, b'priority': b'a', b'exchange': b'v', b'value': b'2'})
        c = MxValue({b'preference': 0, b'priority': b'b', b'exchange': b'z', b'value': b'3'})
        self.assertEqual(a, a)
        self.assertEqual(b, b)
        self.assertEqual(c, c)
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(b, a)
        self.assertNotEqual(b, c)
        self.assertNotEqual(c, a)
        self.assertNotEqual(c, b)
        self.assertTrue(a < b)
        self.assertTrue(a < c)
        self.assertTrue(b > a)
        self.assertTrue(b > c)
        self.assertTrue(c > a)
        self.assertTrue(c < b)
        self.assertTrue(a <= b)
        self.assertTrue(a <= c)
        self.assertTrue(a <= a)
        self.assertTrue(a >= a)
        self.assertTrue(b >= a)
        self.assertTrue(b >= c)
        self.assertTrue(b >= b)
        self.assertTrue(b <= b)
        self.assertTrue(c >= a)
        self.assertTrue(c <= b)
        self.assertTrue(c >= c)
        self.assertTrue(c <= c)

    def test_sshfp_value(self):
        a = SshfpValue({b'algorithm': 0, b'fingerprint_type': 0, b'fingerprint': b'abcd'})
        b = SshfpValue({b'algorithm': 1, b'fingerprint_type': 0, b'fingerprint': b'abcd'})
        c = SshfpValue({b'algorithm': 0, b'fingerprint_type': 1, b'fingerprint': b'abcd'})
        d = SshfpValue({b'algorithm': 0, b'fingerprint_type': 0, b'fingerprint': b'bcde'})
        self.assertEqual(a, a)
        self.assertEqual(b, b)
        self.assertEqual(c, c)
        self.assertEqual(d, d)
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, d)
        self.assertNotEqual(b, a)
        self.assertNotEqual(b, c)
        self.assertNotEqual(b, d)
        self.assertNotEqual(c, a)
        self.assertNotEqual(c, b)
        self.assertNotEqual(c, d)
        self.assertNotEqual(d, a)
        self.assertNotEqual(d, b)
        self.assertNotEqual(d, c)
        self.assertTrue(a < b)
        self.assertTrue(a < c)
        self.assertTrue(b > a)
        self.assertTrue(b > c)
        self.assertTrue(c > a)
        self.assertTrue(c < b)
        self.assertTrue(a <= b)
        self.assertTrue(a <= c)
        self.assertTrue(a <= a)
        self.assertTrue(a >= a)
        self.assertTrue(b >= a)
        self.assertTrue(b >= c)
        self.assertTrue(b >= b)
        self.assertTrue(b <= b)
        self.assertTrue(c >= a)
        self.assertTrue(c <= b)
        self.assertTrue(c >= c)
        self.assertTrue(c <= c)
        values = set()
        values.add(a)
        self.assertTrue(a in values)
        self.assertFalse(b in values)
        values.add(b)
        self.assertTrue(b in values)

    def test_srv_value(self):
        a = SrvValue({b'priority': 0, b'weight': 0, b'port': 0, b'target': b'foo.'})
        b = SrvValue({b'priority': 1, b'weight': 0, b'port': 0, b'target': b'foo.'})
        c = SrvValue({b'priority': 0, b'weight': 2, b'port': 0, b'target': b'foo.'})
        d = SrvValue({b'priority': 0, b'weight': 0, b'port': 3, b'target': b'foo.'})
        e = SrvValue({b'priority': 0, b'weight': 0, b'port': 0, b'target': b'mmm.'})
        self.assertEqual(a, a)
        self.assertEqual(b, b)
        self.assertEqual(c, c)
        self.assertEqual(d, d)
        self.assertEqual(e, e)
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, d)
        self.assertNotEqual(a, e)
        self.assertNotEqual(b, a)
        self.assertNotEqual(b, c)
        self.assertNotEqual(b, d)
        self.assertNotEqual(b, e)
        self.assertNotEqual(c, a)
        self.assertNotEqual(c, b)
        self.assertNotEqual(c, d)
        self.assertNotEqual(c, e)
        self.assertNotEqual(d, a)
        self.assertNotEqual(d, b)
        self.assertNotEqual(d, c)
        self.assertNotEqual(d, e)
        self.assertNotEqual(e, a)
        self.assertNotEqual(e, b)
        self.assertNotEqual(e, c)
        self.assertNotEqual(e, d)
        self.assertTrue(a < b)
        self.assertTrue(a < c)
        self.assertTrue(b > a)
        self.assertTrue(b > c)
        self.assertTrue(c > a)
        self.assertTrue(c < b)
        self.assertTrue(a <= b)
        self.assertTrue(a <= c)
        self.assertTrue(a <= a)
        self.assertTrue(a >= a)
        self.assertTrue(b >= a)
        self.assertTrue(b >= c)
        self.assertTrue(b >= b)
        self.assertTrue(b <= b)
        self.assertTrue(c >= a)
        self.assertTrue(c <= b)
        self.assertTrue(c >= c)
        self.assertTrue(c <= c)
        values = set()
        values.add(a)
        self.assertTrue(a in values)
        self.assertFalse(b in values)
        values.add(b)
        self.assertTrue(b in values)


class TestRecordValidation(TestCase):
    zone = Zone(b'unit.tests.', [])

    def test_base(self):
        with self.assertRaises(ValidationError) as (ctx):
            name = b'x' * (253 - len(self.zone.name))
            Record.new(self.zone, name, {b'ttl': 300, 
               b'type': b'A', 
               b'value': b'1.2.3.4'})
        reason = ctx.exception.reasons[0]
        self.assertTrue(reason.startswith(b'invalid fqdn, "xxxx'))
        self.assertTrue(reason.endswith(b'.unit.tests." is too long at 254 chars, max is 253'))
        with self.assertRaises(ValidationError) as (ctx):
            name = b'x' * 64
            Record.new(self.zone, name, {b'ttl': 300, 
               b'type': b'A', 
               b'value': b'1.2.3.4'})
        reason = ctx.exception.reasons[0]
        self.assertTrue(reason.startswith(b'invalid name, "xxxx'))
        self.assertTrue(reason.endswith(b'xxx" is too long at 64 chars, max is 63'))
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'A', 
               b'value': b'1.2.3.4'})
        self.assertEquals([b'missing ttl'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'www', {b'type': b'A', 
               b'ttl': -1, 
               b'value': b'1.2.3.4'})
        self.assertEquals(b'www.unit.tests.', ctx.exception.fqdn)
        self.assertEquals([b'invalid ttl'], ctx.exception.reasons)
        Record.new(self.zone, b'www', {b'type': b'A', 
           b'ttl': -1, 
           b'value': b'1.2.3.4'}, lenient=True)
        with self.assertRaises(KeyError) as (ctx):
            Record.new(self.zone, b'www', {b'type': b'A', 
               b'ttl': -1}, lenient=True)
        self.assertEquals(('value', ), ctx.exception.args)
        Record.new(self.zone, b'www', {b'octodns': {b'lenient': True}, 
           b'type': b'A', 
           b'ttl': -1, 
           b'value': b'1.2.3.4'}, lenient=True)

    def test_A_and_values_mixin(self):
        Record.new(self.zone, b'', {b'type': b'A', 
           b'ttl': 600, 
           b'value': b'1.2.3.4'})
        Record.new(self.zone, b'', {b'type': b'A', 
           b'ttl': 600, 
           b'values': [
                     b'1.2.3.4']})
        Record.new(self.zone, b'', {b'type': b'A', 
           b'ttl': 600, 
           b'values': [
                     b'1.2.3.4',
                     b'1.2.3.5']})
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'A', 
               b'ttl': 600})
        self.assertEquals([b'missing value(s)'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'www', {b'type': b'A', 
               b'ttl': 600, 
               b'values': []})
        self.assertEquals([b'missing value(s)'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'www', {b'type': b'A', 
               b'ttl': 600, 
               b'values': None})
        self.assertEquals([b'missing value(s)'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'www', {b'type': b'A', 
               b'ttl': 600, 
               b'values': [
                         None, b'']})
        self.assertEquals([b'missing value(s)',
         b'empty value'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'www', {b'type': b'A', 
               b'ttl': 600, 
               b'value': None})
        self.assertEquals([b'missing value(s)'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'www', {b'type': b'A', 
               b'ttl': 600, 
               b'value': b''})
        self.assertEquals([b'empty value'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'A'})
        self.assertEquals([b'missing ttl', b'missing value(s)'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'A', 
               b'ttl': 600, 
               b'value': b'hello'})
        self.assertEquals([b'invalid IPv4 address "hello"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'A', 
               b'ttl': 600, 
               b'values': [
                         b'hello', b'goodbye']})
        self.assertEquals([
         b'invalid IPv4 address "hello"',
         b'invalid IPv4 address "goodbye"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'A', 
               b'values': [
                         b'1.2.3.4', b'hello', b'5.6.7.8']})
        self.assertEquals([
         b'missing ttl',
         b'invalid IPv4 address "hello"'], ctx.exception.reasons)
        return

    def test_AAAA_validation(self):
        Record.new(self.zone, b'', {b'type': b'AAAA', 
           b'ttl': 600, 
           b'value': b'2601:644:500:e210:62f8:1dff:feb8:947a'})
        Record.new(self.zone, b'', {b'type': b'AAAA', 
           b'ttl': 600, 
           b'values': [
                     b'2601:644:500:e210:62f8:1dff:feb8:947a']})
        Record.new(self.zone, b'', {b'type': b'AAAA', 
           b'ttl': 600, 
           b'values': [
                     b'2601:644:500:e210:62f8:1dff:feb8:947a',
                     b'2601:642:500:e210:62f8:1dff:feb8:947a']})
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'AAAA', 
               b'ttl': 600})
        self.assertEquals([b'missing value(s)'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'www', {b'type': b'AAAA', 
               b'ttl': 600, 
               b'values': []})
        self.assertEquals([b'missing value(s)'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'www', {b'type': b'AAAA', 
               b'ttl': 600, 
               b'values': None})
        self.assertEquals([b'missing value(s)'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'www', {b'type': b'AAAA', 
               b'ttl': 600, 
               b'values': [
                         None, b'']})
        self.assertEquals([b'missing value(s)',
         b'empty value'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'www', {b'type': b'AAAA', 
               b'ttl': 600, 
               b'value': None})
        self.assertEquals([b'missing value(s)'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'www', {b'type': b'AAAA', 
               b'ttl': 600, 
               b'value': b''})
        self.assertEquals([b'empty value'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'AAAA'})
        self.assertEquals([b'missing ttl', b'missing value(s)'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'AAAA', 
               b'ttl': 600, 
               b'value': b'hello'})
        self.assertEquals([b'invalid IPv6 address "hello"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'AAAA', 
               b'ttl': 600, 
               b'values': [
                         b'hello', b'goodbye']})
        self.assertEquals([
         b'invalid IPv6 address "hello"',
         b'invalid IPv6 address "goodbye"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'AAAA', 
               b'values': [
                         b'2601:644:500:e210:62f8:1dff:feb8:947a',
                         b'hello',
                         b'2601:642:500:e210:62f8:1dff:feb8:947a']})
        self.assertEquals([
         b'missing ttl',
         b'invalid IPv6 address "hello"'], ctx.exception.reasons)
        return

    def test_geo(self):
        Record.new(self.zone, b'', {b'geo': {b'NA': [
                          b'1.2.3.5'], 
                    b'NA-US': [
                             b'1.2.3.5', b'1.2.3.6']}, 
           b'type': b'A', 
           b'ttl': 600, 
           b'value': b'1.2.3.4'})
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'geo': {b'NA': [
                              b'hello'], 
                        b'NA-US': [
                                 b'1.2.3.5', b'1.2.3.6']}, 
               b'type': b'A', 
               b'ttl': 600, 
               b'value': b'1.2.3.4'})
        self.assertEquals([b'invalid IPv4 address "hello"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'geo': {b'XYZ': [
                               b'1.2.3.4']}, 
               b'type': b'A', 
               b'ttl': 600, 
               b'value': b'1.2.3.4'})
        self.assertEquals([b'invalid geo "XYZ"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'geo': {b'NA': [
                              b'hello'], 
                        b'NA-US': [
                                 b'1.2.3.5', b'goodbye']}, 
               b'type': b'A', 
               b'ttl': 600, 
               b'value': b'1.2.3.4'})
        self.assertEquals([
         b'invalid IPv4 address "hello"',
         b'invalid IPv4 address "goodbye"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'a', {b'geo': {b'NA': [
                              b'1.2.3.5'], 
                        b'NA-US': [
                                 b'1.2.3.5', b'1.2.3.6']}, 
               b'type': b'A', 
               b'ttl': 600, 
               b'value': b'1.2.3.4', 
               b'octodns': {b'healthcheck': {b'protocol': b'FTP'}}})
        self.assertEquals([b'invalid healthcheck protocol'], ctx.exception.reasons)

    def test_AAAA(self):
        Record.new(self.zone, b'', {b'type': b'AAAA', 
           b'ttl': 600, 
           b'value': b'2601:644:500:e210:62f8:1dff:feb8:947a'})
        Record.new(self.zone, b'', {b'type': b'AAAA', 
           b'ttl': 600, 
           b'values': [
                     b'2601:644:500:e210:62f8:1dff:feb8:947a',
                     b'2601:644:500:e210:62f8:1dff:feb8:947b']})
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'AAAA', 
               b'ttl': 600, 
               b'value': b'hello'})
        self.assertEquals([b'invalid IPv6 address "hello"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'AAAA', 
               b'ttl': 600, 
               b'values': [
                         b'1.2.3.4',
                         b'2.3.4.5']})
        self.assertEquals([
         b'invalid IPv6 address "1.2.3.4"',
         b'invalid IPv6 address "2.3.4.5"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'AAAA', 
               b'ttl': 600, 
               b'values': [
                         b'hello', b'goodbye']})
        self.assertEquals([
         b'invalid IPv6 address "hello"',
         b'invalid IPv6 address "goodbye"'], ctx.exception.reasons)

    def test_ALIAS_and_value_mixin(self):
        Record.new(self.zone, b'', {b'type': b'ALIAS', 
           b'ttl': 600, 
           b'value': b'foo.bar.com.'})
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'ALIAS', 
               b'ttl': 600})
        self.assertEquals([b'missing value'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'www', {b'type': b'ALIAS', 
               b'ttl': 600, 
               b'value': None})
        self.assertEquals([b'missing value'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'www', {b'type': b'ALIAS', 
               b'ttl': 600, 
               b'value': b''})
        self.assertEquals([b'empty value'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'ALIAS', 
               b'ttl': 600, 
               b'value': b'foo.bar.com'})
        self.assertEquals([b'ALIAS value "foo.bar.com" missing trailing .'], ctx.exception.reasons)
        return

    def test_CAA(self):
        Record.new(self.zone, b'', {b'type': b'CAA', 
           b'ttl': 600, 
           b'value': {b'flags': 128, 
                      b'tag': b'iodef', 
                      b'value': b'http://foo.bar.com/'}})
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'CAA', 
               b'ttl': 600, 
               b'value': {b'flags': -42, 
                          b'tag': b'iodef', 
                          b'value': b'http://foo.bar.com/'}})
        self.assertEquals([b'invalid flags "-42"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'CAA', 
               b'ttl': 600, 
               b'value': {b'flags': 442, 
                          b'tag': b'iodef', 
                          b'value': b'http://foo.bar.com/'}})
        self.assertEquals([b'invalid flags "442"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'CAA', 
               b'ttl': 600, 
               b'value': {b'flags': b'nope', 
                          b'tag': b'iodef', 
                          b'value': b'http://foo.bar.com/'}})
        self.assertEquals([b'invalid flags "nope"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'CAA', 
               b'ttl': 600, 
               b'value': {b'value': b'http://foo.bar.com/'}})
        self.assertEquals([b'missing tag'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'CAA', 
               b'ttl': 600, 
               b'value': {b'tag': b'iodef'}})
        self.assertEquals([b'missing value'], ctx.exception.reasons)

    def test_CNAME(self):
        Record.new(self.zone, b'www', {b'type': b'CNAME', 
           b'ttl': 600, 
           b'value': b'foo.bar.com.'})
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'CNAME', 
               b'ttl': 600, 
               b'value': b'foo.bar.com.'})
        self.assertEquals([b'root CNAME not allowed'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'www', {b'type': b'CNAME', 
               b'ttl': 600, 
               b'value': b'foo.bar.com'})
        self.assertEquals([b'CNAME value "foo.bar.com" missing trailing .'], ctx.exception.reasons)

    def test_MX(self):
        Record.new(self.zone, b'', {b'type': b'MX', 
           b'ttl': 600, 
           b'value': {b'preference': 10, 
                      b'exchange': b'foo.bar.com.'}})
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'MX', 
               b'ttl': 600, 
               b'value': {b'exchange': b'foo.bar.com.'}})
        self.assertEquals([b'missing preference'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'MX', 
               b'ttl': 600, 
               b'value': {b'preference': b'nope', 
                          b'exchange': b'foo.bar.com.'}})
        self.assertEquals([b'invalid preference "nope"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'MX', 
               b'ttl': 600, 
               b'value': {b'preference': 10}})
        self.assertEquals([b'missing exchange'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'MX', 
               b'ttl': 600, 
               b'value': {b'preference': 10, 
                          b'exchange': b'foo.bar.com'}})
        self.assertEquals([b'MX value "foo.bar.com" missing trailing .'], ctx.exception.reasons)

    def test_NXPTR(self):
        Record.new(self.zone, b'', {b'type': b'NAPTR', 
           b'ttl': 600, 
           b'value': {b'order': 10, 
                      b'preference': 20, 
                      b'flags': b'S', 
                      b'service': b'srv', 
                      b'regexp': b'.*', 
                      b'replacement': b'.'}})
        value = {b'order': 10, 
           b'preference': 20, 
           b'flags': b'S', 
           b'service': b'srv', 
           b'regexp': b'.*', 
           b'replacement': b'.'}
        for k in ('order', 'preference', 'flags', 'service', 'regexp', 'replacement'):
            v = dict(value)
            del v[k]
            with self.assertRaises(ValidationError) as (ctx):
                Record.new(self.zone, b'', {b'type': b'NAPTR', 
                   b'ttl': 600, 
                   b'value': v})
            self.assertEquals([(b'missing {}').format(k)], ctx.exception.reasons)

        v = dict(value)
        v[b'order'] = b'boo'
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'NAPTR', 
               b'ttl': 600, 
               b'value': v})
        self.assertEquals([b'invalid order "boo"'], ctx.exception.reasons)
        v = dict(value)
        v[b'preference'] = b'who'
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'NAPTR', 
               b'ttl': 600, 
               b'value': v})
        self.assertEquals([b'invalid preference "who"'], ctx.exception.reasons)
        v = dict(value)
        v[b'flags'] = b'X'
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'NAPTR', 
               b'ttl': 600, 
               b'value': v})
        self.assertEquals([b'unrecognized flags "X"'], ctx.exception.reasons)

    def test_NS(self):
        Record.new(self.zone, b'', {b'type': b'NS', 
           b'ttl': 600, 
           b'values': [
                     b'foo.bar.com.',
                     b'1.2.3.4.']})
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'NS', 
               b'ttl': 600})
        self.assertEquals([b'missing value(s)'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'NS', 
               b'ttl': 600, 
               b'value': b'foo.bar'})
        self.assertEquals([b'NS value "foo.bar" missing trailing .'], ctx.exception.reasons)

    def test_PTR(self):
        Record.new(self.zone, b'', {b'type': b'PTR', 
           b'ttl': 600, 
           b'value': b'foo.bar.com.'})
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'PTR', 
               b'ttl': 600})
        self.assertEquals([b'missing value'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'PTR', 
               b'ttl': 600, 
               b'value': b'foo.bar'})
        self.assertEquals([b'PTR value "foo.bar" missing trailing .'], ctx.exception.reasons)

    def test_SSHFP(self):
        Record.new(self.zone, b'', {b'type': b'SSHFP', 
           b'ttl': 600, 
           b'value': {b'algorithm': 1, 
                      b'fingerprint_type': 1, 
                      b'fingerprint': b'bf6b6825d2977c511a475bbefb88aad54a92ac73'}})
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'SSHFP', 
               b'ttl': 600, 
               b'value': {b'fingerprint_type': 1, 
                          b'fingerprint': b'bf6b6825d2977c511a475bbefb88aad54a92ac73'}})
        self.assertEquals([b'missing algorithm'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'SSHFP', 
               b'ttl': 600, 
               b'value': {b'algorithm': b'nope', 
                          b'fingerprint_type': 2, 
                          b'fingerprint': b'bf6b6825d2977c511a475bbefb88aad54a92ac73'}})
        self.assertEquals([b'invalid algorithm "nope"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'SSHFP', 
               b'ttl': 600, 
               b'value': {b'algorithm': 42, 
                          b'fingerprint_type': 1, 
                          b'fingerprint': b'bf6b6825d2977c511a475bbefb88aad54a92ac73'}})
        self.assertEquals([b'unrecognized algorithm "42"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'SSHFP', 
               b'ttl': 600, 
               b'value': {b'algorithm': 2, 
                          b'fingerprint': b'bf6b6825d2977c511a475bbefb88aad54a92ac73'}})
        self.assertEquals([b'missing fingerprint_type'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'SSHFP', 
               b'ttl': 600, 
               b'value': {b'algorithm': 3, 
                          b'fingerprint_type': b'yeeah', 
                          b'fingerprint': b'bf6b6825d2977c511a475bbefb88aad54a92ac73'}})
        self.assertEquals([b'invalid fingerprint_type "yeeah"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'SSHFP', 
               b'ttl': 600, 
               b'value': {b'algorithm': 1, 
                          b'fingerprint_type': 42, 
                          b'fingerprint': b'bf6b6825d2977c511a475bbefb88aad54a92ac73'}})
        self.assertEquals([b'unrecognized fingerprint_type "42"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'SSHFP', 
               b'ttl': 600, 
               b'value': {b'algorithm': 1, 
                          b'fingerprint_type': 1}})
        self.assertEquals([b'missing fingerprint'], ctx.exception.reasons)

    def test_SPF(self):
        Record.new(self.zone, b'', {b'type': b'SPF', 
           b'ttl': 600, 
           b'values': [
                     b'v=spf1 ip4:192.168.0.1/16-all',
                     b'v=spf1 ip4:10.1.2.1/24-all',
                     b'this has some\\; semi-colons\\; in it']})
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'SPF', 
               b'ttl': 600})
        self.assertEquals([b'missing value(s)'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'SPF', 
               b'ttl': 600, 
               b'value': b'this has some; semi-colons\\; in it'})
        self.assertEquals([b'unescaped ; in "this has some; semi-colons\\; in it"'], ctx.exception.reasons)

    def test_SRV(self):
        Record.new(self.zone, b'_srv._tcp', {b'type': b'SRV', 
           b'ttl': 600, 
           b'value': {b'priority': 1, 
                      b'weight': 2, 
                      b'port': 3, 
                      b'target': b'foo.bar.baz.'}})
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'neup', {b'type': b'SRV', 
               b'ttl': 600, 
               b'value': {b'priority': 1, 
                          b'weight': 2, 
                          b'port': 3, 
                          b'target': b'foo.bar.baz.'}})
        self.assertEquals([b'invalid name'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'_srv._tcp', {b'type': b'SRV', 
               b'ttl': 600, 
               b'value': {b'weight': 2, 
                          b'port': 3, 
                          b'target': b'foo.bar.baz.'}})
        self.assertEquals([b'missing priority'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'_srv._tcp', {b'type': b'SRV', 
               b'ttl': 600, 
               b'value': {b'priority': b'foo', 
                          b'weight': 2, 
                          b'port': 3, 
                          b'target': b'foo.bar.baz.'}})
        self.assertEquals([b'invalid priority "foo"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'_srv._tcp', {b'type': b'SRV', 
               b'ttl': 600, 
               b'value': {b'priority': 1, 
                          b'port': 3, 
                          b'target': b'foo.bar.baz.'}})
        self.assertEquals([b'missing weight'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'_srv._tcp', {b'type': b'SRV', 
               b'ttl': 600, 
               b'value': {b'priority': 1, 
                          b'weight': b'foo', 
                          b'port': 3, 
                          b'target': b'foo.bar.baz.'}})
        self.assertEquals([b'invalid weight "foo"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'_srv._tcp', {b'type': b'SRV', 
               b'ttl': 600, 
               b'value': {b'priority': 1, 
                          b'weight': 2, 
                          b'target': b'foo.bar.baz.'}})
        self.assertEquals([b'missing port'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'_srv._tcp', {b'type': b'SRV', 
               b'ttl': 600, 
               b'value': {b'priority': 1, 
                          b'weight': 2, 
                          b'port': b'foo', 
                          b'target': b'foo.bar.baz.'}})
        self.assertEquals([b'invalid port "foo"'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'_srv._tcp', {b'type': b'SRV', 
               b'ttl': 600, 
               b'value': {b'priority': 1, 
                          b'weight': 2, 
                          b'port': 3}})
        self.assertEquals([b'missing target'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'_srv._tcp', {b'type': b'SRV', 
               b'ttl': 600, 
               b'value': {b'priority': 1, 
                          b'weight': 2, 
                          b'port': 3, 
                          b'target': b'foo.bar.baz'}})
        self.assertEquals([b'SRV value "foo.bar.baz" missing trailing .'], ctx.exception.reasons)

    def test_TXT(self):
        Record.new(self.zone, b'', {b'type': b'TXT', 
           b'ttl': 600, 
           b'values': [
                     b'hello world',
                     b'this has some\\; semi-colons\\; in it']})
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'TXT', 
               b'ttl': 600})
        self.assertEquals([b'missing value(s)'], ctx.exception.reasons)
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'', {b'type': b'TXT', 
               b'ttl': 600, 
               b'value': b'this has some; semi-colons\\; in it'})
        self.assertEquals([b'unescaped ; in "this has some; semi-colons\\; in it"'], ctx.exception.reasons)

    def test_TXT_long_value_chunking(self):
        expected = b'"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor i" "n reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."'
        long_value = b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
        single = Record.new(self.zone, b'', {b'type': b'TXT', 
           b'ttl': 600, 
           b'values': [
                     b'hello world',
                     long_value,
                     b'this has some\\; semi-colons\\; in it']})
        self.assertEquals(3, len(single.values))
        self.assertEquals(3, len(single.chunked_values))
        self.assertEquals(expected, single.chunked_values[0])
        long_split_value = b'"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex" " ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."'
        chunked = Record.new(self.zone, b'', {b'type': b'TXT', 
           b'ttl': 600, 
           b'values': [
                     b'"hello world"',
                     long_split_value,
                     b'"this has some\\; semi-colons\\; in it"']})
        self.assertEquals(expected, chunked.chunked_values[0])
        self.assertEquals(single.values, chunked.values)
        self.assertEquals(single.chunked_values, chunked.chunked_values)


class TestDynamicRecords(TestCase):
    zone = Zone(b'unit.tests.', [])

    def test_simple_a_weighted(self):
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'5.5.5.5'},
                                                      {b'value': b'4.4.4.4'}]}, 
                                   b'three': {b'values': [
                                                        {b'weight': 10, 
                                                           b'value': b'4.4.4.4'},
                                                        {b'weight': 12, 
                                                           b'value': b'5.5.5.5'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'AF', b'EU'], 
                                    b'pool': b'three'},
                                 {b'geos': [
                                            b'NA-US-CA'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        a = ARecord(self.zone, b'weighted', a_data)
        self.assertEquals(b'A', a._type)
        self.assertEquals(a_data[b'ttl'], a.ttl)
        self.assertEquals(a_data[b'values'], a.values)
        dynamic = a.dynamic
        self.assertTrue(dynamic)
        pools = dynamic.pools
        self.assertTrue(pools)
        self.assertEquals({b'value': b'3.3.3.3', 
           b'weight': 1}, pools[b'one'].data[b'values'][0])
        self.assertEquals([
         {b'value': b'4.4.4.4', 
            b'weight': 1},
         {b'value': b'5.5.5.5', 
            b'weight': 1}], pools[b'two'].data[b'values'])
        self.assertEquals([
         {b'weight': 10, 
            b'value': b'4.4.4.4'},
         {b'weight': 12, 
            b'value': b'5.5.5.5'}], pools[b'three'].data[b'values'])
        rules = dynamic.rules
        self.assertTrue(rules)
        self.assertEquals(a_data[b'dynamic'][b'rules'][0], rules[0].data)

    def test_simple_aaaa_weighted(self):
        aaaa_data = {b'dynamic': {b'pools': {b'one': b'2601:642:500:e210:62f8:1dff:feb8:9473', 
                                   b'two': [
                                          b'2601:642:500:e210:62f8:1dff:feb8:9474',
                                          b'2601:642:500:e210:62f8:1dff:feb8:9475'], 
                                   b'three': {1: b'2601:642:500:e210:62f8:1dff:feb8:9476', 
                                              2: b'2601:642:500:e210:62f8:1dff:feb8:9477'}}, 
                        b'rules': [
                                 {b'pools': [
                                             b'three',
                                             b'two',
                                             b'one']}]}, 
           b'ttl': 60, 
           b'values': [
                     b'2601:642:500:e210:62f8:1dff:feb8:9471',
                     b'2601:642:500:e210:62f8:1dff:feb8:9472']}
        aaaa_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'2601:642:500:e210:62f8:1dff:feb8:9473'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'2601:642:500:e210:62f8:1dff:feb8:9475'},
                                                      {b'value': b'2601:642:500:e210:62f8:1dff:feb8:9474'}]}, 
                                   b'three': {b'values': [
                                                        {b'weight': 10, 
                                                           b'value': b'2601:642:500:e210:62f8:1dff:feb8:9476'},
                                                        {b'weight': 12, 
                                                           b'value': b'2601:642:500:e210:62f8:1dff:feb8:9477'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'AF', b'EU'], 
                                    b'pool': b'three'},
                                 {b'geos': [
                                            b'NA-US-CA'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'values': [
                     b'2601:642:500:e210:62f8:1dff:feb8:9471',
                     b'2601:642:500:e210:62f8:1dff:feb8:9472']}
        aaaa = AaaaRecord(self.zone, b'weighted', aaaa_data)
        self.assertEquals(b'AAAA', aaaa._type)
        self.assertEquals(aaaa_data[b'ttl'], aaaa.ttl)
        self.assertEquals(aaaa_data[b'values'], aaaa.values)
        dynamic = aaaa.dynamic
        self.assertTrue(dynamic)
        pools = dynamic.pools
        self.assertTrue(pools)
        self.assertEquals({b'value': b'2601:642:500:e210:62f8:1dff:feb8:9473', 
           b'weight': 1}, pools[b'one'].data[b'values'][0])
        self.assertEquals([
         {b'value': b'2601:642:500:e210:62f8:1dff:feb8:9474', 
            b'weight': 1},
         {b'value': b'2601:642:500:e210:62f8:1dff:feb8:9475', 
            b'weight': 1}], pools[b'two'].data[b'values'])
        self.assertEquals([
         {b'weight': 10, 
            b'value': b'2601:642:500:e210:62f8:1dff:feb8:9476'},
         {b'weight': 12, 
            b'value': b'2601:642:500:e210:62f8:1dff:feb8:9477'}], pools[b'three'].data[b'values'])
        rules = dynamic.rules
        self.assertTrue(rules)
        self.assertEquals(aaaa_data[b'dynamic'][b'rules'][0], rules[0].data)

    def test_simple_cname_weighted(self):
        cname_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'one.cname.target.'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'two.cname.target.'}]}, 
                                   b'three': {b'values': [
                                                        {b'weight': 12, 
                                                           b'value': b'three-1.cname.target.'},
                                                        {b'weight': 32, 
                                                           b'value': b'three-2.cname.target.'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'AF', b'EU'], 
                                    b'pool': b'three'},
                                 {b'geos': [
                                            b'NA-US-CA'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'value': b'cname.target.'}
        cname = CnameRecord(self.zone, b'weighted', cname_data)
        self.assertEquals(b'CNAME', cname._type)
        self.assertEquals(cname_data[b'ttl'], cname.ttl)
        self.assertEquals(cname_data[b'value'], cname.value)
        dynamic = cname.dynamic
        self.assertTrue(dynamic)
        pools = dynamic.pools
        self.assertTrue(pools)
        self.assertEquals({b'value': b'one.cname.target.', 
           b'weight': 1}, pools[b'one'].data[b'values'][0])
        self.assertEquals({b'value': b'two.cname.target.', 
           b'weight': 1}, pools[b'two'].data[b'values'][0])
        self.assertEquals([
         {b'value': b'three-1.cname.target.', 
            b'weight': 12},
         {b'value': b'three-2.cname.target.', 
            b'weight': 32}], pools[b'three'].data[b'values'])
        rules = dynamic.rules
        self.assertTrue(rules)
        self.assertEquals(cname_data[b'dynamic'][b'rules'][0], rules[0].data)

    def test_dynamic_validation(self):
        a_data = {b'dynamic': {b'rules': [
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([b'missing pools', b'rule 1 undefined pool "one"'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {}, b'rules': [
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([b'missing pools', b'rule 1 undefined pool "one"'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': [], b'rules': [
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([b'pools must be a dict',
         b'rule 1 undefined pool "one"'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'this-aint-right'}]}, 
                                   b'two': {b'fallback': b'one', 
                                            b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'nor-is-this'}]}, 
                                   b'three': {b'fallback': b'two', 
                                              b'values': [
                                                        {b'weight': 1, 
                                                           b'value': b'5.5.5.5'},
                                                        {b'weight': 2, 
                                                           b'value': b'yet-another-bad-one'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'AF', b'EU'], 
                                    b'pool': b'three'},
                                 {b'geos': [
                                            b'NA-US-CA'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([
         b'invalid IPv4 address "this-aint-right"',
         b'invalid IPv4 address "yet-another-bad-one"',
         b'invalid IPv4 address "nor-is-this"'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {}, b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}, 
                                   b'three': {b'values': [
                                                        {b'weight': 1, 
                                                           b'value': b'6.6.6.6'},
                                                        {b'weight': 2, 
                                                           b'value': b'7.7.7.7'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'AF', b'EU'], 
                                    b'pool': b'three'},
                                 {b'geos': [
                                            b'NA-US-CA'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([b'pool "one" is missing values'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': b'', 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}, 
                                   b'three': {b'values': [
                                                        {b'weight': 1, 
                                                           b'value': b'6.6.6.6'},
                                                        {b'weight': 2, 
                                                           b'value': b'7.7.7.7'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'AF', b'EU'], 
                                    b'pool': b'three'},
                                 {b'geos': [
                                            b'NA-US-CA'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([b'pool "one" must be a dict'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {}, b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}, 
                                   b'three': {b'values': [
                                                        {b'weight': 1, 
                                                           b'value': b'6.6.6.6'},
                                                        {b'weight': 2, 
                                                           b'value': b'7.7.7.7'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'AF', b'EU'], 
                                    b'pool': b'three'},
                                 {b'geos': [
                                            b'NA-US-CA'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([b'pool "one" is missing values'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}, 
                                   b'three': {b'values': [
                                                        {b'weight': 1, 
                                                           b'value': b'6.6.6.6'},
                                                        {b'weight': 16, 
                                                           b'value': b'7.7.7.7'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'AF', b'EU'], 
                                    b'pool': b'three'},
                                 {b'geos': [
                                            b'NA-US-CA'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([b'invalid weight "16" in pool "three" value 2'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}, 
                                   b'three': {b'values': [
                                                        {b'weight': 1, 
                                                           b'value': b'6.6.6.6'},
                                                        {b'weight': b'foo', 
                                                           b'value': b'7.7.7.7'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'AF', b'EU'], 
                                    b'pool': b'three'},
                                 {b'geos': [
                                            b'NA-US-CA'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([b'invalid weight "foo" in pool "three" value 2'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'fallback': b'invalid', 
                                            b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}, 
                                   b'three': {b'fallback': b'two', 
                                              b'values': [
                                                        {b'weight': 1, 
                                                           b'value': b'6.6.6.6'},
                                                        {b'weight': 5, 
                                                           b'value': b'7.7.7.7'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'AF', b'EU'], 
                                    b'pool': b'three'},
                                 {b'geos': [
                                            b'NA-US-CA'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([b'undefined fallback "invalid" for pool "two"'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {b'fallback': b'three', 
                                            b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'fallback': b'one', 
                                            b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}, 
                                   b'three': {b'fallback': b'two', 
                                              b'values': [
                                                        {b'weight': 1, 
                                                           b'value': b'6.6.6.6'},
                                                        {b'weight': 5, 
                                                           b'value': b'7.7.7.7'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'AF', b'EU'], 
                                    b'pool': b'three'},
                                 {b'geos': [
                                            b'NA-US-CA'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([
         b'loop in pool fallbacks: one -> three -> two',
         b'loop in pool fallbacks: three -> two -> one',
         b'loop in pool fallbacks: two -> one -> three'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': b'', 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'blip'}]}, 
                                   b'three': {b'values': [
                                                        {b'weight': 1},
                                                        {b'weight': 5000, 
                                                           b'value': b'7.7.7.7'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'AF', b'EU'], 
                                    b'pool': b'three'},
                                 {b'geos': [
                                            b'NA-US-CA'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([
         b'pool "one" must be a dict',
         b'missing value in pool "three" value 1',
         b'invalid weight "5000" in pool "three" value 2',
         b'invalid IPv4 address "blip"'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}}}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([
         b'missing rules',
         b'unused pools: "one", "two"'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}}, 
                        b'rules': []}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([
         b'missing rules',
         b'unused pools: "one", "two"'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}}, 
                        b'rules': {}}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([
         b'rules must be a list',
         b'unused pools: "one", "two"'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'NA-US-CA']},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([
         b'rule 1 missing pool',
         b'unused pools: "two"'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'NA-US-CA'], 
                                    b'pool': []},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([
         b'rule 1 invalid pool "[]"',
         b'unused pools: "two"'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'NA-US-CA'], 
                                    b'pool': b'non-existent'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([
         b'rule 1 undefined pool "non-existent"',
         b'unused pools: "two"'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}}, 
                        b'rules': [
                                 {b'geos': b'NA-US-CA', 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([b'rule 1 geos must be a list'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'invalid'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([b'rule 1 unknown continent code "invalid"'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}}, 
                        b'rules': [
                                 {b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([b'rule 2 duplicate default'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'EU'], 
                                    b'pool': b'two'},
                                 {b'geos': [
                                            b'AF'], 
                                    b'pool': b'one'},
                                 {b'geos': [
                                            b'OC'], 
                                    b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([b'rule 3 invalid, target pool "one" reused'], ctx.exception.reasons)
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'EU-GB'], 
                                    b'pool': b'one'},
                                 {b'geos': [
                                            b'EU'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        Record.new(self.zone, b'bad', a_data)

    def test_dynamic_lenient(self):
        a_data = {b'dynamic': {b'rules': [
                                 {b'geos': [
                                            b'EU'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        a = Record.new(self.zone, b'bad', a_data, lenient=True)
        self.assertEquals({b'pools': {}, b'rules': a_data[b'dynamic'][b'rules']}, a._data()[b'dynamic'])
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5', 
                                                         b'weight': 2}]}}}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        a = Record.new(self.zone, b'bad', a_data, lenient=True)
        self.assertEquals({b'pools': {b'one': {b'fallback': None, 
                               b'values': [
                                         {b'value': b'3.3.3.3', 
                                            b'weight': 1}]}, 
                      b'two': {b'fallback': None, 
                               b'values': [
                                         {b'value': b'4.4.4.4', 
                                            b'weight': 1},
                                         {b'value': b'5.5.5.5', 
                                            b'weight': 2}]}}, 
           b'rules': []}, a._data()[b'dynamic'])
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5', 
                                                         b'weight': 2}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'EU'], 
                                    b'pool': b'two'}, {}]}, 
           b'ttl': 60, 
           b'type': b'A', 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        a = Record.new(self.zone, b'bad', a_data, lenient=True)
        self.assertEquals({b'pools': {b'one': {b'fallback': None, 
                               b'values': [
                                         {b'value': b'3.3.3.3', 
                                            b'weight': 1}]}, 
                      b'two': {b'fallback': None, 
                               b'values': [
                                         {b'value': b'4.4.4.4', 
                                            b'weight': 1},
                                         {b'value': b'5.5.5.5', 
                                            b'weight': 2}]}}, 
           b'rules': a_data[b'dynamic'][b'rules']}, a._data()[b'dynamic'])
        return

    def test_dynamic_changes(self):
        simple = SimpleProvider()
        dynamic = DynamicProvider()
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'EU'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        a = ARecord(self.zone, b'weighted', a_data)
        dup = ARecord(self.zone, b'weighted', a_data)
        b_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4', 
                                                         b'weight': 2},
                                                      {b'value': b'5.5.5.5'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'EU'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        b = ARecord(self.zone, b'weighted', b_data)
        c_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'4.4.4.4'},
                                                      {b'value': b'5.5.5.5'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'NA'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'ttl': 60, 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        c = ARecord(self.zone, b'weighted', c_data)
        self.assertFalse(a.changes(dup, simple))
        self.assertFalse(a.changes(dup, dynamic))
        self.assertFalse(a.changes(b, simple))
        update = a.changes(b, dynamic)
        self.assertEquals(a, update.existing)
        self.assertEquals(b, update.new)
        self.assertFalse(b.changes(a, simple))
        update = b.changes(a, dynamic)
        self.assertEquals(a, update.existing)
        self.assertEquals(b, update.new)
        self.assertFalse(a.changes(c, simple))
        self.assertTrue(a.changes(c, dynamic))
        self.assertFalse(c.changes(a, simple))
        self.assertTrue(c.changes(a, dynamic))
        self.assertEquals(a.dynamic.pools, a.dynamic.pools)
        self.assertEquals(a.dynamic.pools[b'one'], a.dynamic.pools[b'one'])
        self.assertNotEquals(a.dynamic.pools[b'one'], a.dynamic.pools[b'two'])
        self.assertEquals(a.dynamic.rules, a.dynamic.rules)
        self.assertEquals(a.dynamic.rules[0], a.dynamic.rules[0])
        self.assertNotEquals(a.dynamic.rules[0], c.dynamic.rules[0])

    def test_dynamic_and_geo_validation(self):
        a_data = {b'dynamic': {b'pools': {b'one': {b'values': [
                                                      {b'value': b'3.3.3.3'}]}, 
                                   b'two': {b'values': [
                                                      {b'value': b'5.5.5.5'},
                                                      {b'value': b'4.4.4.4'}]}, 
                                   b'three': {b'values': [
                                                        {b'weight': 10, 
                                                           b'value': b'4.4.4.4'},
                                                        {b'weight': 12, 
                                                           b'value': b'5.5.5.5'}]}}, 
                        b'rules': [
                                 {b'geos': [
                                            b'AF', b'EU'], 
                                    b'pool': b'three'},
                                 {b'geos': [
                                            b'NA-US-CA'], 
                                    b'pool': b'two'},
                                 {b'pool': b'one'}]}, 
           b'geo': {b'NA': [
                          b'1.2.3.5'], 
                    b'NA-US': [
                             b'1.2.3.5', b'1.2.3.6']}, 
           b'type': b'A', 
           b'ttl': 60, 
           b'values': [
                     b'1.1.1.1',
                     b'2.2.2.2']}
        with self.assertRaises(ValidationError) as (ctx):
            Record.new(self.zone, b'bad', a_data)
        self.assertEquals([b'"dynamic" record with "geo" content'], ctx.exception.reasons)

    def test_dynamic_eqs(self):
        pool_one = _DynamicPool(b'one', {b'values': [
                     {b'value': b'1.2.3.4'}]})
        pool_two = _DynamicPool(b'two', {b'values': [
                     {b'value': b'1.2.3.5'}]})
        self.assertEquals(pool_one, pool_one)
        self.assertNotEquals(pool_one, pool_two)
        self.assertNotEquals(pool_one, 42)
        pools = {b'one': pool_one, 
           b'two': pool_two}
        rule_one = _DynamicRule(0, {b'pool': b'one'})
        rule_two = _DynamicRule(1, {b'pool': b'two'})
        self.assertEquals(rule_one, rule_one)
        self.assertNotEquals(rule_one, rule_two)
        self.assertNotEquals(rule_one, 42)
        rules = [
         rule_one,
         rule_two]
        dynamic = _Dynamic(pools, rules)
        other = _Dynamic({}, [])
        self.assertEquals(dynamic, dynamic)
        self.assertNotEquals(dynamic, other)
        self.assertNotEquals(dynamic, 42)