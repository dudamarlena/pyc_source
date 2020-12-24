# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcs_acl_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5893 bytes
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class GoogleCloudStorageBucketCreateAclEntryOperator(BaseOperator):
    """GoogleCloudStorageBucketCreateAclEntryOperator"""
    template_fields = ('bucket', 'entity', 'role', 'user_project')

    @apply_defaults
    def __init__(self, bucket, entity, role, user_project=None, google_cloud_storage_conn_id='google_cloud_default', *args, **kwargs):
        (super(GoogleCloudStorageBucketCreateAclEntryOperator, self).__init__)(*args, **kwargs)
        self.bucket = bucket
        self.entity = entity
        self.role = role
        self.user_project = user_project
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id

    def execute(self, context):
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id))
        hook.insert_bucket_acl(bucket=(self.bucket), entity=(self.entity), role=(self.role), user_project=(self.user_project))


class GoogleCloudStorageObjectCreateAclEntryOperator(BaseOperator):
    """GoogleCloudStorageObjectCreateAclEntryOperator"""
    template_fields = ('bucket', 'object_name', 'entity', 'role', 'generation', 'user_project')

    @apply_defaults
    def __init__(self, bucket, object_name, entity, role, generation=None, user_project=None, google_cloud_storage_conn_id='google_cloud_default', *args, **kwargs):
        (super(GoogleCloudStorageObjectCreateAclEntryOperator, self).__init__)(*args, **kwargs)
        self.bucket = bucket
        self.object_name = object_name
        self.entity = entity
        self.role = role
        self.generation = generation
        self.user_project = user_project
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id

    def execute(self, context):
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id))
        hook.insert_object_acl(bucket=(self.bucket), object_name=(self.object_name), entity=(self.entity),
          role=(self.role),
          generation=(self.generation),
          user_project=(self.user_project))