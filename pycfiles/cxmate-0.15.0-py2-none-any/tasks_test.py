# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/tests/tasks_test.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = 'Calxeda: task_test.py'
import unittest, time
from cxmanage_api.tasks import TaskQueue

class TaskTest(unittest.TestCase):
    """Test for the TaskQueue Class."""

    def test_task_queue(self):
        """ Test the task queue """
        task_queue = TaskQueue()
        counters = [ Counter() for _ in xrange(128) ]
        tasks = [ task_queue.put(counters[i].add, i) for i in xrange(128) ]
        for task in tasks:
            task.join()

        for i in xrange(128):
            self.assertEqual(counters[i].value, i)

    def test_sequential_delay(self):
        """ Test that a single thread delays between tasks """
        task_queue = TaskQueue(threads=1, delay=0.25)
        counters = [ Counter() for x in xrange(8) ]
        start = time.time()
        tasks = [ task_queue.put(x.add, 1) for x in counters ]
        for task in tasks:
            task.join()

        finish = time.time()
        self.assertGreaterEqual(finish - start, 2.0)


class Counter(object):
    """ Simple counter object for testing purposes """

    def __init__(self):
        self.value = 0

    def add(self, value):
        """ Increment this counter's value by some amount """
        self.value += value