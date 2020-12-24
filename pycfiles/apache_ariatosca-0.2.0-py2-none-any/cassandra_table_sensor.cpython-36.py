# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/cassandra_table_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2317 bytes
from airflow.contrib.hooks.cassandra_hook import CassandraHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class CassandraTableSensor(BaseSensorOperator):
    """CassandraTableSensor"""
    template_fields = ('table', )

    @apply_defaults
    def __init__(self, table, cassandra_conn_id, *args, **kwargs):
        (super(CassandraTableSensor, self).__init__)(*args, **kwargs)
        self.cassandra_conn_id = cassandra_conn_id
        self.table = table

    def poke(self, context):
        self.log.info('Sensor check existence of table: %s', self.table)
        hook = CassandraHook(self.cassandra_conn_id)
        return hook.table_exists(self.table)