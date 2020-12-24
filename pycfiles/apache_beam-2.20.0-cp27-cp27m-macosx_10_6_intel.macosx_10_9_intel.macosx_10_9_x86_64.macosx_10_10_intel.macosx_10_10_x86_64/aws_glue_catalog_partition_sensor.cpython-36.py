# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/aws_glue_catalog_partition_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3794 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class AwsGlueCatalogPartitionSensor(BaseSensorOperator):
    """AwsGlueCatalogPartitionSensor"""
    template_fields = ('database_name', 'table_name', 'expression')
    ui_color = '#C5CAE9'

    @apply_defaults
    def __init__(self, table_name, expression="ds='{{ ds }}'", aws_conn_id='aws_default', region_name=None, database_name='default', poke_interval=180, *args, **kwargs):
        (super(AwsGlueCatalogPartitionSensor, self).__init__)(args, poke_interval=poke_interval, **kwargs)
        self.aws_conn_id = aws_conn_id
        self.region_name = region_name
        self.table_name = table_name
        self.expression = expression
        self.database_name = database_name

    def poke(self, context):
        """
        Checks for existence of the partition in the AWS Glue Catalog table
        """
        if '.' in self.table_name:
            self.database_name, self.table_name = self.table_name.split('.')
        self.log.info('Poking for table %s. %s, expression %s', self.database_name, self.table_name, self.expression)
        return self.get_hook().check_for_partition(self.database_name, self.table_name, self.expression)

    def get_hook(self):
        """
        Gets the AwsGlueCatalogHook
        """
        if not hasattr(self, 'hook'):
            from airflow.contrib.hooks.aws_glue_catalog_hook import AwsGlueCatalogHook
            self.hook = AwsGlueCatalogHook(aws_conn_id=(self.aws_conn_id),
              region_name=(self.region_name))
        return self.hook