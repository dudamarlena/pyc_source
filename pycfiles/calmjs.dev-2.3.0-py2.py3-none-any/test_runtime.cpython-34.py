# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/tyu030/work/calmjs.bower/src/calmjs/bower/tests/test_runtime.py
# Compiled at: 2016-09-04 08:30:55
# Size of source mod 2**32: 5519 bytes
import unittest, json, os, sys
from os.path import join
import pkg_resources
from calmjs import cli
from calmjs import dist
from calmjs import runtime
from calmjs.utils import which
from calmjs.utils import finalize_env
from calmjs.testing import mocks
from calmjs.testing.utils import make_dummy_dist
from calmjs.testing.utils import mkdtemp
from calmjs.testing.utils import remember_cwd
from calmjs.testing.utils import stub_base_which
from calmjs.testing.utils import stub_item_attr_value
from calmjs.testing.utils import stub_mod_call
from calmjs.testing.utils import stub_mod_check_interactive
from calmjs.testing.utils import stub_stdouts
which_bower = which('bower')

class IntegrationTestCase(unittest.TestCase):

    def test_calmjs_main_console_entry_point(self):
        stub_stdouts(self)
        with self.assertRaises(SystemExit):
            runtime.main(['-h'])
        self.assertIn('bower', sys.stdout.getvalue())

    def setup_runtime(self):
        make_dummy_dist(self, (
         (
          'bower.json',
          json.dumps({'name': 'site', 
           'dependencies': {'jquery': '~3.1.0'}})),), 'example.package1', '1.0')
        make_dummy_dist(self, (
         (
          'bower.json',
          json.dumps({'name': 'site', 
           'dependencies': {'underscore': '~1.8.3'}})),), 'example.package2', '2.0')
        working_set = pkg_resources.WorkingSet([self._calmjs_testing_tmpdir])
        stub_item_attr_value(self, dist, 'default_working_set', working_set)
        stub_mod_check_interactive(self, [cli], True)
        working_set = mocks.WorkingSet({'calmjs.runtime': [
                            'bower = calmjs.bower:bower.runtime']})
        return runtime.Runtime(working_set=working_set)

    def test_calmjs_main_runtime_bower_version(self):
        stub_stdouts(self)
        with self.assertRaises(SystemExit):
            runtime.main(['bower', '-V'])
        self.assertIn('calmjs.bower', sys.stdout.getvalue())

    def test_bower_init_integration(self):
        remember_cwd(self)
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        rt = self.setup_runtime()
        rt(['bower', '--init', 'example.package1'])
        with open(join(tmpdir, 'bower.json')) as (fd):
            result = json.load(fd)
        self.assertEqual(result['dependencies']['jquery'], '~3.1.0')

    def test_bower_install_integration(self):
        remember_cwd(self)
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        stub_mod_call(self, cli)
        stub_base_which(self, which_bower)
        rt = self.setup_runtime()
        rt(['bower', '--install', 'example.package1', 'example.package2'])
        with open(join(tmpdir, 'bower.json')) as (fd):
            result = json.load(fd)
        self.assertEqual(result['dependencies']['jquery'], '~3.1.0')
        self.assertEqual(result['dependencies']['underscore'], '~1.8.3')
        args, kwargs = self.call_args
        self.assertEqual(args, (['bower', 'install'],))
        env = kwargs.pop('env', {})
        self.assertEqual(kwargs, {})
        self.assertEqual(env, finalize_env(env))

    def test_bower_view(self):
        remember_cwd(self)
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        stub_stdouts(self)
        rt = self.setup_runtime()
        rt(['bower', '--view', 'example.package1', 'example.package2'])
        result = json.loads(sys.stdout.getvalue())
        self.assertEqual(result['dependencies']['jquery'], '~3.1.0')
        self.assertEqual(result['dependencies']['underscore'], '~1.8.3')
        stub_stdouts(self)
        rt(['bower', 'example.package1', 'example.package2'])
        result = json.loads(sys.stdout.getvalue())
        self.assertEqual(result['dependencies']['jquery'], '~3.1.0')
        self.assertEqual(result['dependencies']['underscore'], '~1.8.3')

    def test_bower_all_the_actions(self):
        remember_cwd(self)
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        stub_stdouts(self)
        stub_mod_call(self, cli)
        stub_base_which(self, which_bower)
        rt = self.setup_runtime()
        rt(['bower', '--install', '--view', '--init',
         'example.package1', 'example.package2'])
        result = json.loads(sys.stdout.getvalue())
        self.assertEqual(result['dependencies']['jquery'], '~3.1.0')
        self.assertEqual(result['dependencies']['underscore'], '~1.8.3')
        with open(join(tmpdir, 'bower.json')) as (fd):
            result = json.load(fd)
        self.assertEqual(result['dependencies']['jquery'], '~3.1.0')
        self.assertEqual(result['dependencies']['underscore'], '~1.8.3')
        args, kwargs = self.call_args
        self.assertEqual(args, (['bower', 'install'],))
        env = kwargs.pop('env', {})
        self.assertEqual(kwargs, {})
        self.assertEqual(env, finalize_env(env))