# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/metastore_partition_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3427 bytes
from airflow.sensors.sql_sensor import SqlSensor
from airflow.utils.decorators import apply_defaults

class MetastorePartitionSensor(SqlSensor):
    """MetastorePartitionSensor"""
    template_fields = ('partition_name', 'table', 'schema')
    ui_color = '#8da7be'

    @apply_defaults
    def __init__(self, table, partition_name, schema='default', mysql_conn_id='metastore_mysql', *args, **kwargs):
        self.partition_name = partition_name
        self.table = table
        self.schema = schema
        self.first_poke = True
        self.conn_id = mysql_conn_id
        (super(SqlSensor, self).__init__)(*args, **kwargs)

    def poke(self, context):
        if self.first_poke:
            self.first_poke = False
            if '.' in self.table:
                self.schema, self.table = self.table.split('.')
            self.sql = "\n            SELECT 'X'\n            FROM PARTITIONS A0\n            LEFT OUTER JOIN TBLS B0 ON A0.TBL_ID = B0.TBL_ID\n            LEFT OUTER JOIN DBS C0 ON B0.DB_ID = C0.DB_ID\n            WHERE\n                B0.TBL_NAME = '{self.table}' AND\n                C0.NAME = '{self.schema}' AND\n                A0.PART_NAME = '{self.partition_name}';\n            ".format(self=self)
        return super(MetastorePartitionSensor, self).poke(context)