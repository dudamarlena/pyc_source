# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/bigquery_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2885 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.utils.decorators import apply_defaults

class BigQueryTableSensor(BaseSensorOperator):
    """BigQueryTableSensor"""
    template_fields = ('project_id', 'dataset_id', 'table_id')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, project_id, dataset_id, table_id, bigquery_conn_id='bigquery_default_conn', delegate_to=None, *args, **kwargs):
        (super(BigQueryTableSensor, self).__init__)(*args, **kwargs)
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.bigquery_conn_id = bigquery_conn_id
        self.delegate_to = delegate_to

    def poke(self, context):
        table_uri = '{0}:{1}.{2}'.format(self.project_id, self.dataset_id, self.table_id)
        self.log.info('Sensor checks existence of table: %s', table_uri)
        hook = BigQueryHook(bigquery_conn_id=(self.bigquery_conn_id),
          delegate_to=(self.delegate_to))
        return hook.table_exists(self.project_id, self.dataset_id, self.table_id)