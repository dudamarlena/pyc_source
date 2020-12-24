# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/running/fixture_decorators.py
# Compiled at: 2009-10-07 18:08:46
"""Decorators for standard fixtures"""

class BaseFixture:
    __module__ = __name__

    def __init__(self, fixture):
        self.fixture = fixture

    def __call__(self, *args):
        self.fixture(*args)

    def get_fixture(self):
        result = self.fixture
        while hasattr(result, 'get_fixture'):
            result = result.get_fixture()

        return result


class ManipulativeFixture(BaseFixture):
    """
    A fixture that allows changing the original test method itself.
    """
    __module__ = __name__

    def __init__(self, fixture):
        BaseFixture.__init__(self, fixture)
        self.coreFixture = self.get_fixture()
        self.testMethodName = self.coreFixture.id().split('.')[(-1)]
        self.testMethod = getattr(self.coreFixture, self.testMethodName)
        self.testSetUp = self.coreFixture.setUp
        self.testTearDown = self.coreFixture.tearDown

    def updateMethod(self, newMethod):
        setattr(self.coreFixture, self.testMethodName, newMethod)


def get_alarmed_fixture(timeout):

    class AlarmedFixture(BaseFixture):
        """
        A fixture that times out, implemented with SIGALRM.

        Needs signals to work, so doesn't work on Windows.

        Won't work properly some other code, like the test itself, sends
        SIGALRM or changes the signal handler.
        """
        __module__ = __name__

        def __init__(self, fixture):
            BaseFixture.__init__(self, fixture)
            from signal import alarm
            self.alarm = alarm

        def __call__(self, *args):
            self.alarm(timeout)
            BaseFixture.__call__(self, *args)
            self.alarm(0)

    return AlarmedFixture


import thread, threading

class TimeoutMain:
    """
    Will raise a KeyboardInterrupt exception in the main thread on
    timeout.
    If cancelled, the timing-out thread may persist for a bit.
    """
    __module__ = __name__

    def __init__(self, timeout):
        self.timeout = timeout
        self.timed_out = False
        self.cancelled = threading.Event()

    def start(self):
        thread.start_new_thread(self._timeout_method, ())
        return self

    def cancel(self):
        self.cancelled.set()

    def verify_timeout(self):
        """
        Should be called when the main thread receives a KeyboardInterrupt
        While waiting for a timeout. If no timeout occurred, re-raises
        KeyboardInterrupt.
        """
        if not self.timed_out:
            raise KeyboardInterrupt

    def _timeout_method(self):
        self.cancelled.wait(self.timeout)
        if self.cancelled.isSet():
            return
        self.timed_out = True
        thread.interrupt_main()


def get_thread_timingout_fixture(timeout):
    assert timeout is not None
    timeout_main = TimeoutMain(timeout)

    class TimingOutFixture(ManipulativeFixture):
        """
        A fixture that times out, implemented with threads.

        Also works on Windows.

        Known problem: thread.interrupt_main() raises an exception in the main
        thread only when the main thread has control, doesn't raise it while
        its blocking.
        """
        __module__ = __name__

        def __init__(self, fixture):
            ManipulativeFixture.__init__(self, fixture)

            def testWithTimeout():
                timeout_main.start()
                try:
                    self.testMethod()
                    timeout_main.cancel()
                except KeyboardInterrupt:
                    timeout_main.verify_timeout()
                    raise AssertionError('Timeout after %s seconds' % timeout)

            self.updateMethod(testWithTimeout)

    return TimingOutFixture
    return


def _fix_sourcefile_extension(filename):
    if filename[-4:].lower() in ['.pyc', '.pyo']:
        return filename[:-4] + '.py'
    return filename


def _fix_sourcefile(filename):
    from os.path import normcase, abspath
    return abspath(normcase(_fix_sourcefile_extension(filename)))


def _module_sourcefile(module_name):
    return _fix_sourcefile(__import__(module_name).__file__)


def get_coverage_fixture(coverage):
    from os.path import abspath

    class CoveredFixture(BaseFixture):
        __module__ = __name__

        def __init__(self, fixture):
            BaseFixture.__init__(self, fixture)
            coverage.ignorepaths.append(_module_sourcefile(fixture.__module__))

        def __call__(self, *args):
            coverage.runfunc(BaseFixture.__call__, self, *args)

    return CoveredFixture


def get_timed_fixture(time_limit):

    class TimedFixture(ManipulativeFixture):
        """Run the fixture repeatedly for a minimum time"""
        __module__ = __name__

        def __init__(self, fixture):
            ManipulativeFixture.__init__(self, fixture)

            def timedTest():
                from time import time
                start = time()
                self.testMethod()
                while time() - start < time_limit:
                    self.testTearDown()
                    self.testSetUp()
                    self.testMethod()

            self.updateMethod(timedTest)

    return TimedFixture


def get_interrupterd_fixture(isRegistered=False):

    class InterruptedFixture(ManipulativeFixture):
        __module__ = __name__

        def __call__(self, reporter, *args):
            from testoob import SkipTestException
            exception = SkipTestException('Test was interrupted')
            reporter.addSkip(self.get_fixture(), (SkipTestException, exception, None), isRegistered)
            return

    return InterruptedFixture


def get_capture_fixture():

    class CaptureFixture(ManipulativeFixture):
        """Capture a test's output and error"""
        __module__ = __name__

        def __init__(self, fixture):
            ManipulativeFixture.__init__(self, fixture)

            def CaptureTest():
                import sys, os
                stdout_fh = sys.stdout
                stderr_fh = sys.stderr
                (read_fd, write_fd) = os.pipe()
                writer = os.fdopen(write_fd, 'w')
                reader = os.fdopen(read_fd, 'r')
                sys.stdout = sys.stderr = writer
                try:
                    self.testMethod()
                finally:
                    writer.close()
                    self.coreFixture._testOOB_output_txt = reader.read()
                    reader.close()
                    sys.stdout = stdout_fh
                    sys.stderr = stderr_fh

            self.updateMethod(CaptureTest)

    return CaptureFixture