# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/adls_to_gcs.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6146 bytes
import os
from tempfile import NamedTemporaryFile
from airflow.contrib.hooks.azure_data_lake_hook import AzureDataLakeHook
from airflow.contrib.operators.adls_list_operator import AzureDataLakeStorageListOperator
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook, _parse_gcs_url
from airflow.utils.decorators import apply_defaults

class AdlsToGoogleCloudStorageOperator(AzureDataLakeStorageListOperator):
    """AdlsToGoogleCloudStorageOperator"""
    template_fields = ('src_adls', 'dest_gcs')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, src_adls, dest_gcs, azure_data_lake_conn_id, google_cloud_storage_conn_id, delegate_to=None, replace=False, *args, **kwargs):
        (super(AdlsToGoogleCloudStorageOperator, self).__init__)(args, path=src_adls, azure_data_lake_conn_id=azure_data_lake_conn_id, **kwargs)
        self.src_adls = src_adls
        self.dest_gcs = dest_gcs
        self.replace = replace
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.delegate_to = delegate_to

    def execute(self, context):
        files = super(AdlsToGoogleCloudStorageOperator, self).execute(context)
        g_hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id),
          delegate_to=(self.delegate_to))
        if not self.replace:
            bucket_name, prefix = _parse_gcs_url(self.dest_gcs)
            existing_files = g_hook.list(bucket=bucket_name, prefix=prefix)
            files = set(files) - set(existing_files)
        else:
            if files:
                hook = AzureDataLakeHook(azure_data_lake_conn_id=(self.azure_data_lake_conn_id))
                for obj in files:
                    with NamedTemporaryFile(mode='wb', delete=True) as (f):
                        hook.download_file(local_path=(f.name), remote_path=obj)
                        f.flush()
                        dest_gcs_bucket, dest_gcs_prefix = _parse_gcs_url(self.dest_gcs)
                        dest_path = os.path.join(dest_gcs_prefix, obj)
                        self.log.info('Saving file to %s', dest_path)
                        g_hook.upload(bucket=dest_gcs_bucket, object=dest_path, filename=(f.name))

                self.log.info('All done, uploaded %d files to GCS', len(files))
            else:
                self.log.info('In sync, no files needed to be uploaded to GCS')
        return files