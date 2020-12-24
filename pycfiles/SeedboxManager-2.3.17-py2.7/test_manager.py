# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tests/process/test_manager.py
# Compiled at: 2015-06-14 13:30:57
from seedbox.process import manager
from seedbox.tests import test

class SampleTask(object):

    def __call__(self):
        return [
         True]


class ManagerTestCase(test.ConfiguredBaseTestCase):

    def test_manager(self):
        mgr = manager.TaskManager()
        _tasks = []
        _tasks.append(SampleTask())
        _tasks.append(SampleTask())
        _tasks.append(SampleTask())
        mgr.add_tasks(_tasks)
        mgr.add_tasks(SampleTask())
        self.assertEqual(len(mgr.tasks), 4)
        results = mgr.run()
        self.assertEqual(len(mgr.tasks), 0)
        self.assertEqual(len(results), 4)
        mgr.shutdown()