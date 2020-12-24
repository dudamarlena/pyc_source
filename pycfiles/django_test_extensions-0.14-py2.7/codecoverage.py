# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/test_extensions/testrunners/codecoverage.py
# Compiled at: 2011-03-12 15:46:24
import coverage, os, sys
from inspect import getmembers, ismodule
from django.conf import settings
from django.test.simple import run_tests as django_test_runner
from django.db.models import get_app, get_apps
from django.utils.functional import curry
from nodatabase import run_tests as nodatabase_run_tests

def is_wanted_module(mod):
    included = getattr(settings, 'COVERAGE_INCLUDE_MODULES', [])
    excluded = getattr(settings, 'COVERAGE_EXCLUDE_MODULES', [])
    marked_to_include = None
    for exclude in excluded:
        if exclude.endswith('*'):
            if mod.__name__.startswith(exclude[:-1]):
                marked_to_include = False
        elif mod.__name__ == exclude:
            marked_to_include = False

    for include in included:
        if include.endswith('*'):
            if mod.__name__.startswith(include[:-1]):
                marked_to_include = True
        elif mod.__name__ == include:
            marked_to_include = True

    if marked_to_include is None:
        if included and excluded:
            marked_to_include = False
        elif excluded:
            marked_to_include = True
        elif included:
            marked_to_include = False
        else:
            marked_to_include = True
    return marked_to_include


def get_coverage_modules(app_module):
    """
    Returns a list of modules to report coverage info for, given an
    application module.
    """
    app_path = app_module.__name__.split('.')[:-1]
    coverage_module = __import__(('.').join(app_path), {}, {}, app_path[(-1)])
    return [
     coverage_module] + [ attr for name, attr in getmembers(coverage_module) if ismodule(attr) and name != 'tests'
                        ]


def get_all_coverage_modules(app_module):
    """
    Returns all possible modules to report coverage on, even if they
    aren't loaded.
    """
    app_path = app_module.__name__.split('.')[:-1]
    app_package = __import__(('.').join(app_path), {}, {}, app_path[(-1)])
    app_dirpath = app_package.__path__[(-1)]
    mod_list = []
    for root, dirs, files in os.walk(app_dirpath):
        root_path = app_path + root[len(app_dirpath):].split(os.path.sep)[1:]
        excludes = getattr(settings, 'EXCLUDE_FROM_COVERAGE', [])
        if app_path[0] not in excludes:
            for file in files:
                if file.lower().endswith('.py'):
                    mod_name = file[:-3].lower()
                    try:
                        mod = __import__(('.').join(root_path + [mod_name]), {}, {}, mod_name)
                    except ImportError:
                        pass
                    else:
                        mod_list.append(mod)

    return mod_list


def run_tests(test_labels, verbosity=1, interactive=True, extra_tests=[], nodatabase=False, xml_out=False, callgraph=False, html_only=False):
    """
    Test runner which displays a code coverage report at the end of the
    run.
    """
    cov = coverage.coverage()
    cov.erase()
    cov.use_cache(0)
    test_labels = test_labels or getattr(settings, 'TEST_APPS', None)
    cover_branch = getattr(settings, 'COVERAGE_BRANCH_COVERAGE', False)
    cov = coverage.coverage(branch=cover_branch, cover_pylib=False)
    cov.use_cache(0)
    coverage_modules = []
    if test_labels:
        for label in test_labels:
            if '.' not in label:
                app = get_app(label)
                coverage_modules.extend(get_all_coverage_modules(app))

    else:
        for app in get_apps():
            coverage_modules.extend(get_all_coverage_modules(app))

    morfs = filter(is_wanted_module, coverage_modules)
    if callgraph:
        try:
            import pycallgraph
            _included = getattr(settings, 'COVERAGE_INCLUDE_MODULES', [])
            _excluded = getattr(settings, 'COVERAGE_EXCLUDE_MODULES', [])
            _included = [ i.strip('*') + '*' for i in _included ]
            _excluded = [ i.strip('*') + '*' for i in _included ]
            _filter_func = pycallgraph.GlobbingFilter(include=_included or ['*'])
            pycallgraph_enabled = True
        except ImportError:
            pycallgraph_enabled = False

    else:
        pycallgraph_enabled = False
    cov.start()
    if pycallgraph_enabled:
        pycallgraph.start_trace(filter_func=_filter_func)
    if nodatabase:
        results = nodatabase_run_tests(test_labels, verbosity, interactive, extra_tests)
    else:
        results = django_test_runner(test_labels, verbosity, interactive, extra_tests)
    if callgraph and pycallgraph_enabled:
        pycallgraph.stop_trace()
    cov.stop()
    if getattr(settings, 'COVERAGE_HTML_REPORT', False) or os.environ.get('COVERAGE_HTML_REPORT'):
        output_dir = getattr(settings, 'COVERAGE_HTML_DIRECTORY', 'covhtml')
        report_method = curry(cov.html_report, directory=output_dir)
        if callgraph and pycallgraph_enabled:
            callgraph_path = output_dir + '/' + 'callgraph.png'
            pycallgraph.make_dot_graph(callgraph_path)
        print >> sys.stdout
        print >> sys.stdout, "Coverage HTML reports were output to '%s'" % output_dir
        if callgraph:
            if pycallgraph_enabled:
                print >> sys.stdout, "Call graph was output to '%s'" % callgraph_path
            else:
                print >> sys.stdout, "Call graph was not generated: Install 'pycallgraph' module to do so"
    else:
        report_method = cov.report
    if coverage_modules:
        if xml_out:
            if not os.path.isdir(os.path.join('temp', 'xml')):
                os.makedirs(os.path.join('temp', 'xml'))
            output_filename = 'temp/xml/coverage_output.xml'
            cov.xml_report(morfs=coverage_modules, outfile=output_filename)
        if not html_only:
            cov.report(coverage_modules, show_missing=1)
    return results


def run_tests_xml(test_labels, verbosity=1, interactive=True, extra_tests=[], nodatabase=False):
    return run_tests(test_labels, verbosity, interactive, extra_tests, nodatabase, xml_out=True)