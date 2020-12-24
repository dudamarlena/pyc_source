# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/turtl/engine.py
# Compiled at: 2011-08-16 14:59:21
from twisted.internet import defer, task

class _ConcurrencyPrimitive(object):
    """
    This code was taken from Twisted project with some minor changes.
    Twisted is available at http://twistedmatrix.com/trac/
    """
    _execute = defer.maybeDeferred

    def __init__(self):
        self.waiting = []

    def _releaseAndReturn(self, r):
        self.release()
        return r

    def run(*args, **kwargs):
        """Acquire, run, release.

        This function takes a callable as its first argument and any
        number of other positional and keyword arguments.  When the
        lock or semaphore is acquired, the callable will be invoked
        with those arguments.

        The callable may return a Deferred; if it does, the lock or
        semaphore won't be released until that Deferred fires.

        @return: Deferred of function result.
        """
        if len(args) < 2:
            if not args:
                raise TypeError('run() takes at least 2 arguments, none given.')
            raise TypeError('%s.run() takes at least 2 arguments, 1 given' % (
             args[0].__class__.__name__,))
        self, f = args[:2]
        args = args[2:]

        def execute(ignoredResult):
            d = self._execute(f, *args, **kwargs)
            d.addBoth(self._releaseAndReturn)
            return d

        d = self.acquire(kwargs.pop('_hpriority', False))
        d.addCallback(execute)
        return d

    def runasap(*args, **kwargs):
        """Acquire, run, release and put in the front of the waiting queue

        @return: Deferred of function result.
        """
        kwargs['_hpriority'] = True
        return _ConcurrencyPrimitive.run(*args, **kwargs)


class ThrottlingDeferred(_ConcurrencyPrimitive):

    def __init__(self, concurrency, calls, interval):
        """Throttling deferred that considers both the concurrency
        requirements and the frequency, over time, of calls that
        you are allowed to make. It's clear however that if the
        rate of calls is higher than the tokens there will be
        a queue, and the queue can grow indefinitely if calls don't
        return quickly enough. More specifically: if T(f) is the
        time it takes to execute a call, and this time is formed
        by Ts(f) and Tp(f) [serial time and parallelizable time]:

            Ts(f)*calls + Tp(f)*(calls/tokens) <= interval

        If this is not true then the ingress could be too high
        and causing an ever-increasing queue.

        @param concurrency: The maximum number of concurrent
                            calls.
        @type concurrency: C{int}

        @param calls: Represents the number of calls that
                can be made every C{interval}
        @type calls: C{int}

        @param interval: Represents the time between a
                C{calls} number of calls

        NOTE: Currently it's not a requirement but if distributed
                usage of this deferred was a necessity, the points
                and current concurrency levels should be stored
                somewhere else and updated every time they are
                checked (there would also be race conditions and
                so on).
        """
        _ConcurrencyPrimitive.__init__(self)
        self._sem = defer.DeferredSemaphore(concurrency)
        self._execute = self._sem.run
        self.calls = calls
        self.interval = interval
        self.points = calls
        self.stopping = False
        self._resetLoop = task.LoopingCall(self._reset)
        self._resetLoop.start(interval, now=False)
        self._lastReset = None
        return

    def _reset(self):
        self.points = self.calls
        if self._lastReset is None or self._lastReset.called:
            self._lastReset = self._sem.run(self.release)
        return

    def acquire(self, priority=False):
        """Attempt to acquire the token.

        @param priority: Defines an high priority call that should
                            either be executed immediately or scheduled
                            as the immediate next one.
        @type priority: C{bool}

        @return: a Deferred which fires on token acquisition.
        """
        if not self.points >= 0:
            raise AssertionError, 'Internal inconsistency??  points should never be negative'
            d = defer.Deferred()
            if self.points or priority:
                self.waiting.insert(0, d)
            else:
                self.waiting.append(d)
        else:
            self.points = self.points - 1
            d.callback(self)
        return d

    def release(self):
        """Release the token.

        Should be called by whoever did the acquire() when the shared
        resource is free.
        """
        if not self.stopping and self.points > 0 and self.waiting:
            self.points = self.points - 1
            d = self.waiting.pop(0)
            d.callback(self)

    def stop(self):
        """Stop the reset calls and cleanup all the unfired deferreds.
        """
        self.stopping = True
        if self._resetLoop.running:
            self._resetLoop.stop()
        for d in self.waiting:
            d.errback(defer.CancelledError('ThrottlingDeferred.stop was called'))