# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/s3_delete_objects_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3276 bytes
from airflow.exceptions import AirflowException
from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class S3DeleteObjectsOperator(BaseOperator):
    """S3DeleteObjectsOperator"""
    template_fields = ('keys', 'bucket')

    @apply_defaults
    def __init__(self, bucket, keys, aws_conn_id='aws_default', verify=None, *args, **kwargs):
        (super(S3DeleteObjectsOperator, self).__init__)(*args, **kwargs)
        self.bucket = bucket
        self.keys = keys
        self.aws_conn_id = aws_conn_id
        self.verify = verify

    def execute(self, context):
        s3_hook = S3Hook(aws_conn_id=(self.aws_conn_id), verify=(self.verify))
        response = s3_hook.delete_objects(bucket=(self.bucket), keys=(self.keys))
        deleted_keys = [x['Key'] for x in response.get('Deleted', [])]
        self.log.info('Deleted: %s', deleted_keys)
        if 'Errors' in response:
            errors_keys = [x['Key'] for x in response.get('Errors', [])]
            raise AirflowException('Errors when deleting: {}'.format(errors_keys))