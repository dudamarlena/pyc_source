# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/test/simple.py
# Compiled at: 2018-07-11 18:15:30
import unittest as real_unittest
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_app, get_apps
from django.test import _doctest as doctest
from django.test.utils import setup_test_environment, teardown_test_environment
from django.test.testcases import OutputChecker, DocTestRunner
from django.utils import unittest
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
__all__ = 'DjangoTestSuiteRunner'
TEST_MODULE = 'tests'
doctestOutputChecker = OutputChecker()

def get_tests(app_module):
    parts = app_module.__name__.split('.')
    prefix, last = parts[:-1], parts[(-1)]
    try:
        test_module = import_module(('.').join(prefix + [TEST_MODULE]))
    except ImportError:
        if last == 'models':
            app_root = import_module(('.').join(prefix))
        else:
            app_root = app_module
        if not module_has_submodule(app_root, TEST_MODULE):
            test_module = None
        else:
            raise

    return test_module


def build_suite(app_module):
    """
    Create a complete Django test suite for the provided application module.
    """
    suite = unittest.TestSuite()
    if hasattr(app_module, 'suite'):
        suite.addTest(app_module.suite())
    else:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(app_module))
        try:
            suite.addTest(doctest.DocTestSuite(app_module, checker=doctestOutputChecker, runner=DocTestRunner))
        except ValueError:
            pass

    test_module = get_tests(app_module)
    if test_module:
        if hasattr(test_module, 'suite'):
            suite.addTest(test_module.suite())
        else:
            suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(test_module))
            try:
                suite.addTest(doctest.DocTestSuite(test_module, checker=doctestOutputChecker, runner=DocTestRunner))
            except ValueError:
                pass

    return suite


def build_test(label):
    """
    Construct a test case with the specified label. Label should be of the
    form model.TestClass or model.TestClass.test_method. Returns an
    instantiated test or test suite corresponding to the label provided.

    """
    parts = label.split('.')
    if len(parts) < 2 or len(parts) > 3:
        raise ValueError("Test label '%s' should be of the form app.TestCase or app.TestCase.test_method" % label)
    app_module = get_app(parts[0])
    test_module = get_tests(app_module)
    TestClass = getattr(app_module, parts[1], None)
    if TestClass is None:
        if test_module:
            TestClass = getattr(test_module, parts[1], None)
    try:
        if issubclass(TestClass, (unittest.TestCase, real_unittest.TestCase)):
            if len(parts) == 2:
                try:
                    return unittest.TestLoader().loadTestsFromTestCase(TestClass)
                except TypeError:
                    raise ValueError("Test label '%s' does not refer to a test class" % label)

            else:
                return TestClass(parts[2])
    except TypeError:
        pass

    tests = []
    for module in (app_module, test_module):
        try:
            doctests = doctest.DocTestSuite(module, checker=doctestOutputChecker, runner=DocTestRunner)
            for test in doctests:
                if test._dt_test.name in (
                 '%s.%s' % (module.__name__, ('.').join(parts[1:])),
                 '%s.__test__.%s' % (
                  module.__name__, ('.').join(parts[1:]))):
                    tests.append(test)

        except ValueError:
            pass

    if not tests:
        raise ValueError("Test label '%s' does not refer to a test" % label)
    return unittest.TestSuite(tests)


def partition_suite(suite, classes, bins):
    """
    Partitions a test suite by test type.

    classes is a sequence of types
    bins is a sequence of TestSuites, one more than classes

    Tests of type classes[i] are added to bins[i],
    tests with no match found in classes are place in bins[-1]
    """
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            partition_suite(test, classes, bins)
        else:
            for i in range(len(classes)):
                if isinstance(test, classes[i]):
                    bins[i].addTest(test)
                    break
            else:
                bins[(-1)].addTest(test)


def reorder_suite(suite, classes):
    """
    Reorders a test suite by test type.

    `classes` is a sequence of types

    All tests of type classes[0] are placed first, then tests of type
    classes[1], etc. Tests with no match in classes are placed last.
    """
    class_count = len(classes)
    bins = [ unittest.TestSuite() for i in range(class_count + 1) ]
    partition_suite(suite, classes, bins)
    for i in range(class_count):
        bins[0].addTests(bins[(i + 1)])

    return bins[0]


def dependency_ordered(test_databases, dependencies):
    """
    Reorder test_databases into an order that honors the dependencies
    described in TEST_DEPENDENCIES.
    """
    ordered_test_databases = []
    resolved_databases = set()
    dependencies_map = {}
    for sig, (_, aliases) in test_databases:
        all_deps = set()
        for alias in aliases:
            all_deps.update(dependencies.get(alias, []))

        if not all_deps.isdisjoint(aliases):
            raise ImproperlyConfigured('Circular dependency: databases %r depend on each other, but are aliases.' % aliases)
        dependencies_map[sig] = all_deps

    while test_databases:
        changed = False
        deferred = []
        for signature, (db_name, aliases) in test_databases:
            if dependencies_map[signature].issubset(resolved_databases):
                resolved_databases.update(aliases)
                ordered_test_databases.append((signature, (db_name, aliases)))
                changed = True
            else:
                deferred.append((signature, (db_name, aliases)))

        if not changed:
            raise ImproperlyConfigured('Circular dependency in TEST_DEPENDENCIES')
        test_databases = deferred

    return ordered_test_databases


class DjangoTestSuiteRunner(object):

    def __init__(self, verbosity=1, interactive=True, failfast=True, **kwargs):
        self.verbosity = verbosity
        self.interactive = interactive
        self.failfast = failfast

    def setup_test_environment(self, **kwargs):
        setup_test_environment()
        settings.DEBUG = False
        unittest.installHandler()

    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        suite = unittest.TestSuite()
        if test_labels:
            for label in test_labels:
                if '.' in label:
                    suite.addTest(build_test(label))
                else:
                    app = get_app(label)
                    suite.addTest(build_suite(app))

        else:
            for app in get_apps():
                suite.addTest(build_suite(app))

        if extra_tests:
            for test in extra_tests:
                suite.addTest(test)

        return reorder_suite(suite, (unittest.TestCase,))

    def setup_databases(self, **kwargs):
        from django.db import connections, DEFAULT_DB_ALIAS
        mirrored_aliases = {}
        test_databases = {}
        dependencies = {}
        default_sig = connections[DEFAULT_DB_ALIAS].creation.test_db_signature()
        for alias in connections:
            connection = connections[alias]
            if connection.settings_dict['TEST_MIRROR']:
                mirrored_aliases[alias] = connection.settings_dict['TEST_MIRROR']
            else:
                item = test_databases.setdefault(connection.creation.test_db_signature(), (
                 connection.settings_dict['NAME'], set()))
                item[1].add(alias)
                if 'TEST_DEPENDENCIES' in connection.settings_dict:
                    dependencies[alias] = connection.settings_dict['TEST_DEPENDENCIES']
                elif alias != DEFAULT_DB_ALIAS and connection.creation.test_db_signature() != default_sig:
                    dependencies[alias] = connection.settings_dict.get('TEST_DEPENDENCIES', [DEFAULT_DB_ALIAS])

        old_names = []
        mirrors = []
        for signature, (db_name, aliases) in dependency_ordered(test_databases.items(), dependencies):
            test_db_name = None
            for alias in aliases:
                connection = connections[alias]
                if test_db_name is None:
                    test_db_name = connection.creation.create_test_db(self.verbosity, autoclobber=not self.interactive)
                    destroy = True
                else:
                    connection.settings_dict['NAME'] = test_db_name
                    destroy = False
                old_names.append((connection, db_name, destroy))

        for alias, mirror_alias in mirrored_aliases.items():
            mirrors.append((alias, connections[alias].settings_dict['NAME']))
            connections[alias].settings_dict['NAME'] = connections[mirror_alias].settings_dict['NAME']

        return (old_names, mirrors)

    def run_suite(self, suite, **kwargs):
        return unittest.TextTestRunner(verbosity=self.verbosity, failfast=self.failfast).run(suite)

    def teardown_databases(self, old_config, **kwargs):
        """
        Destroys all the non-mirror databases.
        """
        old_names, mirrors = old_config
        for connection, old_name, destroy in old_names:
            if destroy:
                connection.creation.destroy_test_db(old_name, self.verbosity)

    def teardown_test_environment(self, **kwargs):
        unittest.removeHandler()
        teardown_test_environment()

    def suite_result(self, suite, result, **kwargs):
        return len(result.failures) + len(result.errors)

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        """
        Run the unit tests for all the test labels in the provided list.
        Labels must be of the form:
         - app.TestClass.test_method
            Run a single specific test method
         - app.TestClass
            Run all the test methods in a given class
         - app
            Search for doctests and unittests in the named application.

        When looking for tests, the test runner will look in the models and
        tests modules for the application.

        A list of 'extra' tests may also be provided; these tests
        will be added to the test suite.

        Returns the number of tests that failed.
        """
        self.setup_test_environment()
        suite = self.build_suite(test_labels, extra_tests)
        old_config = self.setup_databases()
        result = self.run_suite(suite)
        self.teardown_databases(old_config)
        self.teardown_test_environment()
        return self.suite_result(suite, result)