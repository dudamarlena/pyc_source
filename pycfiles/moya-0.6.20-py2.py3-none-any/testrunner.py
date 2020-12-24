# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/sub/testrunner.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from __future__ import print_function
from ...command import SubCommand
from ...context import Context
from ...console import Console, Cell
from ...compat import text_type
from ... import namespaces
from ... import build
from datetime import datetime
from collections import Counter
import sys

class TestRunner(object):

    def __init__(self, context, results):
        self.context = context
        self.results = results

    def __enter__(self):
        self.console = Console(text=True)
        self.context[b'.console'] = self.console

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def safe_to_string(obj):
    """Try to build a string representation of this object"""
    try:
        s = text_type(obj)
    except:
        try:
            s = repr(obj)
        except:
            s = b'<failed to create string representation>'

    return s


class TestResults(object):

    def __init__(self, context, lib, suite):
        self.lib = lib
        self.context = context
        self.suite = suite
        self.setup_error = None
        self.teardown_error = None
        self.tests = []
        self.case = None
        self.output = []
        self.group = None
        return

    def __repr__(self):
        return b'<testresults>'

    def __moyaconsole__(self, console):
        self.summary(console)

    def clear_output(self):
        output = (b'\n').join(self.output)
        del self.output[:]
        return output

    def get_output(self):
        text = self.context[b'.console'].get_text()
        self.context[b'.console'] = Console(text=True)
        return text

    def add_setup_error(self, element, error):
        self.setup_error = {b'element': element, b'error': error, 
           b'console_trace': self.get_output()}

    def add_teardown_error(self, element, error):
        self.teardown_error = {b'element': element, b'error': error, 
           b'console_trace': self.get_output()}

    def _test_result(self, status, **kwargs):
        result = {b'status': status}
        result.update(kwargs)
        console_trace = self.get_output()
        result.update(case=self.case, group=self.group, console_trace=console_trace)
        self.tests.append(result)
        return result

    def add_error(self, element, error):
        console = Console(text=True, width=120)
        console.obj(self.context, error)
        trace = console.get_text()
        self._test_result(b'error', element=element, error=error, trace=trace, description=self.case.description, msg=safe_to_string(error))

    def add_pass(self, element):
        self._test_result(b'pass', element=element, description=self.case.description)

    def add_fail(self, element, msg):
        self._test_result(b'fail', element=element, msg=msg, description=self.case.description)

    def summary(self, console):
        passes, fails, errors = self.stats
        results = {}
        results[b'pass'] = passes
        results[b'fail'] = fails
        results[b'error'] = errors
        summary = (b'{fail} fail(s), {error} error(s), {pass} pass(es)').format(**results)
        if results[b'error'] or results[b'fail']:
            console.text(summary, fg=b'red', bold=True)
        else:
            console.text(summary, fg=b'green', bold=True)

    @property
    def stats(self):
        results = Counter(fail=0, error=0)
        results[b'pass'] = 0
        if self.setup_error is not None:
            results[b'error'] += 1
        if self.teardown_error is not None:
            results[b'error'] += 1
        for test in self.tests:
            results[test[b'status']] += 1

        return (
         results[b'pass'], results[b'fail'], results[b'error'])

    def report(self, console, show_trace=True, show_passes=False, verbose=False):

        def show_result(result, description, msg=None):
            if result == b'pass':
                fg = b'green'
            else:
                fg = b'red'
            console((b'[{}]\t').format(result.upper()), fg=fg, bold=result != b'pass')((b' {}').format(description), dim=result == b'pass')
            if msg:
                console((b' - {}').format(msg), italic=True)
            console.nl()

        def show_output(test):
            if show_trace:
                trace = test[b'console_trace'].strip()
                if trace:
                    console.table([[Cell(trace, fg=b'cyan', bold=True)]])
                    console.div()

        if verbose:
            console.div((b'[{}]').format(self.suite), fg=b'magenta', bold=True, italic=False)
        if self.setup_error is not None:
            console.error(b'setup failed, unable to run tests')
            console(self.setup_error[b'error'])
            show_output(self.setup_error)
        if self.teardown_error is not None:
            console.error(b'teardown failed')
            console(self.teardown_error[b'error'])
            show_output(self.teardown_error)
        for test in self.tests:
            status = test[b'status']
            if status == b'pass' and not show_passes:
                continue
            show_result(status, test[b'description'], test.get(b'msg', None))
            if status == b'error' and show_trace:
                console(test[b'error'])
            if status == b'fail' and show_trace:
                node = test[b'element']
                console.div(b'failed here', dim=True)
                console(b'File "%s"' % node._location).nl()
                console.xmlsnippet(node._code, node.source_line or 0, extralines=2 if verbose else 0)
            if status != b'pass':
                show_output(test)

        return


class Test(SubCommand):
    """Run unit tests"""
    help = b'unit tests'

    def add_arguments(self, parser):
        parser.add_argument(dest=b'location', default=None, nargs=b'+', help=b"location of library (directory containing lib.ini) or a python import if preceded by 'py:', e.g. py:moya.libs.auth")
        parser.add_argument(b'--verbose', dest=b'verbose', action=b'store_true', help=b'add extra information to reports')
        parser.add_argument(b'-o', b'--output', dest=b'output', default=None, metavar=b'PATH', help=b'write html report')
        parser.add_argument(b'--summary', dest=b'summary', default=False, action=b'store_true', help=b'summarize all results')
        parser.add_argument(b'-a', b'--automated', dest=b'automated', default=False, action=b'store_true', help=b'disable breakpoints or anything that may block for user input')
        parser.add_argument(b'-q', b'--quick', action=b'store_true', default=False, help=b"run tests that aren't marked as 'slow'")
        parser.add_argument(b'--exclude', dest=b'exclude', default=None, nargs=b'+', metavar=b'GROUP', help=b'exclude tests in a group or groups')
        parser.add_argument(b'--group', dest=b'group', default=None, nargs=b'+', metavar=b'GROUP', help=b'run only tests in a group or groups')
        return

    def run(self):
        args = self.args
        location = args.location
        console = self.console
        if args.output is not None:
            from moya.console import Console
            console = Console(html=True)

        def write_output():
            if args.output is not None:
                from moya import consolehtml
                html = console.get_text()
                html = consolehtml.render_console_html(html)
                with open(args.output, b'wb') as (f):
                    f.write(html.encode(b'utf-8'))
            return

        test_libs = []
        for location in args.location:
            archive, lib = build.build_lib(location)
            lib_name = lib.long_name
            if archive.failed_documents:
                sys.stderr.write(b'library build failed\n')
                build.render_failed_documents(archive, console)
                write_output()
                return -1
            test_libs.append(lib)

        for lib_name in test_libs:
            if not lib.load_tests():
                sys.stderr.write((b'no tests for {}\n').format(lib))
                return -1

        archive.finalize()
        if archive.failed_documents:
            sys.stderr.write(b'tests build failed\n')
            build.render_failed_documents(archive, console)
            write_output()
            return -1
        else:
            if args.automated:
                archive.suppress_breakpoints = True
            all_results = []
            for lib in test_libs:
                suites = list(lib.get_elements_by_type((namespaces.test, b'suite')))
                for suite_no, suite in enumerate(suites, 1):
                    try:
                        suite_description = suite.description
                    except:
                        suite_description = suite.libid

                    if args.quick and suite.slow:
                        with self.console.progress((b'{} {} (skipped slow test)').format(lib, suite_description), 0):
                            pass
                        continue
                    if args.exclude and suite.group is not None and suite.group in args.exclude:
                        with self.console.progress((b'{} {} (excluded group)').format(lib, suite_description), 0):
                            pass
                        continue
                    if args.group and suite.group not in args.group:
                        with self.console.progress((b'{} {} (not in group)').format(lib, suite_description), 0):
                            pass
                        continue
                    steps = 0
                    setup = suite.get_child((namespaces.test, b'setup'))
                    teardown = suite.get_child((namespaces.test, b'teardown'))
                    if setup is not None:
                        setup_callable = archive.get_callable_from_element(setup)
                        steps += 1
                    if teardown is not None:
                        teardown_callable = archive.get_callable_from_element(teardown)
                        steps += 1
                    tests = list(suite.children((namespaces.test, b'case')))
                    steps += len(tests)
                    test_runner = {}
                    context = Context({b'_test_runner': test_runner})
                    results = TestResults(context, lib, suite.description)
                    results.group = suite._definition
                    all_results.append(results)
                    context[b'._test_results'] = results
                    test_info = (b'({} of {})').format(suite_no, len(suites))
                    progress_text = (b'{} {} {}').format(lib, suite_description, test_info)
                    with self.console.progress(progress_text, steps) as (progress):
                        if steps == 0:
                            progress.step()
                        else:
                            try:
                                with TestRunner(context, results):
                                    if setup is not None:
                                        setup_callable(context)
                                        progress.step()
                            except Exception as e:
                                results.add_setup_error(setup, e)
                                progress.step(b'setup failed')
                            else:
                                with TestRunner(context, results):
                                    for test in tests:
                                        results.case = test
                                        test_callable = archive.get_callable_from_element(test)
                                        try:
                                            try:
                                                test_return = test_callable(context)
                                            except Exception as e:
                                                results.add_error(test, e)

                                            if test_return != b'fail':
                                                results.add_pass(test)
                                        finally:
                                            progress.step()

                                try:
                                    with TestRunner(context, results):
                                        if teardown is not None:
                                            teardown_callable(context)
                                            progress.step()
                                except Exception as e:
                                    results.add_teardown_error(teardown, e)

            all_totals = {b'pass': 0, b'fail': 0, b'error': 0}
            for result in all_results:
                _pass, fail, error = result.stats
                all_totals[b'pass'] += _pass
                all_totals[b'fail'] += fail
                all_totals[b'error'] += error

            summary = (b'{fail} fail(s), {error} error(s), {pass} pass(es)').format(**all_totals)
            if args.quick:
                console.div((b'Test results (quick) {}').format(datetime.now().ctime()))
            else:
                console.div((b'Test results {}').format(datetime.now().ctime()))
            test_count = sum(len(r.tests) for r in all_results)
            console.text((b'Ran {} test(s) in {} test suite(s) - {}').format(test_count, len(all_results), summary))
            for results in all_results:
                results.report(console, show_trace=not args.summary, show_passes=args.verbose or args.summary, verbose=args.verbose)

            header = [b'lib', b'suite', b'passes', b'fails', b'errors']
            table = []
            passes = 0
            fails = 0
            errors = 0
            for result in all_results:
                _pass, fail, error = result.stats
                passes += _pass
                fails += fail
                errors += error
                _pass = Cell(_pass, fg=b'green' if _pass else b'white', bold=True)
                fail = Cell(fail, fg=b'red' if fail else b'green', bold=True)
                error = Cell(error, fg=b'red' if error else b'green', bold=True)
                table.append([result.lib.long_name, result.suite, _pass, fail, error])

            if not args.summary or args.verbose:
                console.nl()
                console.table(table, header_row=header)
            summary = (b'{fails} fail(s), {errors} error(s), {passes} pass(es)').format(fails=fails, errors=errors, passes=passes)
            if errors or fails:
                console.text(summary, fg=b'red', bold=True)
            else:
                console.text(summary, fg=b'green', bold=True)
            write_output()
            return fails