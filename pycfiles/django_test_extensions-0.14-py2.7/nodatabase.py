# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/test_extensions/testrunners/nodatabase.py
# Compiled at: 2011-10-26 15:19:51
"""
Test runner that doesn't use the database. Contributed by
Bradley Wright <intranation.com>
"""
import os, unittest
from glob import glob
from django.test.utils import setup_test_environment, teardown_test_environment
from django.conf import settings
from django.test.simple import get_app, build_test, build_suite
import coverage

def run_tests(test_labels, verbosity=1, interactive=True, extra_tests=[]):
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
    setup_test_environment()
    settings.DEBUG = False
    suite = unittest.TestSuite()
    modules_to_cover = []
    if test_labels:
        for label in test_labels:
            if '.' in label:
                suite.addTest(build_test(label))
            else:
                app = get_app(label)
                suite.addTest(build_suite(app))

    else:
        for app in get_apps():
            if not app.__name__.startswith('django'):
                app_name = app.__name__.replace('.models', '')
                files = glob('%s/*.py' % app_name)
                new_files = [ i for i in files if not i.endswith('models.py') ]
                modules_to_cover.extend(new_files)
                suite.addTest(build_suite(app))

        for test in extra_tests:
            suite.addTest(test)

    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    teardown_test_environment()
    return len(result.failures) + len(result.errors)


def run_tests_with_coverage(test_labels, verbosity=1, interactive=True, extra_tests=[], xml_out=False):
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
    setup_test_environment()
    settings.DEBUG = False
    suite = unittest.TestSuite()
    modules_to_cover = []
    cov = coverage.coverage()
    cov.erase()
    cov.start()
    if test_labels:
        for label in test_labels:
            if '.' in label:
                suite.addTest(build_test(label))
            else:
                app = get_app(label)
                suite.addTest(build_suite(app))

    else:
        for app in get_apps():
            if not app.__name__.startswith('django'):
                app_name = app.__name__.replace('.models', '')
                files = glob('%s/*.py' % app_name)
                new_files = [ i for i in files if not i.endswith('models.py') ]
                modules_to_cover.extend(new_files)
                suite.addTest(build_suite(app))

        for test in extra_tests:
            suite.addTest(test)

    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    teardown_test_environment()
    cov.stop()
    print ''
    print '--------------------------'
    print 'Unit test coverage results'
    print '--------------------------'
    print ''
    if xml_out:
        if not os.path.isdir(os.path.join('temp', 'xml')):
            os.makedirs(os.path.join('temp', 'xml'))
        output_filename = 'temp/xml/coverage_output.xml'
        cov.xml_report(morfs=coverage_modules, outfile=output_filename)
    cov.report(modules_to_cover, show_missing=1)
    return len(result.failures) + len(result.errors)


def run_tests_with_xmlcoverage(test_labels, verbosity=1, interactive=True, extra_tests=[]):
    return run_tests_with_coverage(test_labels, verbosity, interactive, extra_tests, xml_out=True)