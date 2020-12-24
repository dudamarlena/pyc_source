# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/s3_prefix_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3417 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class S3PrefixSensor(BaseSensorOperator):
    """S3PrefixSensor"""
    template_fields = ('prefix', 'bucket_name')

    @apply_defaults
    def __init__(self, bucket_name, prefix, delimiter='/', aws_conn_id='aws_default', verify=None, *args, **kwargs):
        (super(S3PrefixSensor, self).__init__)(*args, **kwargs)
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.delimiter = delimiter
        self.full_url = 's3://' + bucket_name + '/' + prefix
        self.aws_conn_id = aws_conn_id
        self.verify = verify

    def poke(self, context):
        self.log.info('Poking for prefix : %s in bucket s3://%s', self.prefix, self.bucket_name)
        from airflow.hooks.S3_hook import S3Hook
        hook = S3Hook(aws_conn_id=(self.aws_conn_id), verify=(self.verify))
        return hook.check_for_prefix(prefix=(self.prefix),
          delimiter=(self.delimiter),
          bucket_name=(self.bucket_name))