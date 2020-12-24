# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/redis_key_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1538 bytes
from airflow.contrib.hooks.redis_hook import RedisHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class RedisKeySensor(BaseSensorOperator):
    """RedisKeySensor"""
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