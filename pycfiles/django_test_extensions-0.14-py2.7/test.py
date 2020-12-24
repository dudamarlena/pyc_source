# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/test_extensions/management/commands/test.py
# Compiled at: 2011-03-12 15:46:24
import sys
from optparse import make_option
from django.core import management
from django.conf import settings
from django.db.models import get_app, get_apps
from django.core.management.base import BaseCommand
try:
    from django.test.simple import DjangoTestSuiteRunner
    xml_runner = 'test_extensions.testrunners.xmloutput.XMLTestSuiteRunner'
except ImportError:
    xml_runner = 'test_extensions.testrunners.xmloutput.run_tests'

skippers = []

class Command(BaseCommand):
    option_list = BaseCommand.option_list
    if '--verbosity' not in [ opt.get_opt_string() for opt in BaseCommand.option_list ]:
        option_list += (
         make_option('--verbosity', action='store', dest='verbosity', default='0', type='choice', choices=['0', '1', '2'], help='Verbosity level; 0=minimal, 1=normal, 2=all'),)
    option_list += (
     make_option('--noinput', action='store_false', dest='interactive', default=True, help='Tells Django to NOT prompt the user for input of any kind.'),
     make_option('--callgraph', action='store_true', dest='callgraph', default=False, help='Generate execution call graph (slow!)'),
     make_option('--coverage', action='store_true', dest='coverage', default=False, help='Show coverage details'),
     make_option('--coverage_html_only', action='store_true', dest='coverage_html_only', default=False, help='Supress stdout output if using HTML output. Else, is ignored'),
     make_option('--xmlcoverage', action='store_true', dest='xmlcoverage', default=False, help='Show coverage details and write them into a xml file'),
     make_option('--figleaf', action='store_true', dest='figleaf', default=False, help='Produce figleaf coverage report'),
     make_option('--xml', action='store_true', dest='xml', default=False, help='Produce JUnit-type xml output'),
     make_option('--nodb', action='store_true', dest='nodb', default=False, help='No database required for these tests'),
     make_option('--failfast', action='store_true', dest='failfast', default=False, help='Tells Django to stop running the test suite after first failed test.'))
    help = 'Custom test command which allows for\n        specifying different test runners.'
    args = '[appname ...]'
    requires_model_validation = True

    def handle(self, *test_labels, **options):
        verbosity = int(options.get('verbosity', 1))
        interactive = options.get('interactive', True)
        callgraph = options.get('callgraph', False)
        failfast = options.get('failfast', False)
        coverage_html_only = options.get('coverage_html_only', False)
        management.get_commands()
        management._commands['syncdb'] = 'django.core'
        if options.get('nodb'):
            if options.get('xmlcoverage'):
                test_runner_name = 'test_extensions.testrunners.nodatabase.run_tests_with_xmlcoverage'
            elif options.get('coverage'):
                test_runner_name = 'test_extensions.testrunners.nodatabase.run_tests_with_coverage'
            else:
                test_runner_name = 'test_extensions.testrunners.nodatabase.run_tests'
        else:
            if options.get('xmlcoverage'):
                test_runner_name = 'test_extensions.testrunners.codecoverage.run_tests_xml'
            elif options.get('coverage'):
                test_runner_name = 'test_extensions.testrunners.codecoverage.run_tests'
            elif options.get('figleaf'):
                test_runner_name = 'test_extensions.testrunners.figleafcoverage.run_tests'
            elif options.get('xml'):
                test_runner_name = xml_runner
            else:
                test_runner_name = settings.TEST_RUNNER
            test_path = test_runner_name.split('.')
            if len(test_path) > 1:
                test_module_name = ('.').join(test_path[:-1])
            else:
                test_module_name = '.'
            test_module = __import__(test_module_name, {}, {}, test_path[(-1)])
            test_runner = getattr(test_module, test_path[(-1)])
            if hasattr(settings, 'SKIP_TESTS'):
                if not test_labels:
                    test_labels = list()
                    for app in get_apps():
                        test_labels.append(app.__name__.split('.')[(-2)])

                for app in settings.SKIP_TESTS:
                    try:
                        test_labels = list(test_labels)
                        test_labels.remove(app)
                    except ValueError:
                        pass

            test_options = dict(verbosity=verbosity, interactive=interactive)
            if options.get('coverage'):
                test_options['callgraph'] = callgraph
                test_options['html_only'] = coverage_html_only
            try:
                failures = test_runner(test_labels, **test_options)
            except TypeError:
                test_options['failfast'] = failfast
                failures = test_runner(**test_options).run_tests(test_labels)

        if failures:
            sys.exit(failures)