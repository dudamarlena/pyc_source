# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = "\n    Synchronizes an Azure Data Lake Storage path with a GCS bucket\n\n    :param src_adls: The Azure Data Lake path to find the objects (templated)\n    :type src_adls: str\n    :param dest_gcs: The Google Cloud Storage bucket and prefix to\n        store the objects. (templated)\n    :type dest_gcs: str\n    :param replace: If true, replaces same-named files in GCS\n    :type replace: bool\n    :param azure_data_lake_conn_id: The connection ID to use when\n        connecting to Azure Data Lake Storage.\n    :type azure_data_lake_conn_id: str\n    :param google_cloud_storage_conn_id: The connection ID to use when\n        connecting to Google Cloud Storage.\n    :type google_cloud_storage_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide delegation enabled.\n    :type delegate_to: str\n\n    **Examples**:\n        The following Operator would copy a single file named\n        ``hello/world.avro`` from ADLS to the GCS bucket ``mybucket``. Its full\n        resulting gcs path will be ``gs://mybucket/hello/world.avro`` ::\n\n            copy_single_file = AdlsToGoogleCloudStorageOperator(\n                task_id='copy_single_file',\n                src_adls='hello/world.avro',\n                dest_gcs='gs://mybucket',\n                replace=False,\n                azure_data_lake_conn_id='azure_data_lake_default',\n                google_cloud_storage_conn_id='google_cloud_default'\n            )\n\n        The following Operator would copy all parquet files from ADLS\n        to the GCS bucket ``mybucket``. ::\n\n            copy_all_files = AdlsToGoogleCloudStorageOperator(\n                task_id='copy_all_files',\n                src_adls='*.parquet',\n                dest_gcs='gs://mybucket',\n                replace=False,\n                azure_data_lake_conn_id='azure_data_lake_default',\n                google_cloud_storage_conn_id='google_cloud_default'\n            )\n\n         The following Operator would copy all parquet files from ADLS\n         path ``/hello/world``to the GCS bucket ``mybucket``. ::\n\n            copy_world_files = AdlsToGoogleCloudStorageOperator(\n                task_id='copy_world_files',\n                src_adls='hello/world/*.parquet',\n                dest_gcs='gs://mybucket',\n                replace=False,\n                azure_data_lake_conn_id='azure_data_lake_default',\n                google_cloud_storage_conn_id='google_cloud_default'\n            )\n    "
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