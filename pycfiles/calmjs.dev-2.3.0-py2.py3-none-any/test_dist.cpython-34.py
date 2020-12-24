# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/tyu030/work/calmjs.bower/src/calmjs/bower/tests/test_dist.py
# Compiled at: 2016-08-30 06:11:11
# Size of source mod 2**32: 4370 bytes
import unittest, json, sys, textwrap
from os.path import join
from pkg_resources import WorkingSet
from calmjs import dist
from calmjs.utils import fork_exec
from calmjs.testing.utils import mkdtemp
from calmjs.testing.utils import make_dummy_dist

class DistTestCase(unittest.TestCase):

    def test_node_modules_registry_flattening(self):
        lib = make_dummy_dist(self, (
         (
          'requires.txt', '\n'.join([])),
         (
          'bower.json',
          json.dumps({'dependencies': {'jquery': '~1.8.3', 
                            'underscore': '1.8.3'}})),
         (
          'extras_calmjs.json',
          json.dumps({'bower_components': {'jquery': 'jquery/dist/jquery.js', 
                                'underscore': 'underscore/underscore-min.js'}, 
           'something_else': {'parent': 'lib'}}))), 'lib', '1.0.0')
        app = make_dummy_dist(self, (
         (
          'requires.txt',
          '\n'.join([
           'lib>=1.0.0'])),
         (
          'bower.json',
          json.dumps({'dependencies': {'jquery': '~3.0.0'}})),
         (
          'extras_calmjs.json',
          json.dumps({'bower_components': {'jquery': 'jquery/dist/jquery.min.js'}, 
           'something_else': {'child': 'named'}}))), 'app', '2.0')
        working_set = WorkingSet()
        working_set.add(lib, self._calmjs_testing_tmpdir)
        working_set.add(app, self._calmjs_testing_tmpdir)
        results = dist.flatten_extras_calmjs(['app'], working_set=working_set)
        self.assertEqual(results['bower_components'], {'jquery': 'jquery/dist/jquery.min.js', 
         'underscore': 'underscore/underscore-min.js'})
        self.assertEqual(results['something_else'], {'child': 'named'})


class DistIntegrationTestCase(unittest.TestCase):
    """DistIntegrationTestCase"""

    def setUp(self):
        """
        Set up the dummy test files.
        """
        self.pkg_root = mkdtemp(self)
        setup_py = join(self.pkg_root, 'setup.py')
        dummy_pkg = join(self.pkg_root, 'dummy_pkg.py')
        contents = (
         (
          setup_py,
          "\n                from setuptools import setup\n                setup(\n                    py_modules=['dummy_pkg'],\n                    name='dummy_pkg',\n                    bower_json={\n                        'dependencies': {\n                            'jquery': '~3.0.0',\n                        },\n                    },\n                    extras_calmjs={\n                        'bower_components': {\n                            'jquery': 'jquery/dist/jquery.js',\n                        },\n                    },\n                    zip_safe=False,\n                )\n            "),
         (
          dummy_pkg,
          "\n            foo = 'bar'\n            "))
        for fn, content in contents:
            with open(fn, 'w') as (fd):
                fd.write(textwrap.dedent(content).lstrip())

    def test_setup_egg_info(self):
        """
        Emulate the execution of ``python setup.py egg_info``.

        Ensure everything is covered.
        """
        stdout, stderr = fork_exec([
         sys.executable, 'setup.py', 'egg_info'], cwd=self.pkg_root)
        self.assertIn('writing bower_json', stdout)
        self.assertIn('writing extras_calmjs', stdout)
        egg_root = join(self.pkg_root, 'dummy_pkg.egg-info')
        with open(join(egg_root, 'bower.json')) as (fd):
            self.assertEqual(json.load(fd), {'dependencies': {'jquery': '~3.0.0'}})
        with open(join(egg_root, 'extras_calmjs.json')) as (fd):
            self.assertEqual(json.load(fd), {'bower_components': {'jquery': 'jquery/dist/jquery.js'}})