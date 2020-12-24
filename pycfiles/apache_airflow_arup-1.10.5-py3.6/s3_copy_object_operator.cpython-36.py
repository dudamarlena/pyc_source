# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/s3_copy_object_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3990 bytes
from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class S3CopyObjectOperator(BaseOperator):
    __doc__ = "\n    Creates a copy of an object that is already stored in S3.\n\n    Note: the S3 connection used here needs to have access to both\n    source and destination bucket/key.\n\n    :param source_bucket_key: The key of the source object. (templated)\n\n        It can be either full s3:// style url or relative path from root level.\n\n        When it's specified as a full s3:// url, please omit source_bucket_name.\n    :type source_bucket_key: str\n    :param dest_bucket_key: The key of the object to copy to. (templated)\n\n        The convention to specify `dest_bucket_key` is the same as `source_bucket_key`.\n    :type dest_bucket_key: str\n    :param source_bucket_name: Name of the S3 bucket where the source object is in. (templated)\n\n        It should be omitted when `source_bucket_key` is provided as a full s3:// url.\n    :type source_bucket_name: str\n    :param dest_bucket_name: Name of the S3 bucket to where the object is copied. (templated)\n\n        It should be omitted when `dest_bucket_key` is provided as a full s3:// url.\n    :type dest_bucket_name: str\n    :param source_version_id: Version ID of the source object (OPTIONAL)\n    :type source_version_id: str\n    :param aws_conn_id: Connection id of the S3 connection to use\n    :type aws_conn_id: str\n    :param verify: Whether or not to verify SSL certificates for S3 connection.\n        By default SSL certificates are verified.\n\n        You can provide the following values:\n\n        - False: do not validate SSL certificates. SSL will still be used,\n                 but SSL certificates will not be\n                 verified.\n        - path/to/cert/bundle.pem: A filename of the CA cert bundle to uses.\n                 You can specify this argument if you want to use a different\n                 CA cert bundle than the one used by botocore.\n    :type verify: bool or str\n    "
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