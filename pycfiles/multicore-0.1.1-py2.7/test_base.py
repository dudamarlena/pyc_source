# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/multicore/tests/test_base.py
# Compiled at: 2017-08-07 06:17:24
import math, time, unittest
from multicore import Task, initialize, shutdown
from multicore.utils import ranges
users = []
for i in range(100):
    users.append({'username': 'user%s' % i})

def expensive_render(user):
    time.sleep(0.01)
    return user['username']


def multi_expensive_render(start, end):
    """Do multiple expensive renders"""
    s = ''
    for user in users[start:end]:
        s += expensive_render(user)

    return s


class TaskTestCase(unittest.TestCase):

    def setUp(self):
        super(TaskTestCase, self).setUp()
        shutdown()

    def tearDown(self):
        super(TaskTestCase, self).tearDown()
        shutdown()

    def test_speed(self):
        initialize(force=True)
        t_start = time.time()
        s_sync = ''
        for user in users:
            s_sync += expensive_render(user)

        duration_sync = time.time() - t_start
        t_start = time.time()
        task = Task()
        for start, end in ranges(users):
            task.run(multi_expensive_render, start, end)

        s_async = ('').join(task.get())
        duration_async = time.time() - t_start
        self.assertEqual(s_sync, s_async)
        self.failUnless(duration_async < duration_sync)

    def test_no_deadlock(self):
        initialize(force=True)