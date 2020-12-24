# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/redis_publish_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2191 bytes
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.redis_hook import RedisHook
from airflow.models import BaseOperator

class RedisPublishOperator(BaseOperator):
    __doc__ = '\n    Publish a message to Redis.\n\n    :param channel: redis channel to which the message is published (templated)\n    :type channel: str\n    :param message: the message to publish (templated)\n    :type message: str\n    :param redis_conn_id: redis connection to use\n    :type redis_conn_id: str\n    '
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