# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\test\support.py
# Compiled at: 2017-12-11 20:12:50
from time import clock
import sys, unittest, functools, contextlib, cStringIO, stackless, stacklesslib.errors
from stacklesslib.util import timeout
from stacklesslib import app, main
TIMEOUT = 10

def timesafe(t=1.0):
    """Decorate a unittest with this to make it error after 't' seconds"""

    def helper(func):

        @functools.wraps(func)
        def testmethod(self):
            try:
                with timeout(t):
                    func(self)
            except stacklesslib.errors.TimeoutError:
                self.fail('test case timed out')

        return testmethod

    return helper


@contextlib.contextmanager
def captured_stderr():
    old = sys.stderr
    sys.stderr = cStringIO.StringIO()
    try:
        yield sys.stderr
    finally:
        sys.stderr = old


class StacklessTestSuite(unittest.TestSuite):

    def run(self, results):
        err = []

        def tasklet_run():
            try:
                unittest.TestSuite.run(self, results)
            except:
                err.append(sys.exc_info())

        app.install_stackless()
        tasklet = stackless.tasklet(tasklet_run)()
        deadline = clock() + TIMEOUT
        while tasklet.alive:
            main.mainloop.loop()
            if clock() > deadline:
                raise stacklesslib.errors.TimeoutError('unittest took too long.  Deadlock?')

        if err:
            try:
                raise err[0][0], err[0][1], err[0][2]
            finally:
                err = None

        return


def load_tests(loader, tests, pattern):
    suite = StacklessTestSuite()
    suite.addTests(tests)
    return suite