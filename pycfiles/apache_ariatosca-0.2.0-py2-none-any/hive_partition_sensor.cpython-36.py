# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/hive_partition_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3069 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class HivePartitionSensor(BaseSensorOperator):
    """HivePartitionSensor"""
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