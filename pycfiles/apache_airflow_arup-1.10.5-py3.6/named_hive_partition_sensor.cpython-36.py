# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/named_hive_partition_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3894 bytes
from past.builtins import basestring
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class NamedHivePartitionSensor(BaseSensorOperator):
    __doc__ = '\n    Waits for a set of partitions to show up in Hive.\n\n    :param partition_names: List of fully qualified names of the\n        partitions to wait for. A fully qualified name is of the\n        form ``schema.table/pk1=pv1/pk2=pv2``, for example,\n        default.users/ds=2016-01-01. This is passed as is to the metastore\n        Thrift client ``get_partitions_by_name`` method. Note that\n        you cannot use logical or comparison operators as in\n        HivePartitionSensor.\n    :type partition_names: list[str]\n    :param metastore_conn_id: reference to the metastore thrift service\n        connection id\n    :type metastore_conn_id: str\n    '
    template_fields = ('partition_names', )
    ui_color = '#8d99ae'

    @apply_defaults
    def __init__(self, partition_names, metastore_conn_id='metastore_default', poke_interval=180, hook=None, *args, **kwargs):
        (super(NamedHivePartitionSensor, self).__init__)(args, poke_interval=poke_interval, **kwargs)
        if isinstance(partition_names, basestring):
            raise TypeError('partition_names must be an array of strings')
        self.metastore_conn_id = metastore_conn_id
        self.partition_names = partition_names
        self.hook = hook
        if self.hook:
            if metastore_conn_id != 'metastore_default':
                self.log.warning('A hook was passed but a non defaul metastore_conn_id=%s was used', metastore_conn_id)

    @staticmethod
    def parse_partition_name(partition):
        first_split = partition.split('.', 1)
        if len(first_split) == 1:
            schema = 'default'
            table_partition = max(first_split)
        else:
            schema, table_partition = first_split
        second_split = table_partition.split('/', 1)
        if len(second_split) == 1:
            raise ValueError('Could not parse ' + partition + 'into table, partition')
        else:
            table, partition = second_split
        return (
         schema, table, partition)

    def poke_partition(self, partition):
        if not self.hook:
            from airflow.hooks.hive_hooks import HiveMetastoreHook
            self.hook = HiveMetastoreHook(metastore_conn_id=(self.metastore_conn_id))
        schema, table, partition = self.parse_partition_name(partition)
        self.log.info('Poking for %s.%s/%s', schema, table, partition)
        return self.hook.check_for_named_partition(schema, table, partition)

    def poke(self, context):
        self.partition_names = [partition_name for partition_name in self.partition_names if not self.poke_partition(partition_name)]
        return not self.partition_names