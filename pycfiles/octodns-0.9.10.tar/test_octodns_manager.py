# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_manager.py
# Compiled at: 2020-01-15 20:00:35
from __future__ import absolute_import, division, print_function, unicode_literals
from os import environ
from os.path import dirname, join
from six import text_type
from unittest import TestCase
from octodns.record import Record
from octodns.manager import _AggregateTarget, MainThreadExecutor, Manager, ManagerException
from octodns.yaml import safe_load
from octodns.zone import Zone
from helpers import DynamicProvider, GeoProvider, NoSshFpProvider, SimpleProvider, TemporaryDirectory
config_dir = join(dirname(__file__), b'config')

def get_config_filename(which):
    return join(config_dir, which)


class TestManager(TestCase):

    def test_missing_provider_class(self):
        with self.assertRaises(ManagerException) as (ctx):
            Manager(get_config_filename(b'missing-provider-class.yaml')).sync()
        self.assertTrue(b'missing class' in text_type(ctx.exception))

    def test_bad_provider_class(self):
        with self.assertRaises(ManagerException) as (ctx):
            Manager(get_config_filename(b'bad-provider-class.yaml')).sync()
        self.assertTrue(b'Unknown provider class' in text_type(ctx.exception))

    def test_bad_provider_class_module(self):
        with self.assertRaises(ManagerException) as (ctx):
            Manager(get_config_filename(b'bad-provider-class-module.yaml')).sync()
        self.assertTrue(b'Unknown provider class' in text_type(ctx.exception))

    def test_bad_provider_class_no_module(self):
        with self.assertRaises(ManagerException) as (ctx):
            Manager(get_config_filename(b'bad-provider-class-no-module.yaml')).sync()
        self.assertTrue(b'Unknown provider class' in text_type(ctx.exception))

    def test_missing_provider_config(self):
        with self.assertRaises(ManagerException) as (ctx):
            Manager(get_config_filename(b'missing-provider-config.yaml')).sync()
        self.assertTrue(b'provider config' in text_type(ctx.exception))

    def test_missing_env_config(self):
        with self.assertRaises(ManagerException) as (ctx):
            Manager(get_config_filename(b'missing-provider-env.yaml')).sync()
        self.assertTrue(b'missing env var' in text_type(ctx.exception))

    def test_missing_source(self):
        with self.assertRaises(ManagerException) as (ctx):
            Manager(get_config_filename(b'provider-problems.yaml')).sync([
             b'missing.sources.'])
        self.assertTrue(b'missing sources' in text_type(ctx.exception))

    def test_missing_targets(self):
        with self.assertRaises(ManagerException) as (ctx):
            Manager(get_config_filename(b'provider-problems.yaml')).sync([
             b'missing.targets.'])
        self.assertTrue(b'missing targets' in text_type(ctx.exception))

    def test_unknown_source(self):
        with self.assertRaises(ManagerException) as (ctx):
            Manager(get_config_filename(b'provider-problems.yaml')).sync([
             b'unknown.source.'])
        self.assertTrue(b'unknown source' in text_type(ctx.exception))

    def test_unknown_target(self):
        with self.assertRaises(ManagerException) as (ctx):
            Manager(get_config_filename(b'provider-problems.yaml')).sync([
             b'unknown.target.'])
        self.assertTrue(b'unknown target' in text_type(ctx.exception))

    def test_bad_plan_output_class(self):
        with self.assertRaises(ManagerException) as (ctx):
            name = b'bad-plan-output-missing-class.yaml'
            Manager(get_config_filename(name)).sync()
        self.assertEquals(b'plan_output bad is missing class', text_type(ctx.exception))

    def test_bad_plan_output_config(self):
        with self.assertRaises(ManagerException) as (ctx):
            Manager(get_config_filename(b'bad-plan-output-config.yaml')).sync()
        self.assertEqual(b'Incorrect plan_output config for bad', text_type(ctx.exception))

    def test_source_only_as_a_target(self):
        with self.assertRaises(ManagerException) as (ctx):
            Manager(get_config_filename(b'provider-problems.yaml')).sync([
             b'not.targetable.'])
        self.assertTrue(b'does not support targeting' in text_type(ctx.exception))

    def test_always_dry_run(self):
        with TemporaryDirectory() as (tmpdir):
            environ[b'YAML_TMP_DIR'] = tmpdir.dirname
            tc = Manager(get_config_filename(b'always-dry-run.yaml')).sync(dry_run=False)
            self.assertEquals(3, tc)

    def test_simple(self):
        with TemporaryDirectory() as (tmpdir):
            environ[b'YAML_TMP_DIR'] = tmpdir.dirname
            tc = Manager(get_config_filename(b'simple.yaml')).sync(dry_run=False)
            self.assertEquals(21, tc)
            tc = Manager(get_config_filename(b'simple.yaml')).sync(dry_run=False, eligible_zones=[b'unit.tests.'])
            self.assertEquals(15, tc)
            tc = Manager(get_config_filename(b'simple.yaml')).sync(dry_run=False, eligible_zones=[b'subzone.unit.tests.'])
            self.assertEquals(6, tc)
            tc = Manager(get_config_filename(b'simple.yaml')).sync(dry_run=False, eligible_zones=[b'empty.'])
            self.assertEquals(0, tc)
            tc = Manager(get_config_filename(b'simple.yaml')).sync(dry_run=False, force=True)
            self.assertEquals(21, tc)
            tc = Manager(get_config_filename(b'simple.yaml'), max_workers=1).sync(dry_run=False, force=True)
            self.assertEquals(21, tc)
            tc = Manager(get_config_filename(b'simple.yaml'), max_workers=1, include_meta=True).sync(dry_run=False, force=True)
            self.assertEquals(25, tc)

    def test_eligible_targets(self):
        with TemporaryDirectory() as (tmpdir):
            environ[b'YAML_TMP_DIR'] = tmpdir.dirname
            tc = Manager(get_config_filename(b'simple.yaml')).sync(eligible_targets=[
             b'foo'])
            self.assertEquals(0, tc)

    def test_compare(self):
        with TemporaryDirectory() as (tmpdir):
            environ[b'YAML_TMP_DIR'] = tmpdir.dirname
            manager = Manager(get_config_filename(b'simple.yaml'))
            self.assertEquals(2, manager._executor._max_workers)
            changes = manager.compare([b'in'], [b'in'], b'unit.tests.')
            self.assertEquals([], changes)
            with open(join(tmpdir.dirname, b'unit.tests.yaml'), b'w') as (fh):
                fh.write(b'---\n{}')
            changes = manager.compare([b'in'], [b'dump'], b'unit.tests.')
            self.assertEquals(15, len(changes))
            changes = manager.compare([b'in', b'nosshfp'], [
             b'dump'], b'unit.tests.')
            self.assertEquals(14, len(changes))
            with self.assertRaises(ManagerException) as (ctx):
                manager.compare([b'nope'], [b'dump'], b'unit.tests.')
            self.assertEquals(b'Unknown source: nope', text_type(ctx.exception))

    def test_aggregate_target(self):
        simple = SimpleProvider()
        geo = GeoProvider()
        dynamic = DynamicProvider()
        nosshfp = NoSshFpProvider()
        self.assertFalse(_AggregateTarget([simple, simple]).SUPPORTS_GEO)
        self.assertFalse(_AggregateTarget([simple, geo]).SUPPORTS_GEO)
        self.assertFalse(_AggregateTarget([geo, simple]).SUPPORTS_GEO)
        self.assertTrue(_AggregateTarget([geo, geo]).SUPPORTS_GEO)
        self.assertFalse(_AggregateTarget([simple, simple]).SUPPORTS_DYNAMIC)
        self.assertFalse(_AggregateTarget([simple, dynamic]).SUPPORTS_DYNAMIC)
        self.assertFalse(_AggregateTarget([dynamic, simple]).SUPPORTS_DYNAMIC)
        self.assertTrue(_AggregateTarget([dynamic, dynamic]).SUPPORTS_DYNAMIC)
        zone = Zone(b'unit.tests.', [])
        record = Record.new(zone, b'sshfp', {b'ttl': 60, 
           b'type': b'SSHFP', 
           b'value': {b'algorithm': 1, 
                      b'fingerprint_type': 1, 
                      b'fingerprint': b'abcdefg'}})
        self.assertTrue(simple.supports(record))
        self.assertFalse(nosshfp.supports(record))
        self.assertTrue(_AggregateTarget([simple, simple]).supports(record))
        self.assertFalse(_AggregateTarget([simple, nosshfp]).supports(record))

    def test_dump(self):
        with TemporaryDirectory() as (tmpdir):
            environ[b'YAML_TMP_DIR'] = tmpdir.dirname
            manager = Manager(get_config_filename(b'simple.yaml'))
            with self.assertRaises(ManagerException) as (ctx):
                manager.dump(b'unit.tests.', tmpdir.dirname, False, False, b'nope')
            self.assertEquals(b'Unknown source: nope', text_type(ctx.exception))
            manager.dump(b'unit.tests.', tmpdir.dirname, False, False, b'in')
            with self.assertRaises(IOError):
                manager.dump(b'unknown.zone.', tmpdir.dirname, False, False, b'in')

    def test_dump_empty(self):
        with TemporaryDirectory() as (tmpdir):
            environ[b'YAML_TMP_DIR'] = tmpdir.dirname
            manager = Manager(get_config_filename(b'simple.yaml'))
            manager.dump(b'empty.', tmpdir.dirname, False, False, b'in')
            with open(join(tmpdir.dirname, b'empty.yaml')) as (fh):
                data = safe_load(fh, False)
                self.assertFalse(data)

    def test_dump_split(self):
        with TemporaryDirectory() as (tmpdir):
            environ[b'YAML_TMP_DIR'] = tmpdir.dirname
            manager = Manager(get_config_filename(b'simple-split.yaml'))
            with self.assertRaises(ManagerException) as (ctx):
                manager.dump(b'unit.tests.', tmpdir.dirname, False, True, b'nope')
            self.assertEquals(b'Unknown source: nope', text_type(ctx.exception))
            manager.dump(b'unit.tests.', tmpdir.dirname, False, True, b'in')
            with self.assertRaises(OSError):
                manager.dump(b'unknown.zone.', tmpdir.dirname, False, True, b'in')

    def test_validate_configs(self):
        Manager(get_config_filename(b'simple-validate.yaml')).validate_configs()
        with self.assertRaises(ManagerException) as (ctx):
            Manager(get_config_filename(b'missing-sources.yaml')).validate_configs()
        self.assertTrue(b'missing sources' in text_type(ctx.exception))
        with self.assertRaises(ManagerException) as (ctx):
            Manager(get_config_filename(b'unknown-provider.yaml')).validate_configs()
        self.assertTrue(b'unknown source' in text_type(ctx.exception))


class TestMainThreadExecutor(TestCase):

    def test_success(self):
        mte = MainThreadExecutor()
        future = mte.submit(self.success, 42)
        self.assertEquals(42, future.result())
        future = mte.submit(self.success, ret=43)
        self.assertEquals(43, future.result())

    def test_exception(self):
        mte = MainThreadExecutor()
        e = Exception(b'boom')
        future = mte.submit(self.exception, e)
        with self.assertRaises(Exception) as (ctx):
            future.result()
        self.assertEquals(e, ctx.exception)
        future = mte.submit(self.exception, e=e)
        with self.assertRaises(Exception) as (ctx):
            future.result()
        self.assertEquals(e, ctx.exception)

    def success(self, ret):
        return ret

    def exception(self, e):
        raise e