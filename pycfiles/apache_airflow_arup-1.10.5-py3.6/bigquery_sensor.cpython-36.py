# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/bigquery_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2885 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.utils.decorators import apply_defaults

class BigQueryTableSensor(BaseSensorOperator):
    __doc__ = '\n    Checks for the existence of a table in Google Bigquery.\n\n    :param project_id: The Google cloud project in which to look for the table.\n        The connection supplied to the hook must provide\n        access to the specified project.\n    :type project_id: str\n    :param dataset_id: The name of the dataset in which to look for the table.\n        storage bucket.\n    :type dataset_id: str\n    :param table_id: The name of the table to check the existence of.\n    :type table_id: str\n    :param bigquery_conn_id: The connection ID to use when connecting to\n        Google BigQuery.\n    :type bigquery_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must\n        have domain-wide delegation enabled.\n    :type delegate_to: str\n    '
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