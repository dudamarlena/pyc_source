# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/datastore_import_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4234 bytes
from airflow.contrib.hooks.datastore_hook import DatastoreHook
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DatastoreImportOperator(BaseOperator):
    """DatastoreImportOperator"""

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