# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/testutil.py
# Compiled at: 2019-06-26 11:58:00
from __future__ import print_function
import os, signal, time
from twisted.internet import defer, reactor
from twisted.trial import unittest
from . import repeatable_random
repeatable_random

class SignalMixin:
    sigchldHandler = None

    def setUp(self):
        if hasattr(reactor, '_handleSigchld') and hasattr(signal, 'SIGCHLD'):
            self.sigchldHandler = signal.signal(signal.SIGCHLD, reactor._handleSigchld)

    def tearDown(self):
        if self.sigchldHandler:
            signal.signal(signal.SIGCHLD, self.sigchldHandler)


class PollMixin:

    def poll(self, check_f, pollinterval=0.01):
        d = defer.maybeDeferred(self._poll, None, check_f, pollinterval)
        return d

    def _poll(self, res, check_f, pollinterval):
        if check_f():
            return True
        else:
            d = defer.Deferred()
            d.addCallback(self._poll, check_f, pollinterval)
            reactor.callLater(pollinterval, d.callback, None)
            return d


class TestMixin(SignalMixin):

    def setUp(self, repeatable=False):
        """
        @param repeatable: install the repeatable_randomness hacks to attempt
            to without access to real randomness and real time.time from the
            code under test
        """
        self.repeatable = repeatable
        if self.repeatable:
            import repeatable_random
            repeatable_random.force_repeatability()
        if hasattr(time, 'realtime'):
            self.teststarttime = time.realtime()
        else:
            self.teststarttime = time.time()

    def tearDown(self):
        if self.repeatable:
            repeatable_random.restore_non_repeatability()
        self.clean_pending(required_to_quiesce=True)

    def clean_pending(self, dummy=None, required_to_quiesce=True):
        """
        This handy method cleans all pending tasks from the reactor.

        When writing a unit test, consider the following question:

            Is the code that you are testing required to release control once it
            has done its job, so that it is impossible for it to later come around
            (with a delayed reactor task) and do anything further?

        If so, then trial will usefully test that for you -- if the code under
        test leaves any pending tasks on the reactor then trial will fail it.

        On the other hand, some code is *not* required to release control -- some
        code is allowed to continuously maintain control by rescheduling reactor
        tasks in order to do ongoing work.  Trial will incorrectly require that
        code to clean up all its tasks from the reactor.

        Most people think that such code should be amended to have an optional
        "shutdown" operation that releases all control, but on the contrary it is
        good design for some code to *not* have a shutdown operation, but instead
        to have a "crash-only" design in which it recovers from crash on startup.

        If the code under test is of the "long-running" kind, which is *not*
        required to shutdown cleanly in order to pass tests, then you can simply
        call testutil.clean_pending() at the end of the unit test, and trial will
        be satisfied.
        """
        pending = reactor.getDelayedCalls()
        active = bool(pending)
        for p in pending:
            if p.active():
                p.cancel()
            else:
                print('WEIRDNESS! pending timed call not active!')

        if required_to_quiesce and active:
            self.fail('Reactor was still active when it was required to be quiescent.')


try:
    import win32file, win32con

    def w_make_readonly(path):
        win32file.SetFileAttributes(path, win32con.FILE_ATTRIBUTE_READONLY)


    def w_make_accessible(path):
        win32file.SetFileAttributes(path, win32con.FILE_ATTRIBUTE_NORMAL)


    make_readonly = w_make_readonly
    make_accessible = w_make_accessible
except ImportError:
    import stat

    def make_readonly(path):
        os.chmod(path, stat.S_IREAD)
        os.chmod(os.path.dirname(path), stat.S_IREAD)


    def make_accessible(path):
        os.chmod(os.path.dirname(path), stat.S_IWRITE | stat.S_IEXEC | stat.S_IREAD)
        os.chmod(path, stat.S_IWRITE | stat.S_IEXEC | stat.S_IREAD)