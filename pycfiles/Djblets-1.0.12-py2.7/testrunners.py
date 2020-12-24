# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/testing/testrunners.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import os, shutil, stat, sys, tempfile, nose
from django.core.management import execute_from_command_line
from django.test.runner import DiscoverRunner
try:
    from PIL import Image
    Image.init()
except ImportError:
    try:
        import Image
        Image.init()
    except ImportError:
        pass

from django.conf import settings
from djblets.cache.serials import generate_media_serial

class TestRunner(DiscoverRunner):
    """Test runner for standard Djblets-based projects.

    This class provides all the common setup for settings, databases, and
    directories that are generally needed by Django projects using Djblets.
    Much of the behavior can be overridden by subclasses.

    `nose <http://nose.readthedocs.io/en/latest/>`_ is used to run the test
    suites. The options can be configured through :py:attr:`nose_options`.

    This can be subclassed in order to set the settings for the test run, or
    it can be instantiated with those settings passed in as keyword arguments.
    """
    nose_options = [
     b'-v',
     b'--match=^test',
     b'--with-id',
     b'--with-doctest',
     b'--doctest-extension=.txt']
    test_packages = []
    needs_collect_static = True

    def __init__(self, *args, **kwargs):
        """Initialize the test runner.

        The caller can override any of the options otherwise defined on the
        class.

        Args:
            nose_options (list, optional):
                A list of options used for nose. See :py:attr:`nose_options`.

            test_packages (list, optional):
                A list of Python package/module names to test. See
                :py:attr:`test_packages`.

            needs_collect_static (bool, optional):
                Whether or not ``collectstatic`` needs to be run before
                tests. See :py:attr:`needs_collect_static`.
        """
        super(TestRunner, self).__init__(*args, **kwargs)
        try:
            self.nose_options = kwargs[b'nose_options']
        except KeyError:
            pass

        try:
            self.test_packages = kwargs[b'test_packages']
        except KeyError:
            pass

        try:
            self.needs_collect_static = kwargs[b'needs_collect_static']
        except KeyError:
            pass

    def setup_test_environment(self, *args, **kwargs):
        """Set up an environment for the unit tests.

        This will handle setting all the default settings for a Djblets-based
        project and will create the directory structure needed for the tests
        in a temp directory.

        Subclasses can override this to provide additional setup logic.

        This must be called before :py:meth:`run_tests`.

        Args:
            *args (tuple):
                Additional positional arguments to pass to Django's version
                of this method.

            **kwargs (dict):
                Additional keyword arguments to pass to Django's version
                of this method.
        """
        super(TestRunner, self).setup_test_environment(*args, **kwargs)
        settings.SITE_ROOT = b'/'
        settings.AJAX_SERIAL = 123
        settings.TEMPLATE_SERIAL = 123
        settings.PASSWORD_HASHERS = ('django.contrib.auth.hashers.SHA1PasswordHasher', )
        settings.STATICFILES_STORAGE = b'django.contrib.staticfiles.storage.StaticFilesStorage'
        settings.EMAIL_ENABLE_SMART_SPOOFING = False
        self.tempdir = tempfile.mkdtemp(prefix=b'rb-tests-')
        settings.STATIC_URL = settings.SITE_ROOT + b'static/'
        settings.MEDIA_URL = settings.SITE_ROOT + b'media/'
        settings.STATIC_ROOT = os.path.join(self.tempdir, b'static')
        settings.MEDIA_ROOT = os.path.join(self.tempdir, b'media')
        required_dirs = self.setup_dirs() + [
         settings.STATIC_ROOT,
         settings.MEDIA_ROOT,
         os.path.join(settings.MEDIA_ROOT, b'ext'),
         os.path.join(settings.STATIC_ROOT, b'ext')]
        for dirname in required_dirs:
            if not os.path.exists(dirname):
                os.makedirs(dirname)

        if self.needs_collect_static:
            execute_from_command_line([
             __file__, b'collectstatic', b'--noinput', b'-v', b'0'])
        generate_media_serial()

    def teardown_test_environment(self, *args, **kwargs):
        """Tear down the environment for the unit tests.

        This will clean up the temp directory structure.It must be called after
        :py:meth:`run_tests`.

        Args:
            *args (tuple):
                Additional positional arguments to pass to Django's version
                of this method.

            **kwargs (dict):
                Additional keyword arguments to pass to Django's version
                of this method.
        """
        shutil.rmtree(self.tempdir)
        super(TestRunner, self).teardown_test_environment(*args, **kwargs)

    def run_tests(self, test_labels=[], argv=None, *args, **kwargs):
        """Run the test suite.

        Args:
            test_labels (list of unicode, optional):
                Specific tests to run.

            argv (list of unicode, optional):
                Additional arguments for nose. If not specified, sys.argv is
                used.

            *args (tuple, unused):
                Unused additional positional arguments.

            **kwargs (dict, unused):
                Unused additional keyword arguments.

        Returns:
            int:
            The exit code. 0 means all tests passed, while 1 means there were
            failures.
        """
        if argv is None:
            argv = sys.argv
        self.setup_test_environment()
        old_config = self.setup_databases()
        self.nose_argv = [
         argv[0]] + self.nose_options
        if b'--with-coverage' in argv:
            self.nose_argv += [b'--with-coverage'] + [ b'--cover-package=%s' % package_name for package_name in self.test_packages
                                                     ]
            argv.remove(b'--with-coverage')
        known_file = os.path.join(os.path.dirname(__file__), b'__init__.py')
        if os.path.exists(known_file) and os.stat(known_file).st_mode & stat.S_IXUSR:
            self.nose_argv.append(b'--exe')
        if len(argv) > 2 and b'--' in argv:
            self.nose_argv += argv[argv.index(b'--') + 1:]
        self.nose_argv += [ test_label for test_label in test_labels if not test_label.startswith(b'-') and test_label not in self.nose_argv
                          ]
        specific_tests = [ test_name for test_name in self.nose_argv[1:] if not test_name.startswith(b'-')
                         ]
        if not specific_tests:
            self.nose_argv += self.test_packages
        self.run_nose()
        self.teardown_databases(old_config)
        self.teardown_test_environment()
        if self.result.success:
            return 0
        else:
            return 1
            return

    def setup_dirs(self):
        """Set up directories to create and use.

        This can return one or more directory paths that need to be created
        before the tests can be run. It may also store settings pointing to
        those paths.

        This is not responsible for creating the directories. Any returned
        paths will be created automatically.

        Returns:
            list of unicode:
            A list of directory paths to create.
        """
        return []

    def run_nose(self):
        """Run the unit tests using nose.

        This will use nose to run the tests, storing the result.

        Returns:
            nose.core.TestProgram:
            The result from the run.
        """
        self.result = nose.main(argv=self.nose_argv, exit=False)