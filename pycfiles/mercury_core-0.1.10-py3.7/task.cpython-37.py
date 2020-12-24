# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/common/task_managers/redis/task.py
# Compiled at: 2018-02-08 17:03:50
# Size of source mod 2**32: 1426 bytes
import logging, json, redis
from mercury.common.task_managers.base.task import Task
log = logging.getLogger(__name__)

class RedisTask(Task):

    def __init__(self, redis_host, redis_port, queue_name):
        super(RedisTask, self).__init__()
        self.queue_name = queue_name
        log.debug('Redis QUEUE name: %s' % self.queue_name)
        self.redis = redis.Redis(redis_host, redis_port)

    def fetch(self):
        """Fetch a task from the queue.

        The format of the message retrieved from the queue is:
            [queue_name, task_json]

        :returns: dict or None. A dictionary representing the task,
            or None if no task was found or its format is incorrect.
        """
        message = self.redis.blpop((self.queue_name), timeout=1)
        if not message:
            return
        message = message[1]
        if isinstance(message, bytes):
            message = message.decode()
        try:
            task = json.loads(message)
        except ValueError:
            log.error('Popped some bad data off the queue')
            log.debug('DATA: %s' % message)
            return
        else:
            log.debug(f"Fetched task {task['task_id']}")
            self.task = task
            return task

    def do(self):
        raise NotImplementedError