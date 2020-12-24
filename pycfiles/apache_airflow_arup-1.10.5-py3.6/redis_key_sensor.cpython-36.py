# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/redis_key_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1538 bytes
from airflow.contrib.hooks.redis_hook import RedisHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class RedisKeySensor(BaseSensorOperator):
    __doc__ = '\n    Checks for the existence of a key in a Redis\n    '
    template_fields = ('key', )
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, key, redis_conn_id, *args, **kwargs):
        (super(RedisKeySensor, self).__init__)(*args, **kwargs)
        self.redis_conn_id = redis_conn_id
        self.key = key

    def poke(self, context):
        self.log.info('Sensor checks for existence of key: %s', self.key)
        return RedisHook(self.redis_conn_id).get_conn().exists(self.key)