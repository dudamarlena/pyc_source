# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/hive_partition_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3069 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class HivePartitionSensor(BaseSensorOperator):
    __doc__ = '\n    Waits for a partition to show up in Hive.\n\n    Note: Because ``partition`` supports general logical operators, it\n    can be inefficient. Consider using NamedHivePartitionSensor instead if\n    you don\'t need the full flexibility of HivePartitionSensor.\n\n    :param table: The name of the table to wait for, supports the dot\n        notation (my_database.my_table)\n    :type table: str\n    :param partition: The partition clause to wait for. This is passed as\n        is to the metastore Thrift client ``get_partitions_by_filter`` method,\n        and apparently supports SQL like notation as in ``ds=\'2015-01-01\'\n        AND type=\'value\'`` and comparison operators as in ``"ds>=2015-01-01"``\n    :type partition: str\n    :param metastore_conn_id: reference to the metastore thrift service\n        connection id\n    :type metastore_conn_id: str\n    '
    template_fields = ('schema', 'table', 'partition')
    ui_color = '#C5CAE9'

    @apply_defaults
    def __init__(self, table, partition="ds='{{ ds }}'", metastore_conn_id='metastore_default', schema='default', poke_interval=180, *args, **kwargs):
        (super(HivePartitionSensor, self).__init__)(args, poke_interval=poke_interval, **kwargs)
        if not partition:
            partition = "ds='{{ ds }}'"
        self.metastore_conn_id = metastore_conn_id
        self.table = table
        self.partition = partition
        self.schema = schema

    def poke(self, context):
        if '.' in self.table:
            self.schema, self.table = self.table.split('.')
        self.log.info('Poking for table %s.%s, partition %s', self.schema, self.table, self.partition)
        if not hasattr(self, 'hook'):
            from airflow.hooks.hive_hooks import HiveMetastoreHook
            self.hook = HiveMetastoreHook(metastore_conn_id=(self.metastore_conn_id))
        return self.hook.check_for_partition(self.schema, self.table, self.partition)