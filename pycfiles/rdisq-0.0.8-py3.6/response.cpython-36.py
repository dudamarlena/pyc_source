# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rdisq/response.py
# Compiled at: 2020-03-07 02:12:19
# Size of source mod 2**32: 1971 bytes
__author__ = 'smackware'
import time

class RdisqResponseTimeout(Exception):
    task_id = None

    def __init__(self, task_id):
        self.task_id = task_id


class RdisqResponse(object):
    _task_id = None
    rdisq_consumer = None
    response_payload = None
    total_time_seconds = None
    called_at_unixtime = None
    timeout = None
    exception = None
    returned_value = None

    def __init__(self, task_id, rdisq_consumer):
        self._task_id = task_id
        self.rdisq_consumer = rdisq_consumer
        self.called_at_unixtime = time.time()

    def get_service_timeout(self):
        return self.rdisq_consumer.service_class.response_timeout

    def is_processed(self):
        if self.response_payload is not None:
            return True
        else:
            redis_con = self.rdisq_consumer.service_class.redis_dispatcher.get_redis()
            return redis_con.llen(self._task_id) > 0

    def is_exception(self):
        return self.response_payload.raised_exception is not None

    @property
    def process_time_seconds(self):
        return self.response_payload.processing_time_seconds

    @property
    def exception(self):
        return self.response_payload.raised_exception

    def wait(self):
        timeout = self.get_service_timeout()
        redis_con = self.rdisq_consumer.service_class.redis_dispatcher.get_redis()
        redis_response = redis_con.brpop((self._task_id), timeout=timeout)
        if redis_response is None:
            raise RdisqResponseTimeout(self._task_id)
        queue_name, response = redis_response
        self.total_time_seconds = time.time() - self.called_at_unixtime
        response_payload = self.rdisq_consumer.service_class.serializer.loads(response)
        redis_con.delete(self._task_id)
        self.response_payload = response_payload
        if self.is_exception():
            raise self.exception
        return self.response_payload.returned_value