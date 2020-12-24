# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/google/apputils/setup_command.py
# Compiled at: 2015-02-20 20:25:16
"""Setuptools extension for running Google-style Python tests.

Google-style Python tests differ from normal Python tests in that each test
module is intended to be executed as an independent script. In particular, the
test fixture code in basetest.main() that executes module-wide setUp() and
tearDown() depends on __main__ being the module under test. This conflicts with
the usual setuptools test style, which uses a single TestSuite to run all of a
package's tests.

This package provides a new setuptools command, google_test, that runs all of
the google-style tests found in a specified directory.

NOTE: This works by overriding sys.modules['__main__'] with the module under
test, but still runs tests in the same process. Thus it will *not* work if your
tests depend on any of the following:
  - Per-process (as opposed to per-module) initialization.
  - Any entry point that is not basetest.main().

To use the google_test command in your project, do something like the following:

In setup.py:
  setup(
      name = "mypackage",
      ...
      setup_requires = ["google-apputils>=0.2"],
      google_test_dir = "tests",
      )

Run:
  $ python setup.py google_test
"""
from distutils import errors
import imp, os, re, shlex, sys, traceback
from setuptools.command import test

def ValidateGoogleTestDir(unused_dist, unused_attr, value):
    """Validate that the test directory is a directory."""
    if not os.path.isdir(value):
        raise errors.DistutilsSetupError('%s is not a directory' % value)


class GoogleTest(test.test):
    """Command to run Google-style tests after in-place build."""
    description = 'run Google-style tests after in-place build'
    _DEFAULT_PATTERN = '_(?:unit|reg)?test\\.py$'
    user_options = [
     ('test-dir=', 'd', 'Look for test modules in specified directory.'),
     (
      'test-module-pattern=', 'p',
      'Pattern for matching test modules. Defaults to %r. Only source files (*.py) will be considered, even if more files match this pattern.' % _DEFAULT_PATTERN),
     ('test-args=', 'a', 'Arguments to pass to basetest.main(). May only make sense if test_module_pattern matches exactly one test.')]

    def initialize_options(self):
        self.test_dir = None
        self.test_module_pattern = self._DEFAULT_PATTERN
        self.test_args = ''
        self.test_suite = True
        return

    def finalize_options(self):
        if self.test_dir is None:
            if self.distribution.google_test_dir:
                self.test_dir = self.distribution.google_test_dir
            else:
                raise errors.DistutilsOptionError('No test directory specified')
        self.test_module_pattern = re.compile(self.test_module_pattern)
        self.test_args = shlex.split(self.test_args)
        return

    def _RunTestModule(self, module_path):
        """Run a module as a test module given its path.

    Args:
      module_path: The path to the module to test; must end in '.py'.

    Returns:
      True if the tests in this module pass, False if not or if an error occurs.
    """
        path, filename = os.path.split(module_path)
        old_argv = sys.argv[:]
        old_path = sys.path[:]
        old_modules = sys.modules.copy()
        sys.path.insert(0, path)
        module_name = filename.replace('.py', '')
        import_tuple = imp.find_module(module_name, [path])
        module = imp.load_module(module_name, *import_tuple)
        sys.modules['__main__'] = module
        sys.argv = [module.__file__] + self.test_args
        import basetest
        try:
            try:
                sys.stderr.write('Testing %s\n' % module_name)
                basetest.main()
                return False
            except SystemExit as e:
                returncode, = e.args
                return not returncode
            except:
                traceback.print_exc()
                return False

        finally:
            sys.argv[:] = old_argv
            sys.path[:] = old_path
            sys.modules.clear()
            sys.modules.update(old_modules)

    def run_tests(self):
        ok = True
        for path, _, filenames in os.walk(self.test_dir):
            for filename in filenames:
                if not filename.endswith('.py'):
                    continue
                file_path = os.path.join(path, filename)
                if self.test_module_pattern.search(file_path):
                    ok &= self._RunTestModule(file_path)

        sys.exit(int(not ok))