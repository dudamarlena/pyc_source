# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/s3_to_sftp_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3180 bytes
from airflow.models import BaseOperator
from airflow.hooks.S3_hook import S3Hook
from airflow.contrib.hooks.ssh_hook import SSHHook
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse
from airflow.utils.decorators import apply_defaults

class S3ToSFTPOperator(BaseOperator):
    """S3ToSFTPOperator"""
    template_fields = ('s3_key', 'sftp_path')

    @apply_defaults
    def __init__(self, s3_bucket, s3_key, sftp_path, sftp_conn_id='ssh_default', s3_conn_id='aws_default', *args, **kwargs):
        (super(S3ToSFTPOperator, self).__init__)(*args, **kwargs)
        self.sftp_conn_id = sftp_conn_id
        self.sftp_path = sftp_path
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.s3_conn_id = s3_conn_id

    @staticmethod
    def get_s3_key(s3_key):
        """This parses the correct format for S3 keys
            regardless of how the S3 url is passed."""
        parsed_s3_key = urlparse(s3_key)
        return parsed_s3_key.path.lstrip('/')

    def execute(self, context):
        self.s3_key = self.get_s3_key(self.s3_key)
        ssh_hook = SSHHook(ssh_conn_id=(self.sftp_conn_id))
        s3_hook = S3Hook(self.s3_conn_id)
        s3_client = s3_hook.get_conn()
        sftp_client = ssh_hook.get_conn().open_sftp()
        with NamedTemporaryFile('w') as (f):
            s3_client.download_file(self.s3_bucket, self.s3_key, f.name)
            sftp_client.put(f.name, self.sftp_path)