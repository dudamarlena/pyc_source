# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/file_to_gcs.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2933 bytes
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class FileToGoogleCloudStorageOperator(BaseOperator):
    """FileToGoogleCloudStorageOperator"""
    template_fields = ('src', 'dst', 'bucket')

    @apply_defaults
    def __init__(self, src, dst, bucket, google_cloud_storage_conn_id='google_cloud_default', mime_type='application/octet-stream', delegate_to=None, gzip=False, *args, **kwargs):
        (super(FileToGoogleCloudStorageOperator, self).__init__)(*args, **kwargs)
        self.src = src
        self.dst = dst
        self.bucket = bucket
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.mime_type = mime_type
        self.delegate_to = delegate_to
        self.gzip = gzip

    def execute(self, context):
        """
        Uploads the file to Google cloud storage
        """
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id),
          delegate_to=(self.delegate_to))
        hook.upload(bucket=(self.bucket),
          object=(self.dst),
          mime_type=(self.mime_type),
          filename=(self.src),
          gzip=(self.gzip))