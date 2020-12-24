# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/redis_pub_sub_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2727 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.redis_hook import RedisHook

class RedisPubSubSensor(BaseSensorOperator):
    __doc__ = '\n    Redis sensor for reading a message from pub sub channels\n    '
    template_fields = ('channels', )
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, channels, redis_conn_id, *args, **kwargs):
        (super(RedisPubSubSensor, self).__init__)(*args, **kwargs)
        self.channels = channels
        self.redis_conn_id = redis_conn_id
        self.pubsub = RedisHook(redis_conn_id=(self.redis_conn_id)).get_conn().pubsub()
        self.pubsub.subscribe(self.channels)

    def poke(self, context):
        """
        Check for message on subscribed channels and write to xcom the message with key ``message``

        An example of message ``{'type': 'message', 'pattern': None, 'channel': b'test', 'data': b'hello'}``

        :param context: the context object
        :type context: dict
        :return: ``True`` if message (with type 'message') is available or ``False`` if not
        """
        self.log.info('RedisPubSubSensor checking for message on channels: %s', self.channels)
        message = self.pubsub.get_message()
        self.log.info('Message %s from channel %s', message, self.channels)
        if message and message['type'] == 'message':
            context['ti'].xcom_push(key='message', value=message)
            self.pubsub.unsubscribe(self.channels)
            return True
        else:
            return False