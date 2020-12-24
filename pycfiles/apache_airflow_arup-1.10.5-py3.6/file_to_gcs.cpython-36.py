# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/file_to_gcs.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2933 bytes
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class FileToGoogleCloudStorageOperator(BaseOperator):
    __doc__ = '\n    Uploads a file to Google Cloud Storage.\n    Optionally can compress the file for upload.\n\n    :param src: Path to the local file. (templated)\n    :type src: str\n    :param dst: Destination path within the specified bucket. (templated)\n    :type dst: str\n    :param bucket: The bucket to upload to. (templated)\n    :type bucket: str\n    :param google_cloud_storage_conn_id: The Airflow connection ID to upload with\n    :type google_cloud_storage_conn_id: str\n    :param mime_type: The mime-type string\n    :type mime_type: str\n    :param delegate_to: The account to impersonate, if any\n    :type delegate_to: str\n    :param gzip: Allows for file to be compressed and uploaded as gzip\n    :type gzip: bool\n    '
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