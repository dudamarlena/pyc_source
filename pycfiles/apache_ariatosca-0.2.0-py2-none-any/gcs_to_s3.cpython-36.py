# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcs_to_s3.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6121 bytes
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.contrib.operators.gcs_list_operator import GoogleCloudStorageListOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.S3_hook import S3Hook

class GoogleCloudStorageToS3Operator(GoogleCloudStorageListOperator):
    """GoogleCloudStorageToS3Operator"""
    template_fields = ('bucket', 'prefix', 'delimiter', 'dest_s3_key')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, bucket, prefix=None, delimiter=None, google_cloud_storage_conn_id='google_cloud_storage_default', delegate_to=None, dest_aws_conn_id=None, dest_s3_key=None, dest_verify=None, replace=False, *args, **kwargs):
        (super(GoogleCloudStorageToS3Operator, self).__init__)(args, bucket=bucket, prefix=prefix, delimiter=delimiter, google_cloud_storage_conn_id=google_cloud_storage_conn_id, delegate_to=delegate_to, **kwargs)
        self.dest_aws_conn_id = dest_aws_conn_id
        self.dest_s3_key = dest_s3_key
        self.dest_verify = dest_verify
        self.replace = replace

    def execute(self, context):
        files = super(GoogleCloudStorageToS3Operator, self).execute(context)
        s3_hook = S3Hook(aws_conn_id=(self.dest_aws_conn_id), verify=(self.dest_verify))
        if not self.replace:
            bucket_name, prefix = S3Hook.parse_s3_url(self.dest_s3_key)
            existing_files = s3_hook.list_keys(bucket_name, prefix=prefix)
            existing_files = existing_files if existing_files is not None else []
            existing_files = [file.replace(prefix, '', 1) for file in existing_files]
            files = list(set(files) - set(existing_files))
        else:
            if files:
                hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id),
                  delegate_to=(self.delegate_to))
                for file in files:
                    file_bytes = hook.download(self.bucket, file)
                    dest_key = self.dest_s3_key + file
                    self.log.info('Saving file to %s', dest_key)
                    s3_hook.load_bytes(file_bytes, key=dest_key,
                      replace=(self.replace))

                self.log.info('All done, uploaded %d files to S3', len(files))
            else:
                self.log.info('In sync, no files needed to be uploaded to S3')
        return files