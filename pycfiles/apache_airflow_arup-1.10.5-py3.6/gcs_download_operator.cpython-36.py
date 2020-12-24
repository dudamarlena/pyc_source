# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcs_download_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3896 bytes
import sys
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.models.xcom import MAX_XCOM_SIZE
from airflow.utils.decorators import apply_defaults

class GoogleCloudStorageDownloadOperator(BaseOperator):
    __doc__ = '\n    Downloads a file from Google Cloud Storage.\n\n    :param bucket: The Google cloud storage bucket where the object is. (templated)\n    :type bucket: str\n    :param object: The name of the object to download in the Google cloud\n        storage bucket. (templated)\n    :type object: str\n    :param filename: The file path on the local file system (where the\n        operator is being executed) that the file should be downloaded to. (templated)\n        If no filename passed, the downloaded data will not be stored on the local file\n        system.\n    :type filename: str\n    :param store_to_xcom_key: If this param is set, the operator will push\n        the contents of the downloaded file to XCom with the key set in this\n        parameter. If not set, the downloaded data will not be pushed to XCom. (templated)\n    :type store_to_xcom_key: str\n    :param google_cloud_storage_conn_id: The connection ID to use when\n        connecting to Google cloud storage.\n    :type google_cloud_storage_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide delegation enabled.\n    :type delegate_to: str\n    '
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