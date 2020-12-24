# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/cassandra_table_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2317 bytes
from airflow.contrib.hooks.cassandra_hook import CassandraHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class CassandraTableSensor(BaseSensorOperator):
    __doc__ = '\n    Checks for the existence of a table in a Cassandra cluster.\n\n    For example, if you want to wait for a table called \'t\' to be created\n    in a keyspace \'k\', instantiate it as follows:\n\n    >>> cassandra_sensor = CassandraTableSensor(table="k.t",\n    ...                                         cassandra_conn_id="cassandra_default",\n    ...                                         task_id="cassandra_sensor")\n    '
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