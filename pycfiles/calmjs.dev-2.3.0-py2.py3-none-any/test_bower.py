# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/tyu030/work/calmjs.bower/src/calmjs/bower/tests/test_bower.py
# Compiled at: 2016-09-04 08:22:57
from __future__ import unicode_literals
import warnings, unittest, json, os, sys
from os.path import join
from os.path import exists
from setuptools.dist import Distribution
from pkg_resources import WorkingSet
from calmjs import cli
from calmjs import dist
from calmjs import npm
from calmjs.utils import fork_exec
from calmjs.testing.utils import mkdtemp
from calmjs.testing.utils import make_dummy_dist
from calmjs.testing.utils import stub_item_attr_value
from calmjs.testing.utils import stub_base_which
from calmjs.testing.utils import stub_mod_call
from calmjs.testing.utils import stub_mod_check_interactive
from calmjs.testing.utils import stub_stdin
from calmjs.testing.utils import stub_stdouts
with warnings.catch_warnings():
    warnings.simplefilter(b'ignore')
    from calmjs.bower import Driver
    from calmjs.bower import bower as global_bower

def check_simple_namespace():
    """
    In Python < 3.3, namespace packages are not a thing so under many
    circumstances even with pkg_resources available, calmjs.bower will
    remain non-importable until calmjs is imported as a namespace (maybe
    even need at least a module from the real one as is the case with
    PyPy).  This will mean direction execution of the module will not be
    possible for those platforms, which will cause the standalone test
    to fail.  As this is not a standard way to execute calmjs.bower, the
    test will only run if calmjs.bower can be imported like so.

    The other way this can fail is due to mix of installation options
    between calmjs packages; if calmjs was installed as a wheel, with
    calmjs.bower installed as setup.py develop, the namespace resolution
    at the default level becomes broken.  If both are installed as a
    wheel or as development mode then it will work.

    The rest of the tests naturally test the standard execution methods
    and other parts of the code.
    """
    stdout, stderr = fork_exec([
     sys.executable, b'-c',
     b'python -c "from calmjs import bower; print(bower.__name__)"'])
    return stdout.strip() == b'calmjs.bower'


namespace_available = check_simple_namespace()

class DistCommandTestCase(unittest.TestCase):
    """
    Test case for the commands within.
    """

    def setUp(self):
        self.cwd = os.getcwd()
        app = make_dummy_dist(self, (
         (
          b'requires.txt', (b'\n').join([])),
         (
          b'bower.json', json.dumps({b'dependencies': {b'jquery': b'~1.11.0'}}))), b'foo', b'1.9.0')
        working_set = WorkingSet()
        working_set.add(app, self._calmjs_testing_tmpdir)
        stub_item_attr_value(self, dist, b'default_working_set', working_set)
        stub_stdouts(self)
        stub_mod_check_interactive(self, [cli], True)

    def tearDown(self):
        os.chdir(self.cwd)

    def test_no_args(self):
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        dist = Distribution(dict(script_name=b'setup.py', script_args=[
         b'bower'], name=b'foo'))
        dist.parse_command_line()
        dist.run_commands()
        out = sys.stdout.getvalue()
        self.assertIn(b'\n        "jquery": "~1.11.0"', out)

    def test_interactive_only(self):
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        dist = Distribution(dict(script_name=b'setup.py', script_args=[
         b'bower', b'-i'], name=b'foo'))
        dist.parse_command_line()
        dist.run_commands()
        out = sys.stdout.getvalue()
        self.assertIn(b'\n        "jquery": "~1.11.0"', out)

    def test_view(self):
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        dist = Distribution(dict(script_name=b'setup.py', script_args=[
         b'bower', b'--view'], name=b'foo'))
        dist.parse_command_line()
        dist.run_commands()
        out = sys.stdout.getvalue()
        self.assertIn(b'\n        "jquery": "~1.11.0"', out)

    def test_init_no_overwrite_default_input_interactive(self):
        tmpdir = mkdtemp(self)
        stub_stdin(self, b'')
        with open(os.path.join(tmpdir, b'bower.json'), b'w') as (fd):
            json.dump({b'dependencies': {}, b'devDependencies': {}}, fd, indent=None)
        os.chdir(tmpdir)
        dist = Distribution(dict(script_name=b'setup.py', script_args=[
         b'bower', b'--init', b'--interactive'], name=b'foo'))
        dist.parse_command_line()
        dist.run_commands()
        with open(os.path.join(tmpdir, b'bower.json')) as (fd):
            result = json.loads(fd.readline())
        self.assertEqual(result, {b'dependencies': {}, b'devDependencies': {}})
        stdout = sys.stdout.getvalue()
        self.assertTrue(stdout.startswith(b'running bower\n'))
        target = join(tmpdir, b'bower.json')
        self.assertIn(b"generating a flattened 'bower.json' for 'foo'\nGenerated 'bower.json' differs with '%s'" % target, stdout)
        self.assertIn(b'+     "dependencies": {\n+         "jquery": "~1.11.0"\n+     },', stdout)
        self.assertIn(b"not overwriting existing '%s'\n" % target, sys.stderr.getvalue())
        return

    def test_init_overwrite(self):
        tmpdir = mkdtemp(self)
        with open(os.path.join(tmpdir, b'bower.json'), b'w') as (fd):
            json.dump({b'dependencies': {}, b'devDependencies': {}}, fd)
        os.chdir(tmpdir)
        dist = Distribution(dict(script_name=b'setup.py', script_args=[
         b'bower', b'--init', b'--overwrite'], name=b'foo'))
        dist.parse_command_line()
        dist.run_commands()
        with open(os.path.join(tmpdir, b'bower.json')) as (fd):
            result = json.load(fd)
        self.assertEqual(result, {b'dependencies': {b'jquery': b'~1.11.0'}, b'devDependencies': {}, b'name': b'foo'})

    def test_init_merge(self):
        tmpdir = mkdtemp(self)
        with open(os.path.join(tmpdir, b'bower.json'), b'w') as (fd):
            json.dump({b'dependencies': {b'underscore': b'~1.8.0'}, 
               b'devDependencies': {b'sinon': b'~1.17.0'}}, fd)
        os.chdir(tmpdir)
        dist = Distribution(dict(script_name=b'setup.py', script_args=[
         b'bower', b'--init', b'--merge'], name=b'foo'))
        dist.parse_command_line()
        dist.run_commands()
        with open(os.path.join(tmpdir, b'bower.json')) as (fd):
            result = json.load(fd)
        self.assertEqual(result, {b'dependencies': {b'jquery': b'~1.11.0', b'underscore': b'~1.8.0'}, b'devDependencies': {b'sinon': b'~1.17.0'}, b'name': b'foo'})

    def test_init_merge_interactive_default(self):
        tmpdir = mkdtemp(self)
        stub_stdin(self, b'')
        with open(os.path.join(tmpdir, b'bower.json'), b'w') as (fd):
            json.dump({b'dependencies': {b'underscore': b'~1.8.0'}, 
               b'devDependencies': {b'sinon': b'~1.17.0'}}, fd)
        os.chdir(tmpdir)
        dist = Distribution(dict(script_name=b'setup.py', script_args=[
         b'bower', b'--init', b'--merge', b'--interactive'], name=b'foo'))
        dist.parse_command_line()
        dist.run_commands()
        stdout = sys.stdout.getvalue()
        self.assertIn(b'+         "jquery": "~1.11.0",', stdout)
        with open(os.path.join(tmpdir, b'bower.json')) as (fd):
            result = json.load(fd)
        self.assertEqual(result, {b'dependencies': {b'underscore': b'~1.8.0'}, b'devDependencies': {b'sinon': b'~1.17.0'}})

    def test_install_no_init(self):
        stub_mod_call(self, cli)
        stub_base_which(self, b'bower')
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        dist = Distribution(dict(script_name=b'setup.py', script_args=[
         b'bower', b'--install'], name=b'foo'))
        dist.parse_command_line()
        dist.run_commands()
        with open(os.path.join(tmpdir, b'bower.json')) as (fd):
            result = json.load(fd)
        self.assertEqual(result, {b'dependencies': {b'jquery': b'~1.11.0'}, b'devDependencies': {}, b'name': b'foo'})
        args, kwargs = self.call_args
        self.assertEqual(args, ([b'bower', b'install'],))

    def test_install_no_init_has_bower_json_interactive_default_input(self):
        stub_stdin(self, b'')
        stub_mod_call(self, cli)
        tmpdir = mkdtemp(self)
        with open(os.path.join(tmpdir, b'bower.json'), b'w') as (fd):
            json.dump({b'dependencies': {b'jquery': b'~3.0.0'}, b'devDependencies': {}}, fd)
        os.chdir(tmpdir)
        dist = Distribution(dict(script_name=b'setup.py', script_args=[
         b'bower', b'--install', b'--interactive'], name=b'foo'))
        dist.parse_command_line()
        dist.run_commands()
        with open(os.path.join(tmpdir, b'bower.json')) as (fd):
            result = json.load(fd)
        self.assertEqual(result, {b'dependencies': {b'jquery': b'~3.0.0'}, b'devDependencies': {}})
        self.assertIsNone(self.call_args)

    def test_install_false(self):
        stub_mod_call(self, cli)
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        dist = Distribution(dict(script_name=b'setup.py', script_args=[
         b'bower', b'--install', b'--dry-run'], name=b'foo'))
        dist.parse_command_line()
        dist.run_commands()
        self.assertFalse(exists(join(tmpdir, b'bower.json')))
        self.assertIsNone(self.call_args)


@unittest.skipIf(npm.get_npm_version() is None, b'npm not available')
class BowerTestCase(unittest.TestCase):
    """
    Test actual integration with node.
    """

    def setUp(self):
        self.cwd = os.getcwd()

    def tearDown(self):
        os.chdir(self.cwd)

    def test_integration(self):
        """
        Actually calling the real npm through the calmjs npm_install
        method on this package and then executing the result.
        """
        tmpdir = mkdtemp(self)
        os.chdir(tmpdir)
        npm.npm_install(b'calmjs.bower')
        bower = Driver.create()
        self.assertTrue(exists(join(tmpdir, b'node_modules', b'.bin', b'bower')))
        self.assertEqual(bower.get_bower_version(), (1, 7, 9))


class BowerRuntimeTestCase(unittest.TestCase):

    def test_standalone_main(self):
        stub_stdouts(self)
        with self.assertRaises(SystemExit):
            global_bower.runtime([b'-h'])
        self.assertIn(b'bower support for the calmjs', sys.stdout.getvalue())

    def test_standalone_main_version(self):
        stub_stdouts(self)
        with self.assertRaises(SystemExit):
            global_bower.runtime([b'-V'])
        self.assertIn(b'calmjs.bower', sys.stdout.getvalue())
        self.assertIn(b'from', sys.stdout.getvalue())

    def test_standalone_reuse_main(self):
        stub_stdouts(self)
        global_bower.runtime([b'calmjs', b'-vv'])
        result = json.loads(sys.stdout.getvalue())
        self.assertEqual(result[b'dependencies'], {})
        err = sys.stderr.getvalue()
        self.assertIn(b'DEBUG', err)

    @unittest.skipIf(not namespace_available, b'namespace module unavailable by default')
    def test_standalone_subprocess(self):
        stdout, stderr = fork_exec([
         sys.executable, b'-m', b'calmjs.bower', b'calmjs.bower', b'-vv'])
        result = json.loads(stdout)
        self.assertEqual(result[b'dependencies'], {})
        self.assertIn(b'DEBUG', stderr)

    def test_direct_invocation_acceptance(self):
        stdout, stderr = fork_exec([b'calmjs', b'bower', b'-vv', b'calmjs.bower'])
        result = json.loads(stdout)
        self.assertEqual(result[b'dependencies'], {})
        self.assertIn(b'DEBUG', stderr)