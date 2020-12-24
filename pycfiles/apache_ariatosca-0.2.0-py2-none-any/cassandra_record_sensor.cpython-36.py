# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/cassandra_record_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2616 bytes
from airflow.contrib.hooks.cassandra_hook import CassandraHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class CassandraRecordSensor(BaseSensorOperator):
    """CassandraRecordSensor"""
    template_fields = ('table', 'keys')

    @apply_defaults
    def __init__(self, table, keys, cassandra_conn_id, *args, **kwargs):
        (super(CassandraRecordSensor, self).__init__)(*args, **kwargs)
        self.cassandra_conn_id = cassandra_conn_id
        self.table = table
        self.keys = keys

    def poke(self, context):
        self.log.info('Sensor check existence of record: %s', self.keys)
        hook = CassandraHook(self.cassandra_conn_id)
        return hook.record_exists(self.table, self.keys)