# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/cassandra_record_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2616 bytes
from airflow.contrib.hooks.cassandra_hook import CassandraHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class CassandraRecordSensor(BaseSensorOperator):
    __doc__ = '\n    Checks for the existence of a record in a Cassandra cluster.\n\n    For example, if you want to wait for a record that has values \'v1\' and \'v2\' for each\n    primary keys \'p1\' and \'p2\' to be populated in keyspace \'k\' and table \'t\',\n    instantiate it as follows:\n\n    >>> cassandra_sensor = CassandraRecordSensor(table="k.t",\n    ...                                          keys={"p1": "v1", "p2": "v2"},\n    ...                                          cassandra_conn_id="cassandra_default",\n    ...                                          task_id="cassandra_sensor")\n    '
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