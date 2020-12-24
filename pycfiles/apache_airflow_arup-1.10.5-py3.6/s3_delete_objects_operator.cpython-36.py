# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/s3_delete_objects_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3276 bytes
from airflow.exceptions import AirflowException
from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class S3DeleteObjectsOperator(BaseOperator):
    __doc__ = "\n    To enable users to delete single object or multiple objects from\n    a bucket using a single HTTP request.\n\n    Users may specify up to 1000 keys to delete.\n\n    :param bucket: Name of the bucket in which you are going to delete object(s). (templated)\n    :type bucket: str\n    :param keys: The key(s) to delete from S3 bucket. (templated)\n\n        When ``keys`` is a string, it's supposed to be the key name of\n        the single object to delete.\n\n        When ``keys`` is a list, it's supposed to be the list of the\n        keys to delete.\n\n        You may specify up to 1000 keys.\n    :type keys: str or list\n    :param aws_conn_id: Connection id of the S3 connection to use\n    :type aws_conn_id: str\n    :param verify: Whether or not to verify SSL certificates for S3 connection.\n        By default SSL certificates are verified.\n\n        You can provide the following values:\n\n        - ``False``: do not validate SSL certificates. SSL will still be used,\n                 but SSL certificates will not be\n                 verified.\n        - ``path/to/cert/bundle.pem``: A filename of the CA cert bundle to uses.\n                 You can specify this argument if you want to use a different\n                 CA cert bundle than the one used by botocore.\n    :type verify: bool or str\n    "
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