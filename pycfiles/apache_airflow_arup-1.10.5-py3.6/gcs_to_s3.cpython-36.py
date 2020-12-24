# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcs_to_s3.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6121 bytes
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.contrib.operators.gcs_list_operator import GoogleCloudStorageListOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.S3_hook import S3Hook

class GoogleCloudStorageToS3Operator(GoogleCloudStorageListOperator):
    __doc__ = "\n    Synchronizes a Google Cloud Storage bucket with an S3 bucket.\n\n    :param bucket: The Google Cloud Storage bucket to find the objects. (templated)\n    :type bucket: str\n    :param prefix: Prefix string which filters objects whose name begin with\n        this prefix. (templated)\n    :type prefix: str\n    :param delimiter: The delimiter by which you want to filter the objects. (templated)\n        For e.g to lists the CSV files from in a directory in GCS you would use\n        delimiter='.csv'.\n    :type delimiter: str\n    :param google_cloud_storage_conn_id: The connection ID to use when\n        connecting to Google Cloud Storage.\n    :type google_cloud_storage_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide delegation enabled.\n    :type delegate_to: str\n    :param dest_aws_conn_id: The destination S3 connection\n    :type dest_aws_conn_id: str\n    :param dest_s3_key: The base S3 key to be used to store the files. (templated)\n    :type dest_s3_key: str\n    :param dest_verify: Whether or not to verify SSL certificates for S3 connection.\n        By default SSL certificates are verified.\n        You can provide the following values:\n\n        - ``False``: do not validate SSL certificates. SSL will still be used\n                 (unless use_ssl is False), but SSL certificates will not be\n                 verified.\n        - ``path/to/cert/bundle.pem``: A filename of the CA cert bundle to uses.\n                 You can specify this argument if you want to use a different\n                 CA cert bundle than the one used by botocore.\n    :type dest_verify: bool or str\n    :param replace: Whether or not to verify the existence of the files in the\n        destination bucket.\n        By default is set to False\n        If set to True, will upload all the files replacing the existing ones in\n        the destination bucket.\n        If set to False, will upload only the files that are in the origin but not\n        in the destination bucket.\n    :type replace: bool\n    "
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