# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/testrun.py
# Compiled at: 2018-12-17 11:51:20
__all__ = ('TestRun', 'Testee', 'TestResult')
import random
from collections import deque
from zope.interface import implementer
from interfaces import ITestRun
from util import AttributeBag

class Testee(AttributeBag):
    ATTRIBUTES = [
     'id',
     'name',
     'url',
     'auth',
     'options',
     'debug']


class TestResult(AttributeBag):
    ATTRIBUTES = [
     'id',
     'runId',
     'passed',
     'description',
     'expectation',
     'expected',
     'observed',
     'log',
     'started',
     'ended']


@implementer(ITestRun)
class TestRun:
    """
   A TestRun contains an ordered sequence of test case classes.
   A test runner instantiates tests from these test case classes.
   The test case classes must derive from WampCase or Case.
   """

    def __init__(self, testee, cases, randomize=False):
        assert isinstance(testee, Testee)
        self.testee = testee
        _cases = cases[:]
        if randomize:
            random.shuffle(_cases)
        _cases.reverse()
        self._len = len(_cases)
        self._cases = deque(_cases)

    def next(self):
        try:
            return self._cases.pop()
        except IndexError:
            return

        return

    def remaining(self):
        return len(self._cases)

    def __len__(self):
        return self._len