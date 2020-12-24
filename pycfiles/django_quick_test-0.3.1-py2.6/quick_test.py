# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quick_test/management/commands/quick_test.py
# Compiled at: 2011-08-01 12:40:38
from django.core.management.base import BaseCommand
from optparse import make_option
import sys

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
     make_option('--noinput', action='store_false', dest='interactive', default=True, help='Tells Django to NOT prompt the user for input of any kind.'),
     make_option('--failfast', action='store_true', dest='failfast', default=False, help='Tells Django to stop running the test suite after first failed test.'))
    help = 'Runs the test suite for the specified applications, or the entire site if no apps are specified.'
    args = '[appname ...]'
    requires_model_validation = False

    def handle(self, *test_labels, **options):
        verbosity = int(options.get('verbosity', 1))
        interactive = options.get('interactive', True)
        failfast = options.get('failfast', False)
        test_module = __import__('quick_test.testrunner', {}, {}, 'NoseTestSuiteRunner')
        TestRunner = getattr(test_module, 'NoseTestSuiteRunner')
        if hasattr(TestRunner, 'func_name'):
            import warnings
            warnings.warn('Function-based test runners are deprecated. Test runners should be classes with a run_tests() method.', PendingDeprecationWarning)
            failures = TestRunner(test_labels, verbosity=verbosity, interactive=interactive)
        else:
            test_runner = TestRunner(verbosity=verbosity, interactive=interactive, failfast=failfast)
            failures = test_runner.run_tests(test_labels)
        if failures:
            sys.exit(bool(failures))