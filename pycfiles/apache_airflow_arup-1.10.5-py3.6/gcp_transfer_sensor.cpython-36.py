# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/gcp_transfer_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3066 bytes
import six
from airflow.contrib.hooks.gcp_transfer_hook import GCPTransferServiceHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class GCPTransferServiceWaitForJobStatusSensor(BaseSensorOperator):
    __doc__ = '\n    Waits for at least one operation belonging to the job to have the\n    expected status.\n\n    :param job_name: The name of the transfer job\n    :type job_name: str\n    :param expected_statuses: The expected state of the operation.\n        See:\n        https://cloud.google.com/storage-transfer/docs/reference/rest/v1/transferOperations#Status\n    :type expected_statuses: set[str] or string\n    :param project_id: (Optional) the ID of the project that owns the Transfer\n        Job. If set to None or missing, the default project_id from the GCP\n        connection is used.\n    :type project_id: str\n    :param gcp_conn_id: The connection ID used to connect to Google Cloud\n        Platform.\n    :type gcp_conn_id: str\n    '
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