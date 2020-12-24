# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/s3_key_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3799 bytes
from urllib.parse import urlparse
from airflow.exceptions import AirflowException
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class S3KeySensor(BaseSensorOperator):
    __doc__ = '\n    Waits for a key (a file-like instance on S3) to be present in a S3 bucket.\n    S3 being a key/value it does not support folders. The path is just a key\n    a resource.\n\n    :param bucket_key: The key being waited on. Supports full s3:// style url\n        or relative path from root level.\n    :type bucket_key: str\n    :param bucket_name: Name of the S3 bucket\n    :type bucket_name: str\n    :param wildcard_match: whether the bucket_key should be interpreted as a\n        Unix wildcard pattern\n    :type wildcard_match: bool\n    :param aws_conn_id: a reference to the s3 connection\n    :type aws_conn_id: str\n    :param verify: Whether or not to verify SSL certificates for S3 connection.\n        By default SSL certificates are verified.\n        You can provide the following values:\n\n        - ``False``: do not validate SSL certificates. SSL will still be used\n                 (unless use_ssl is False), but SSL certificates will not be\n                 verified.\n        - ``path/to/cert/bundle.pem``: A filename of the CA cert bundle to uses.\n                 You can specify this argument if you want to use a different\n                 CA cert bundle than the one used by botocore.\n    :type verify: bool or str\n    '
    template_fields = ('bucket_key', 'bucket_name')

    @apply_defaults
    def __init__(self, bucket_key, bucket_name=None, wildcard_match=False, aws_conn_id='aws_default', verify=None, *args, **kwargs):
        (super(S3KeySensor, self).__init__)(*args, **kwargs)
        if bucket_name is None:
            parsed_url = urlparse(bucket_key)
            if parsed_url.netloc == '':
                raise AirflowException('Please provide a bucket_name')
            else:
                bucket_name = parsed_url.netloc
                if parsed_url.path[0] == '/':
                    bucket_key = parsed_url.path[1:]
                else:
                    bucket_key = parsed_url.path
        self.bucket_name = bucket_name
        self.bucket_key = bucket_key
        self.wildcard_match = wildcard_match
        self.aws_conn_id = aws_conn_id
        self.verify = verify

    def poke(self, context):
        from airflow.hooks.S3_hook import S3Hook
        hook = S3Hook(aws_conn_id=(self.aws_conn_id), verify=(self.verify))
        self.log.info('Poking for key : s3://%s/%s', self.bucket_name, self.bucket_key)
        if self.wildcard_match:
            return hook.check_for_wildcard_key(self.bucket_key, self.bucket_name)
        else:
            return hook.check_for_key(self.bucket_key, self.bucket_name)