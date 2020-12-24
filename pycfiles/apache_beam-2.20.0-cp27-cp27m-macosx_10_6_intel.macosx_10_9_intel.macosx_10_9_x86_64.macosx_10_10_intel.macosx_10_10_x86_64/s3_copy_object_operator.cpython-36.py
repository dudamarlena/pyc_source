# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/s3_copy_object_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3990 bytes
from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class S3CopyObjectOperator(BaseOperator):
    """S3CopyObjectOperator"""
    template_fields = ('source_bucket_key', 'dest_bucket_key', 'source_bucket_name',
                       'dest_bucket_name')

    @apply_defaults
    def __init__(self, source_bucket_key, dest_bucket_key, source_bucket_name=None, dest_bucket_name=None, source_version_id=None, aws_conn_id='aws_default', verify=None, *args, **kwargs):
        (super(S3CopyObjectOperator, self).__init__)(*args, **kwargs)
        self.source_bucket_key = source_bucket_key
        self.dest_bucket_key = dest_bucket_key
        self.source_bucket_name = source_bucket_name
        self.dest_bucket_name = dest_bucket_name
        self.source_version_id = source_version_id
        self.aws_conn_id = aws_conn_id
        self.verify = verify

    def execute(self, context):
        s3_hook = S3Hook(aws_conn_id=(self.aws_conn_id), verify=(self.verify))
        s3_hook.copy_object(self.source_bucket_key, self.dest_bucket_key, self.source_bucket_name, self.dest_bucket_name, self.source_version_id)