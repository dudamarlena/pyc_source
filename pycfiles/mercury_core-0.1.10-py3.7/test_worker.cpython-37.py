# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/common/unit/task_managers/base/test_worker.py
# Compiled at: 2018-01-08 12:01:55
# Size of source mod 2**32: 2689 bytes
import mock
from mercury.common.task_managers.base import task
from mercury.common.task_managers.base import worker
from tests.common.unit.base import MercuryCommonUnitTest

class WorkerTest(MercuryCommonUnitTest):
    __doc__ = 'Tests for the mercury.common.task_managers.base.worker'

    @mock.patch.object(task, 'Task')
    def setUp(self, mock_task):
        """Create a fake worker object"""
        mock_task.create.return_value = None
        task_handler = task.Task()
        max_requests = 1
        max_age = 3600
        self.fake_worker = worker.Worker(task_handler, max_requests, max_age, (), {})

    def test_start(self):
        """Test start() executes a new task"""
        self.fake_worker.start()
        self.fake_worker.task.fetch.assert_called_once()
        self.fake_worker.task.execute.assert_called_once()
        self.assertEqual(1, self.fake_worker.handled_tasks)

    def test_start_kill_signal(self):
        """Test start() doesn't execute task if kill_signal is True"""
        self.fake_worker.kill_signal = True
        self.fake_worker.start()
        self.fake_worker.task.fetch.assert_not_called()
        self.fake_worker.task.execute.assert_not_called()
        self.assertEqual(0, self.fake_worker.handled_tasks)

    def test_start_too_many_requests(self):
        """Test start() doesn't execute more tasks than maximum allowed"""
        self.fake_worker.handled_tasks = 1
        self.fake_worker.start()
        self.fake_worker.task.fetch.assert_not_called()
        self.fake_worker.task.execute.assert_not_called()
        self.assertEqual(1, self.fake_worker.handled_tasks)

    def test_start_no_more_task(self):
        """Test start() continue fetching tasks if none found at first"""
        self.fake_worker.task.fetch.side_effect = [
         None, 'fake_task']
        self.fake_worker.start()
        self.assertEqual(2, self.fake_worker.task.fetch.call_count)
        self.fake_worker.task.execute.assert_called_once()
        self.assertEqual(1, self.fake_worker.handled_tasks)