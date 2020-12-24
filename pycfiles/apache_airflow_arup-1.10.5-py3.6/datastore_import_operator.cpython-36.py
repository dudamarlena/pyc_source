# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/datastore_import_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4234 bytes
from airflow.contrib.hooks.datastore_hook import DatastoreHook
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DatastoreImportOperator(BaseOperator):
    __doc__ = '\n    Import entities from Cloud Storage to Google Cloud Datastore\n\n    :param bucket: container in Cloud Storage to store data\n    :type bucket: str\n    :param file: path of the backup metadata file in the specified Cloud Storage bucket.\n        It should have the extension .overall_export_metadata\n    :type file: str\n    :param namespace: optional namespace of the backup metadata file in\n        the specified Cloud Storage bucket.\n    :type namespace: str\n    :param entity_filter: description of what data from the project is included in\n        the export, refer to\n        https://cloud.google.com/datastore/docs/reference/rest/Shared.Types/EntityFilter\n    :type entity_filter: dict\n    :param labels: client-assigned labels for cloud storage\n    :type labels: dict\n    :param datastore_conn_id: the name of the connection id to use\n    :type datastore_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have domain-wide\n        delegation enabled.\n    :type delegate_to: str\n    :param polling_interval_in_seconds: number of seconds to wait before polling for\n        execution status again\n    :type polling_interval_in_seconds: int\n    :param xcom_push: push operation name to xcom for reference\n    :type xcom_push: bool\n    '

    @apply_defaults
    def __init__(self, bucket, file, namespace=None, entity_filter=None, labels=None, datastore_conn_id='google_cloud_default', delegate_to=None, polling_interval_in_seconds=10, xcom_push=False, *args, **kwargs):
        (super(DatastoreImportOperator, self).__init__)(*args, **kwargs)
        self.datastore_conn_id = datastore_conn_id
        self.delegate_to = delegate_to
        self.bucket = bucket
        self.file = file
        self.namespace = namespace
        self.entity_filter = entity_filter
        self.labels = labels
        self.polling_interval_in_seconds = polling_interval_in_seconds
        self.xcom_push = xcom_push

    def execute(self, context):
        self.log.info('Importing data from Cloud Storage bucket %s', self.bucket)
        ds_hook = DatastoreHook(self.datastore_conn_id, self.delegate_to)
        result = ds_hook.import_from_storage_bucket(bucket=(self.bucket), file=(self.file),
          namespace=(self.namespace),
          entity_filter=(self.entity_filter),
          labels=(self.labels))
        operation_name = result['name']
        result = ds_hook.poll_operation_until_done(operation_name, self.polling_interval_in_seconds)
        state = result['metadata']['common']['state']
        if state != 'SUCCESSFUL':
            raise AirflowException('Operation failed: result={}'.format(result))
        if self.xcom_push:
            return result