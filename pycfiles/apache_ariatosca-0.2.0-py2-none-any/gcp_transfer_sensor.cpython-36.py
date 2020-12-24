# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/gcp_transfer_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3066 bytes
import six
from airflow.contrib.hooks.gcp_transfer_hook import GCPTransferServiceHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class GCPTransferServiceWaitForJobStatusSensor(BaseSensorOperator):
    """GCPTransferServiceWaitForJobStatusSensor"""
    template_fields = ('job_name', )

    @apply_defaults
    def __init__(self, job_name, expected_statuses, project_id=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(GCPTransferServiceWaitForJobStatusSensor, self).__init__)(*args, **kwargs)
        self.job_name = job_name
        self.expected_statuses = {expected_statuses} if isinstance(expected_statuses, six.string_types) else expected_statuses
        self.project_id = project_id
        self.gcp_cloud_conn_id = gcp_conn_id

    def poke(self, context):
        hook = GCPTransferServiceHook(gcp_conn_id=(self.gcp_cloud_conn_id))
        operations = hook.list_transfer_operations(filter={'project_id':self.project_id, 
         'job_names':[self.job_name]})
        check = GCPTransferServiceHook.operations_contain_expected_statuses(operations=operations,
          expected_statuses=(self.expected_statuses))
        if check:
            self.xcom_push(key='sensed_operations', value=operations, context=context)
        return check