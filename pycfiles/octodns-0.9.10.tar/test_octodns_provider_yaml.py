# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_provider_yaml.py
# Compiled at: 2020-01-27 16:06:47
from __future__ import absolute_import, division, print_function, unicode_literals
from os import makedirs
from os.path import basename, dirname, isdir, isfile, join
from unittest import TestCase
from six import text_type
from yaml import safe_load
from yaml.constructor import ConstructorError
from octodns.record import Create
from octodns.provider.base import Plan
from octodns.provider.yaml import _list_all_yaml_files, SplitYamlProvider, YamlProvider
from octodns.zone import SubzoneRecordException, Zone
from helpers import TemporaryDirectory

class TestYamlProvider(TestCase):

    def test_provider(self):
        source = YamlProvider(b'test', join(dirname(__file__), b'config'))
        zone = Zone(b'unit.tests.', [])
        dynamic_zone = Zone(b'dynamic.tests.', [])
        source.populate(zone, target=source)
        self.assertEquals(0, len(zone.records))
        source.populate(zone)
        self.assertEquals(18, len(zone.records))
        source.populate(dynamic_zone)
        self.assertEquals(5, len(dynamic_zone.records))
        with TemporaryDirectory() as (td):
            directory = join(td.dirname, b'sub', b'dir')
            yaml_file = join(directory, b'unit.tests.yaml')
            dynamic_yaml_file = join(directory, b'dynamic.tests.yaml')
            target = YamlProvider(b'test', directory)
            plan = target.plan(zone)
            self.assertEquals(15, len([ c for c in plan.changes if isinstance(c, Create)
                                      ]))
            self.assertFalse(isfile(yaml_file))
            self.assertEquals(15, target.apply(plan))
            self.assertTrue(isfile(yaml_file))
            plan = target.plan(dynamic_zone)
            self.assertEquals(5, len([ c for c in plan.changes if isinstance(c, Create)
                                     ]))
            self.assertFalse(isfile(dynamic_yaml_file))
            self.assertEquals(5, target.apply(plan))
            self.assertTrue(isfile(dynamic_yaml_file))
            reloaded = Zone(b'unit.tests.', [])
            target.populate(reloaded)
            self.assertDictEqual({b'included': [b'test']}, [ x for x in reloaded.records if x.name == b'included'
                                                           ][0]._octodns)
            self.assertFalse(zone.changes(reloaded, target=source))
            plan = target.plan(zone)
            self.assertEquals(15, len([ c for c in plan.changes if isinstance(c, Create)
                                      ]))
            with open(yaml_file) as (fh):
                data = safe_load(fh.read())
                roots = sorted(data.pop(b''), key=lambda r: r[b'type'])
                self.assertTrue(b'values' in roots[0])
                self.assertTrue(b'geo' in roots[0])
                self.assertTrue(b'value' in roots[1])
                self.assertTrue(b'values' in roots[2])
                self.assertTrue(b'values' in data.pop(b'_srv._tcp'))
                self.assertTrue(b'values' in data.pop(b'mx'))
                self.assertTrue(b'values' in data.pop(b'naptr'))
                self.assertTrue(b'values' in data.pop(b'sub'))
                self.assertTrue(b'values' in data.pop(b'txt'))
                self.assertTrue(b'value' in data.pop(b'aaaa'))
                self.assertTrue(b'value' in data.pop(b'cname'))
                self.assertTrue(b'value' in data.pop(b'included'))
                self.assertTrue(b'value' in data.pop(b'ptr'))
                self.assertTrue(b'value' in data.pop(b'spf'))
                self.assertTrue(b'value' in data.pop(b'www'))
                self.assertTrue(b'value' in data.pop(b'www.sub'))
                self.assertEquals([], list(data.keys()))
            with open(dynamic_yaml_file) as (fh):
                data = safe_load(fh.read())
                dyna = data.pop(b'a')
                self.assertTrue(b'values' in dyna)
                dyna = data.pop(b'aaaa')
                self.assertTrue(b'values' in dyna)
                dyna = data.pop(b'cname')
                self.assertTrue(b'value' in dyna)
                dyna = data.pop(b'real-ish-a')
                self.assertTrue(b'values' in dyna)
                dyna = data.pop(b'simple-weighted')
                self.assertTrue(b'value' in dyna)
                self.assertEquals([], list(data.keys()))

    def test_empty(self):
        source = YamlProvider(b'test', join(dirname(__file__), b'config'))
        zone = Zone(b'empty.', [])
        source.populate(zone)
        self.assertEquals(0, len(zone.records))

    def test_unsorted(self):
        source = YamlProvider(b'test', join(dirname(__file__), b'config'))
        zone = Zone(b'unordered.', [])
        with self.assertRaises(ConstructorError):
            source.populate(zone)
        source = YamlProvider(b'test', join(dirname(__file__), b'config'), enforce_order=False)
        source.populate(zone)
        self.assertEqual(2, len(zone.records))

    def test_subzone_handling(self):
        source = YamlProvider(b'test', join(dirname(__file__), b'config'))
        zone = Zone(b'unit.tests.', [b'sub'])
        with self.assertRaises(SubzoneRecordException) as (ctx):
            source.populate(zone)
        self.assertEquals(b'Record www.sub.unit.tests. is under a managed subzone', text_type(ctx.exception))


class TestSplitYamlProvider(TestCase):

    def test_list_all_yaml_files(self):
        yaml_files = ('foo.yaml', '1.yaml', '$unit.tests.yaml')
        all_files = ('something', 'else', '1', '$$', '-f') + yaml_files
        all_dirs = ('dir1', 'dir2/sub', 'tricky.yaml')
        with TemporaryDirectory() as (td):
            directory = join(td.dirname)
            for emptyfile in all_files:
                open(join(directory, emptyfile), b'w').close()

            for emptydir in all_dirs:
                makedirs(join(directory, emptydir))

            d = list(basename(f) for f in _list_all_yaml_files(directory))
            self.assertEqual(len(yaml_files), len(d))

    def test_zone_directory(self):
        source = SplitYamlProvider(b'test', join(dirname(__file__), b'config/split'))
        zone = Zone(b'unit.tests.', [])
        self.assertEqual(join(dirname(__file__), b'config/split/unit.tests.'), source._zone_directory(zone))

    def test_apply_handles_existing_zone_directory(self):
        with TemporaryDirectory() as (td):
            provider = SplitYamlProvider(b'test', join(td.dirname, b'config'))
            makedirs(join(td.dirname, b'config', b'does.exist.'))
            zone = Zone(b'does.exist.', [])
            self.assertTrue(isdir(provider._zone_directory(zone)))
            provider.apply(Plan(None, zone, [], True))
            self.assertTrue(isdir(provider._zone_directory(zone)))
        return

    def test_provider(self):
        source = SplitYamlProvider(b'test', join(dirname(__file__), b'config/split'))
        zone = Zone(b'unit.tests.', [])
        dynamic_zone = Zone(b'dynamic.tests.', [])
        source.populate(zone, target=source)
        self.assertEquals(0, len(zone.records))
        source.populate(zone)
        self.assertEquals(18, len(zone.records))
        source.populate(dynamic_zone)
        self.assertEquals(5, len(dynamic_zone.records))
        with TemporaryDirectory() as (td):
            directory = join(td.dirname, b'sub', b'dir')
            zone_dir = join(directory, b'unit.tests.')
            dynamic_zone_dir = join(directory, b'dynamic.tests.')
            target = SplitYamlProvider(b'test', directory)
            plan = target.plan(zone)
            self.assertEquals(15, len([ c for c in plan.changes if isinstance(c, Create)
                                      ]))
            self.assertFalse(isdir(zone_dir))
            self.assertEquals(15, target.apply(plan))
            plan = target.plan(dynamic_zone)
            self.assertEquals(5, len([ c for c in plan.changes if isinstance(c, Create)
                                     ]))
            self.assertFalse(isdir(dynamic_zone_dir))
            self.assertEquals(5, target.apply(plan))
            self.assertTrue(isdir(dynamic_zone_dir))
            reloaded = Zone(b'unit.tests.', [])
            target.populate(reloaded)
            self.assertDictEqual({b'included': [b'test']}, [ x for x in reloaded.records if x.name == b'included'
                                                           ][0]._octodns)
            self.assertFalse(zone.changes(reloaded, target=source))
            plan = target.plan(zone)
            self.assertEquals(15, len([ c for c in plan.changes if isinstance(c, Create)
                                      ]))
            yaml_file = join(zone_dir, b'$unit.tests.yaml')
            self.assertTrue(isfile(yaml_file))
            with open(yaml_file) as (fh):
                data = safe_load(fh.read())
                roots = sorted(data.pop(b''), key=lambda r: r[b'type'])
                self.assertTrue(b'values' in roots[0])
                self.assertTrue(b'geo' in roots[0])
                self.assertTrue(b'value' in roots[1])
                self.assertTrue(b'values' in roots[2])
            for record_name in ('_srv._tcp', 'mx', 'naptr', 'sub', 'txt'):
                yaml_file = join(zone_dir, (b'{}.yaml').format(record_name))
                self.assertTrue(isfile(yaml_file))
                with open(yaml_file) as (fh):
                    data = safe_load(fh.read())
                    self.assertTrue(b'values' in data.pop(record_name))

            for record_name in ('aaaa', 'cname', 'included', 'ptr', 'spf', 'www.sub',
                                'www'):
                yaml_file = join(zone_dir, (b'{}.yaml').format(record_name))
                self.assertTrue(isfile(yaml_file))
                with open(yaml_file) as (fh):
                    data = safe_load(fh.read())
                    self.assertTrue(b'value' in data.pop(record_name))

            for record_name in ('a', 'aaaa', 'real-ish-a'):
                yaml_file = join(dynamic_zone_dir, (b'{}.yaml').format(record_name))
                self.assertTrue(isfile(yaml_file))
                with open(yaml_file) as (fh):
                    data = safe_load(fh.read())
                    dyna = data.pop(record_name)
                    self.assertTrue(b'values' in dyna)
                    self.assertTrue(b'dynamic' in dyna)

            for record_name in ('cname', 'simple-weighted'):
                yaml_file = join(dynamic_zone_dir, (b'{}.yaml').format(record_name))
                self.assertTrue(isfile(yaml_file))
                with open(yaml_file) as (fh):
                    data = safe_load(fh.read())
                    dyna = data.pop(record_name)
                    self.assertTrue(b'value' in dyna)
                    self.assertTrue(b'dynamic' in dyna)

    def test_empty(self):
        source = SplitYamlProvider(b'test', join(dirname(__file__), b'config/split'))
        zone = Zone(b'empty.', [])
        source.populate(zone)
        self.assertEquals(0, len(zone.records))

    def test_unsorted(self):
        source = SplitYamlProvider(b'test', join(dirname(__file__), b'config/split'))
        zone = Zone(b'unordered.', [])
        with self.assertRaises(ConstructorError):
            source.populate(zone)
        zone = Zone(b'unordered.', [])
        source = SplitYamlProvider(b'test', join(dirname(__file__), b'config/split'), enforce_order=False)
        source.populate(zone)
        self.assertEqual(2, len(zone.records))

    def test_subzone_handling(self):
        source = SplitYamlProvider(b'test', join(dirname(__file__), b'config/split'))
        zone = Zone(b'unit.tests.', [b'sub'])
        with self.assertRaises(SubzoneRecordException) as (ctx):
            source.populate(zone)
        self.assertEquals(b'Record www.sub.unit.tests. is under a managed subzone', text_type(ctx.exception))


class TestOverridingYamlProvider(TestCase):

    def test_provider(self):
        config = join(dirname(__file__), b'config')
        override_config = join(dirname(__file__), b'config', b'override')
        base = YamlProvider(b'base', config, populate_should_replace=False)
        override = YamlProvider(b'test', override_config, populate_should_replace=True)
        zone = Zone(b'dynamic.tests.', [])
        base.populate(zone)
        got = {r.name:r for r in zone.records}
        self.assertEquals(5, len(got))
        self.assertTrue(b'dynamic' in got[b'a'].data)
        self.assertFalse(b'added' in got)
        override.populate(zone)
        got = {r.name:r for r in zone.records}
        self.assertEquals(6, len(got))
        self.assertEquals({b'ttl': 3600, 
           b'values': [
                     b'4.4.4.4', b'5.5.5.5']}, got[b'a'].data)
        self.assertTrue(b'added' in got)