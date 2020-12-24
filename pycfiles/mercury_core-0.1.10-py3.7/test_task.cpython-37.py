# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/common/unit/task_managers/base/test_task.py
# Compiled at: 2018-01-08 12:01:55
# Size of source mod 2**32: 1395 bytes
import mock
from mercury.common.task_managers.base import task
from tests.common.unit.base import MercuryCommonUnitTest

class TaskTest(MercuryCommonUnitTest):
    __doc__ = 'Tests for the mercury.common.task_managers.base.task'

    def setUp(self):
        """Create a fake Task object"""
        self.task = task.Task()

    @mock.patch.object(task.Task, 'do')
    def test_execute(self, mock_do):
        """Test execute() calls do() and reset the task to None"""
        self.task.task = 'fake_task'
        self.task.execute()
        mock_do.assert_called_once()
        self.assertIsNone(self.task.task)

    def test_execute_no_task(self):
        """Test execute() fails when no task is defined"""
        self.assertRaises(Exception, self.task.execute)