# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/datastore_export_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4918 bytes
from airflow.contrib.hooks.datastore_hook import DatastoreHook
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DatastoreExportOperator(BaseOperator):
    __doc__ = '\n    Export entities from Google Cloud Datastore to Cloud Storage\n\n    :param bucket: name of the cloud storage bucket to backup data\n    :type bucket: str\n    :param namespace: optional namespace path in the specified Cloud Storage bucket\n        to backup data. If this namespace does not exist in GCS, it will be created.\n    :type namespace: str\n    :param datastore_conn_id: the name of the Datastore connection id to use\n    :type datastore_conn_id: str\n    :param cloud_storage_conn_id: the name of the cloud storage connection id to\n        force-write backup\n    :type cloud_storage_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have domain-wide\n        delegation enabled.\n    :type delegate_to: str\n    :param entity_filter: description of what data from the project is included in the\n        export, refer to\n        https://cloud.google.com/datastore/docs/reference/rest/Shared.Types/EntityFilter\n    :type entity_filter: dict\n    :param labels: client-assigned labels for cloud storage\n    :type labels: dict\n    :param polling_interval_in_seconds: number of seconds to wait before polling for\n        execution status again\n    :type polling_interval_in_seconds: int\n    :param overwrite_existing: if the storage bucket + namespace is not empty, it will be\n        emptied prior to exports. This enables overwriting existing backups.\n    :type overwrite_existing: bool\n    :param xcom_push: push operation name to xcom for reference\n    :type xcom_push: bool\n    '

    @apply_defaults
    def __init__(self, bucket, namespace=None, datastore_conn_id='google_cloud_default', cloud_storage_conn_id='google_cloud_default', delegate_to=None, entity_filter=None, labels=None, polling_interval_in_seconds=10, overwrite_existing=False, xcom_push=False, *args, **kwargs):
        (super(DatastoreExportOperator, self).__init__)(*args, **kwargs)
        self.datastore_conn_id = datastore_conn_id
        self.cloud_storage_conn_id = cloud_storage_conn_id
        self.delegate_to = delegate_to
        self.bucket = bucket
        self.namespace = namespace
        self.entity_filter = entity_filter
        self.labels = labels
        self.polling_interval_in_seconds = polling_interval_in_seconds
        self.overwrite_existing = overwrite_existing
        self.xcom_push = xcom_push

    def execute(self, context):
        self.log.info('Exporting data to Cloud Storage bucket ' + self.bucket)
        if self.overwrite_existing:
            if self.namespace:
                gcs_hook = GoogleCloudStorageHook(self.cloud_storage_conn_id)
                objects = gcs_hook.list((self.bucket), prefix=(self.namespace))
                for o in objects:
                    gcs_hook.delete(self.bucket, o)

        ds_hook = DatastoreHook(self.datastore_conn_id, self.delegate_to)
        result = ds_hook.export_to_storage_bucket(bucket=(self.bucket), namespace=(self.namespace),
          entity_filter=(self.entity_filter),
          labels=(self.labels))
        operation_name = result['name']
        result = ds_hook.poll_operation_until_done(operation_name, self.polling_interval_in_seconds)
        state = result['metadata']['common']['state']
        if state != 'SUCCESSFUL':
            raise AirflowException('Operation failed: result={}'.format(result))
        if self.xcom_push:
            return result