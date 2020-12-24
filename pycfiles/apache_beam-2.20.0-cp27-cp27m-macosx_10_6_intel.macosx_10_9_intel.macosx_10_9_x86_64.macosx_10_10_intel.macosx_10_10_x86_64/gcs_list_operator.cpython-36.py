# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcs_list_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3703 bytes
from typing import Iterable
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class GoogleCloudStorageListOperator(BaseOperator):
    """GoogleCloudStorageListOperator"""
    template_fields = ('bucket', 'prefix', 'delimiter')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, bucket, prefix=None, delimiter=None, google_cloud_storage_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        (super(GoogleCloudStorageListOperator, self).__init__)(*args, **kwargs)
        self.bucket = bucket
        self.prefix = prefix
        self.delimiter = delimiter
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.delegate_to = delegate_to

    def execute(self, context):
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id),
          delegate_to=(self.delegate_to))
        self.log.info('Getting list of the files. Bucket: %s; Delimiter: %s; Prefix: %s', self.bucket, self.delimiter, self.prefix)
        return hook.list(bucket=(self.bucket), prefix=(self.prefix),
          delimiter=(self.delimiter))