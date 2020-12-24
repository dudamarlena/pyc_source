# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcs_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5151 bytes
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.version import version

class GoogleCloudStorageCreateBucketOperator(BaseOperator):
    """GoogleCloudStorageCreateBucketOperator"""
    template_fields = ('bucket_name', 'storage_class', 'location', 'project_id')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, bucket_name, resource=None, storage_class='MULTI_REGIONAL', location='US', project_id=None, labels=None, google_cloud_storage_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        (super(GoogleCloudStorageCreateBucketOperator, self).__init__)(*args, **kwargs)
        self.bucket_name = bucket_name
        self.resource = resource
        self.storage_class = storage_class
        self.location = location
        self.project_id = project_id
        self.labels = labels
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.delegate_to = delegate_to

    def execute(self, context):
        if self.labels is not None:
            self.labels.update({'airflow-version': 'v' + version.replace('.', '-').replace('+', '-')})
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id),
          delegate_to=(self.delegate_to))
        hook.create_bucket(bucket_name=(self.bucket_name), resource=(self.resource),
          storage_class=(self.storage_class),
          location=(self.location),
          project_id=(self.project_id),
          labels=(self.labels))