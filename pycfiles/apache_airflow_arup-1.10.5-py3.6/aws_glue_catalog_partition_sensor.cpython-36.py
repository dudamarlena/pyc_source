# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/aws_glue_catalog_partition_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3794 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class AwsGlueCatalogPartitionSensor(BaseSensorOperator):
    __doc__ = '\n    Waits for a partition to show up in AWS Glue Catalog.\n\n    :param table_name: The name of the table to wait for, supports the dot\n        notation (my_database.my_table)\n    :type table_name: str\n    :param expression: The partition clause to wait for. This is passed as\n        is to the AWS Glue Catalog API\'s get_partitions function,\n        and supports SQL like notation as in ``ds=\'2015-01-01\'\n        AND type=\'value\'`` and comparison operators as in ``"ds>=2015-01-01"``.\n        See https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-catalog-partitions.html\n        #aws-glue-api-catalog-partitions-GetPartitions\n    :type expression: str\n    :param aws_conn_id: ID of the Airflow connection where\n        credentials and extra configuration are stored\n    :type aws_conn_id: str\n    :param region_name: Optional aws region name (example: us-east-1). Uses region from connection\n        if not specified.\n    :type region_name: str\n    :param database_name: The name of the catalog database where the partitions reside.\n    :type database_name: str\n    :param poke_interval: Time in seconds that the job should wait in\n        between each tries\n    :type poke_interval: int\n    '
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