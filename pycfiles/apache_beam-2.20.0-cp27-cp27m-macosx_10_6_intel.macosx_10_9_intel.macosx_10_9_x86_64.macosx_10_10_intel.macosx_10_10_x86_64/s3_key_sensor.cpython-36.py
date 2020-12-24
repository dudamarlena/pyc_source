# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/s3_key_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3799 bytes
from urllib.parse import urlparse
from airflow.exceptions import AirflowException
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class S3KeySensor(BaseSensorOperator):
    """S3KeySensor"""
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