# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/redis_publish_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2191 bytes
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.redis_hook import RedisHook
from airflow.models import BaseOperator

class RedisPublishOperator(BaseOperator):
    """RedisPublishOperator"""
    template_fields = ('channel', 'message')

    @apply_defaults
    def __init__(self, channel, message, redis_conn_id='redis_default', *args, **kwargs):
        (super(RedisPublishOperator, self).__init__)(*args, **kwargs)
        self.redis_conn_id = redis_conn_id
        self.channel = channel
        self.message = message

    def execute(self, context):
        """
        Publish the message to Redis channel

        :param context: the context object
        :type context: dict
        """
        redis_hook = RedisHook(redis_conn_id=(self.redis_conn_id))
        self.log.info('Sending messsage %s to Redis on channel %s', self.message, self.channel)
        result = redis_hook.get_conn().publish(channel=(self.channel), message=(self.message))
        self.log.info('Result of publishing %s', result)