# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcs_download_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3896 bytes
import sys
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.models.xcom import MAX_XCOM_SIZE
from airflow.utils.decorators import apply_defaults

class GoogleCloudStorageDownloadOperator(BaseOperator):
    """GoogleCloudStorageDownloadOperator"""
    template_fields = ('bucket', 'object', 'filename', 'store_to_xcom_key')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, bucket, object, filename=None, store_to_xcom_key=None, google_cloud_storage_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        (super(GoogleCloudStorageDownloadOperator, self).__init__)(*args, **kwargs)
        self.bucket = bucket
        self.object = object
        self.filename = filename
        self.store_to_xcom_key = store_to_xcom_key
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.delegate_to = delegate_to

    def execute(self, context):
        self.log.info('Executing download: %s, %s, %s', self.bucket, self.object, self.filename)
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id),
          delegate_to=(self.delegate_to))
        file_bytes = hook.download(bucket=(self.bucket), object=(self.object),
          filename=(self.filename))
        if self.store_to_xcom_key:
            if sys.getsizeof(file_bytes) < MAX_XCOM_SIZE:
                context['ti'].xcom_push(key=(self.store_to_xcom_key), value=file_bytes)
            else:
                raise RuntimeError('The size of the downloaded file is too large to push to XCom!')