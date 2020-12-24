# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/s3_to_gcs_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 8370 bytes
from tempfile import NamedTemporaryFile
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook, _parse_gcs_url
from airflow.contrib.operators.s3_list_operator import S3ListOperator
from airflow.exceptions import AirflowException
from airflow.hooks.S3_hook import S3Hook
from airflow.utils.decorators import apply_defaults

class S3ToGoogleCloudStorageOperator(S3ListOperator):
    """S3ToGoogleCloudStorageOperator"""
    template_fields = ('bucket', 'prefix', 'delimiter', 'dest_gcs')
    ui_color = '#e09411'

    @apply_defaults
    def __init__(self, bucket, prefix='', delimiter='', aws_conn_id='aws_default', verify=None, dest_gcs_conn_id=None, dest_gcs=None, delegate_to=None, replace=False, *args, **kwargs):
        (super(S3ToGoogleCloudStorageOperator, self).__init__)(args, bucket=bucket, prefix=prefix, delimiter=delimiter, aws_conn_id=aws_conn_id, **kwargs)
        self.dest_gcs_conn_id = dest_gcs_conn_id
        self.dest_gcs = dest_gcs
        self.delegate_to = delegate_to
        self.replace = replace
        self.verify = verify
        if dest_gcs:
            if not self._gcs_object_is_directory(self.dest_gcs):
                self.log.info('Destination Google Cloud Storage path is not a valid "directory", define a path that ends with a slash "/" or leave it empty for the root of the bucket.')
                raise AirflowException('The destination Google Cloud Storage path must end with a slash "/" or be empty.')

    def execute(self, context):
        files = super(S3ToGoogleCloudStorageOperator, self).execute(context)
        gcs_hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.dest_gcs_conn_id),
          delegate_to=(self.delegate_to))
        bucket_name, object_prefix = self.replace or _parse_gcs_url(self.dest_gcs)
        existing_files_prefixed = gcs_hook.list(bucket_name,
          prefix=object_prefix)
        existing_files = []
        if existing_files_prefixed:
            if object_prefix in existing_files_prefixed:
                existing_files_prefixed.remove(object_prefix)
            for f in existing_files_prefixed:
                if f.startswith(object_prefix):
                    existing_files.append(f[len(object_prefix):])
                else:
                    existing_files.append(f)

        else:
            files = list(set(files) - set(existing_files))
            if len(files) > 0:
                self.log.info('%s files are going to be synced: %s.', len(files), files)
            else:
                self.log.info('There are no new files to sync. Have a nice day!')
            if files:
                hook = S3Hook(aws_conn_id=(self.aws_conn_id), verify=(self.verify))
                for file in files:
                    file_object = hook.get_key(file, self.bucket)
                    with NamedTemporaryFile(mode='wb', delete=True) as (f):
                        file_object.download_fileobj(f)
                        f.flush()
                        dest_gcs_bucket, dest_gcs_object_prefix = _parse_gcs_url(self.dest_gcs)
                        dest_gcs_object = dest_gcs_object_prefix + file
                        gcs_hook.upload(dest_gcs_bucket, dest_gcs_object, f.name)

                self.log.info('All done, uploaded %d files to Google Cloud Storage', len(files))
            else:
                self.log.info('In sync, no files needed to be uploaded to Google CloudStorage')
        return files

    @staticmethod
    def _gcs_object_is_directory(object):
        bucket, blob = _parse_gcs_url(object)
        return len(blob) == 0 or blob.endswith('/')