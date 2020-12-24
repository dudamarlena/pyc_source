# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/turtl/test/test_engine.py
# Compiled at: 2009-08-21 14:13:15
from twisted.internet import defer
from twisted.trial import unittest
from turtl import engine

class TestEngine(unittest.TestCase):

    def _incr(self, result, by=1):
        self.counter += by

    def setUp(self):
        self.counter = 0

    def testThrottler(self):
        N = 13
        thr = engine.ThrottlingDeferred(3 * N, N, 200)
        self.assert_(thr._resetLoop.running)
        thr._resetLoop.stop()
        self.assert_(not thr._resetLoop.running)
        controlDeferred = defer.Deferred()

        def helper(self, arg):
            self.arg = arg
            return controlDeferred

        results = []
        uniqueObject = object()
        resultDeferred = thr.run(helper, self=self, arg=uniqueObject)
        resultDeferred.addCallback(results.append)
        resultDeferred.addCallback(self._incr)
        self.assertEquals(results, [])
        self.assertEquals(self.arg, uniqueObject)
        controlDeferred.callback(None)
        self.assertEquals(results.pop(), None)
        self.assertEquals(self.counter, 1)
        thr._reset()
        self.counter = 0
        for i in range(1, 1 + N):
            thr.acquire().addCallback(self._incr)
            self.assertEquals(self.counter, i)

        thr.acquire().addCallback(self._incr)
        self.assertEquals(self.counter, N)
        self.assertEquals(thr.points, 0)
        for i in range(1, N):
            thr.acquire().addCallback(self._incr)
            self.assertEquals(self.counter, N)

        thr.acquire(True).addCallback(self._incr, 10)
        for i in thr.waiting:
            self.assertEquals(thr.points, 0)
            thr.release()

        self.assertEquals(self.counter, N)
        self.assertEquals(thr.points, 0)
        thr._reset()
        self.assertEquals(self.counter, N + 10)
        self.assertEquals(thr.points, 12)
        for i in range(len(thr.waiting)):
            thr.release()

        self.assertEquals(thr.points, 0)
        self.assertEquals(self.counter, N * 2 + 9)
        thr._reset()
        self.assertEquals(self.counter, 2 * N + 10)
        self.assertEquals(thr.points, N - 1)
        return