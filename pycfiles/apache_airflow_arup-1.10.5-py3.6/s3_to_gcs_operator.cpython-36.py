# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = "\n    Synchronizes an S3 key, possibly a prefix, with a Google Cloud Storage\n    destination path.\n\n    :param bucket: The S3 bucket where to find the objects. (templated)\n    :type bucket: str\n    :param prefix: Prefix string which filters objects whose name begin with\n        such prefix. (templated)\n    :type prefix: str\n    :param delimiter: the delimiter marks key hierarchy. (templated)\n    :type delimiter: str\n    :param aws_conn_id: The source S3 connection\n    :type aws_conn_id: str\n    :param verify: Whether or not to verify SSL certificates for S3 connection.\n        By default SSL certificates are verified.\n        You can provide the following values:\n\n        - ``False``: do not validate SSL certificates. SSL will still be used\n                 (unless use_ssl is False), but SSL certificates will not be\n                 verified.\n        - ``path/to/cert/bundle.pem``: A filename of the CA cert bundle to uses.\n                 You can specify this argument if you want to use a different\n                 CA cert bundle than the one used by botocore.\n    :type verify: bool or str\n    :param dest_gcs_conn_id: The destination connection ID to use\n        when connecting to Google Cloud Storage.\n    :type dest_gcs_conn_id: str\n    :param dest_gcs: The destination Google Cloud Storage bucket and prefix\n        where you want to store the files. (templated)\n    :type dest_gcs: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide delegation enabled.\n    :type delegate_to: str\n    :param replace: Whether you want to replace existing destination files\n        or not.\n    :type replace: bool\n\n\n    **Example**:\n\n    .. code-block:: python\n\n       s3_to_gcs_op = S3ToGoogleCloudStorageOperator(\n            task_id='s3_to_gcs_example',\n            bucket='my-s3-bucket',\n            prefix='data/customers-201804',\n            dest_gcs_conn_id='google_cloud_default',\n            dest_gcs='gs://my.gcs.bucket/some/customers/',\n            replace=False,\n            dag=my-dag)\n\n    Note that ``bucket``, ``prefix``, ``delimiter`` and ``dest_gcs`` are\n    templated, so you can use variables in them if you wish.\n    "
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