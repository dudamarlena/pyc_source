# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/s3_list_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3694 bytes
from typing import Iterable
from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class S3ListOperator(BaseOperator):
    """S3ListOperator"""
    template_fields = ('bucket', 'prefix', 'delimiter')
    ui_color = '#ffd700'

    @apply_defaults
    def __init__(self, bucket, prefix='', delimiter='', aws_conn_id='aws_default', verify=None, *args, **kwargs):
        (super(S3ListOperator, self).__init__)(*args, **kwargs)
        self.bucket = bucket
        self.prefix = prefix
        self.delimiter = delimiter
        self.aws_conn_id = aws_conn_id
        self.verify = verify

    def execute(self, context):
        hook = S3Hook(aws_conn_id=(self.aws_conn_id), verify=(self.verify))
        self.log.info('Getting the list of files from bucket: %s in prefix: %s (Delimiter {%s)', self.bucket, self.prefix, self.delimiter)
        return hook.list_keys(bucket_name=(self.bucket),
          prefix=(self.prefix),
          delimiter=(self.delimiter))