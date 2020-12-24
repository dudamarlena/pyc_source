# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\simulation\test_tasks.py
# Compiled at: 2016-04-27 14:54:00
# Size of source mod 2**32: 3997 bytes
from unittest import TestCase
from mock import MagicMock, PropertyMock
from mad.simulation.tasks import Task, LIFOTaskPool, FIFOTaskPool
DEFAULT_PRIORITY = 0

class AbstractTaskPoolTests:

    @staticmethod
    def _make_task(priority=DEFAULT_PRIORITY):
        task = MagicMock(Task)
        type(task).priority = PropertyMock(return_value=priority)
        task.request = MagicMock()
        return task

    def _put_a_task(self, priority=DEFAULT_PRIORITY):
        task = self._make_task(priority)
        self.pool.put(task)
        return task

    def _activate_a_task(self, priority=DEFAULT_PRIORITY):
        task = self._make_task(priority)
        self.pool.pause(task)
        self.pool.activate(task)
        return task

    def _pause_a_task(self):
        task = self._make_task()
        self.pool.pause(task)
        return task

    def test_take_fails_when_empty(self):
        self.assertTrue(self.pool.is_empty)
        with self.assertRaises(ValueError):
            self.pool.take()

    def test_put_increases_size(self):
        self._put_a_task()
        self.assertEqual(self.pool.size, 1)

    def test_take_decreases_size(self):
        self._put_a_task()
        self._put_a_task()
        self.pool.take()
        self.assertEqual(self.pool.size, 1)

    def test_activate_increases_size(self):
        self._activate_a_task()
        self.assertEqual(self.pool.size, 1)
        self.assertEqual(0, len(self.pool.paused))

    def test_pause_increases_blocked_count(self):
        self._pause_a_task()
        self.assertEqual(self.pool.size, 0)
        self.assertEqual(self.pool.blocked_count, 1)

    def test_take_return_a_task_with_highest_priority(self):
        self._put_a_task(priority=1)
        next_task = self._put_a_task(priority=2)
        self._put_a_task(priority=1)
        self.assertIs(next_task, self.pool.take())

    def test_take_returns_paused_tasks_first_regardless_of_priority(self):
        self._put_a_task(priority=5)
        self._put_a_task(priority=5)
        next_task = self._activate_a_task(priority=1)
        self._put_a_task(priority=5)
        self.assertIs(next_task, self.pool.take())

    def test_take_returns_paused_tasks_by_priority(self):
        self._activate_a_task(priority=3)
        next_task = self._activate_a_task(priority=4)
        self._activate_a_task(priority=1)
        self.assertIs(next_task, self.pool.take())

    def test_breaking_tie(self):
        raise NotImplementedError('_AbstractTaskPoolTests::test_breaking_tie')


class LIFOTaskPoolTests(TestCase, AbstractTaskPoolTests):

    def setUp(self):
        self.pool = LIFOTaskPool()

    def test_breaking_tie(self):
        self._put_a_task()
        self._put_a_task()
        next_task = self._put_a_task()
        self.assertIs(next_task, self.pool.take())


class FIFOTaskPoolTests(TestCase, AbstractTaskPoolTests):

    def setUp(self):
        self.pool = FIFOTaskPool()

    def test_breaking_tie(self):
        next_task = self._put_a_task()
        self._put_a_task()
        self._put_a_task()
        self.assertIs(next_task, self.pool.take())


if __name__ == '__main__':
    import unittest.main
    unittest.main()