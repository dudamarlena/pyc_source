# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/common/unit/task_managers/redis/test_redis_task.py
# Compiled at: 2018-01-22 15:39:21
# Size of source mod 2**32: 1912 bytes
import mock
from mercury.common.task_managers.redis import task
from tests.common.unit.base import MercuryCommonUnitTest

class RedisTaskTest(MercuryCommonUnitTest):
    __doc__ = 'Tests for the mercury.common.task_managers.redis.task'

    @mock.patch('redis.Redis')
    def setUp(self, mock_redis):
        self.redisTask = task.RedisTask(None, None, 'rpc_tasks')

    def test_fetch(self):
        """Test fetch() with JSON data in 'rpc_task' queue"""
        self.redisTask.redis.blpop.return_value = [
         'rpc_tasks',
         '{"task_id": "1", "time_updated": 10}']
        fetched_task = self.redisTask.fetch()
        self.assertEqual('1', fetched_task['task_id'])
        self.assertEqual(10, fetched_task['time_updated'])

    def test_fetch_empty_redis(self):
        """Test fetch() with an empty 'rpc_task' queue"""
        self.redisTask.redis.blpop.return_value = None
        fetched_task = self.redisTask.fetch()
        self.assertIsNone(fetched_task)

    def test_fetch_not_json(self):
        """Test fetch() with incorrect data in 'rpc_task' queue"""
        self.redisTask.redis.blpop.return_value = [
         'rpc_tasks',
         'fake_data']
        fetched_task = self.redisTask.fetch()
        self.assertIsNone(fetched_task)