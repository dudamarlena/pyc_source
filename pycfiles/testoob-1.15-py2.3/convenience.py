# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/running/convenience.py
# Compiled at: 2009-10-07 18:08:46
"""convenience functions for running tests"""
from __future__ import generators
import time
from testoob.extracting import suite_iter as _suite_iter
from testoob.extracting import full_extractor as _full_extractor

def apply_decorators(callable, decorators):
    """Wrap the callable in all the decorators"""
    result = callable
    for decorator in decorators:
        result = decorator(result)

    return result


class TestLoop(object):
    """Runs the suites"""
    __module__ = __name__

    def __init__(self, suites, runner, interval=None, stop_on_fail=False, extraction_decorators=None, fixture_decorators=None):
        from fixture_decorators import BaseFixture
        self.suites = suites
        self.runner = runner
        self.interval = interval
        self.stop_on_fail = stop_on_fail
        self.extraction_decorators = extraction_decorators or []
        self.fixture_decorators = fixture_decorators or [BaseFixture]
        self.runner.reporter.setParameters(num_tests=self.num_tests)

    def _all_fixtures(self):
        for suite in _suite_iter(self.suites):
            for fixture in self.test_extractor(suite):
                yield fixture

    all_fixtures = property(_all_fixtures)

    def _num_tests(self):
        result = 0
        for suite in _suite_iter(self.suites):
            result += len(list(self.test_extractor(suite)))

        return result

    num_tests = property(_num_tests)
    test_extractor = property(lambda self: apply_decorators(_full_extractor, self.extraction_decorators))

    def _run_fixture(self, fixture):
        decorated_fixture = apply_decorators(fixture, self.fixture_decorators)
        if hasattr(self, 'not_first') and self.interval is not None:
            time.sleep(self.interval)
        self.not_first = True
        self.last_result = self.runner.run(decorated_fixture)
        return

    def _handle_interrupt(self, fixture):
        from fixture_decorators import get_interrupterd_fixture
        if hasattr(self, 'last_interrupt') and time.time() - self.last_interrupt < 1:
            self.fixture_decorators = [
             get_interrupterd_fixture()]
        self.last_interrupt = time.time()
        decorated_fixture = apply_decorators(fixture, [get_interrupterd_fixture(True)])
        self.runner.run(decorated_fixture)

    def _run_all_fixtures(self):
        for fixture in self.all_fixtures:
            try:
                self._run_fixture(fixture)
                if self.stop_on_fail and not self.last_result:
                    return
            except KeyboardInterrupt, e:
                self._handle_interrupt(fixture)

    def run(self):
        self.runner.reporter.start()
        self._run_all_fixtures()
        self.runner.done()
        return self.runner.isSuccessful()


def run(suite=None, suites=None, **kwargs):
    """Convenience frontend for text_run_suites"""
    if suite is None and suites is None:
        raise TypeError('either suite or suites must be specified')
    if suite is not None and suites is not None:
        raise TypeError('only one of suite or suites may be specified')
    if suites is None:
        suites = [
         suite]
    return run_suites(suites, **kwargs)
    return


def _apply_debug(reporter, runDebug):
    if runDebug is None:
        return reporter

    def replace(reporter, flavor, methodname):
        original = getattr(reporter, methodname)

        def replacement(test, err):
            runDebug(test, err, flavor, reporter, original)

        setattr(reporter, methodname, replacement)

    replace(reporter, 'error', 'addError')
    replace(reporter, 'failure', 'addFailure')
    return reporter
    return


def _create_reporter_proxy(reporters, runDebug, threads):
    from testoob.reporting import ReporterProxy
    result = ReporterProxy(threads)
    for reporter in reporters:
        result.add_observer(_apply_debug(reporter, runDebug))

    return result


def run_suites(suites, reporters, runner=None, runDebug=None, threads=None, **kwargs):
    """Run the test suites"""
    if runner is None:
        from simplerunner import SimpleRunner
        runner = SimpleRunner()
    runner.reporter = _create_reporter_proxy(reporters, runDebug, threads=threads)
    return TestLoop(suites=suites, runner=runner, **kwargs).run()
    return


def text_run(*args, **kwargs):
    """
    Run suites with a TextStreamReporter.
    """
    from testoob.utils import _pop
    kwargs.setdefault('reporters', [])
    import sys
    from testoob.reporting import TextStreamReporter
    reporter_class = _pop(kwargs, 'reporter_class', TextStreamReporter)
    from testoob.reporting.options import silent
    if not silent:
        kwargs['reporters'].append(reporter_class(stream=sys.stderr))
    if len(kwargs['reporters']) == 0:
        from testoob.reporting.base import BaseReporter
        kwargs['reporters'].append(BaseReporter())
    from testoob.reporting.options import coverage
    for reporter in kwargs['reporters']:
        reporter.setCoverageInfo(*coverage)

    return run(*args, **kwargs)