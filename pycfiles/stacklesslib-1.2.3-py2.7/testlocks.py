# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\test\testlocks.py
# Compiled at: 2017-12-11 20:12:50
import unittest, test.test_support
from .. import locks, app
from . import lock_tests

class LockTests(lock_tests.LockTests):
    locktype = staticmethod(locks.Lock)


class RLockTests(lock_tests.RLockTests):
    locktype = staticmethod(locks.RLock)


class EventTests(lock_tests.EventTests):
    eventtype = staticmethod(locks.Event)


class ConditionAsRLockTests(lock_tests.RLockTests):
    locktype = staticmethod(locks.Condition)


class ConditionTests(lock_tests.ConditionTests):
    locktype = staticmethod(locks.Lock)
    condtype = staticmethod(locks.Condition)


class NLConditionTests(lock_tests.NLConditionTests):
    locktype = staticmethod(locks.Lock)
    condtype = staticmethod(locks.NLCondition)


class SemaphoreTests(lock_tests.SemaphoreTests):
    semtype = staticmethod(locks.Semaphore)


class BoundedSemaphoreTests(lock_tests.BoundedSemaphoreTests):
    semtype = staticmethod(locks.BoundedSemaphore)


from .support import load_tests
if __name__ == '__main__':
    app.install_stackless()
    unittest.main()