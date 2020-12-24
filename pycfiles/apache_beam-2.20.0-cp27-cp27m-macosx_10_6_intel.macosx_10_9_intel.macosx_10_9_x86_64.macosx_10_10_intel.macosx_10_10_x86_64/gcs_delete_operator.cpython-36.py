# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcs_delete_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3200 bytes
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class GoogleCloudStorageDeleteOperator(BaseOperator):
    """GoogleCloudStorageDeleteOperator"""
    template_fields = ('bucket_name', 'prefix', 'objects')

    @apply_defaults
    def __init__(self, bucket_name, objects=None, prefix=None, google_cloud_storage_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        self.bucket_name = bucket_name
        self.objects = objects
        self.prefix = prefix
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.delegate_to = delegate_to
        if not objects is not None:
            if not prefix is not None:
                raise AssertionError
        (super(GoogleCloudStorageDeleteOperator, self).__init__)(*args, **kwargs)

    def execute(self, context):
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id),
          delegate_to=(self.delegate_to))
        if self.objects:
            objects = self.objects
        else:
            objects = hook.list(bucket=(self.bucket_name), prefix=(self.prefix))
        self.log.info('Deleting %s objects from %s', len(objects), self.bucket_name)
        for object_name in objects:
            hook.delete(bucket=(self.bucket_name), object=object_name)