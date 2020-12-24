# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/s3_prefix_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3417 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class S3PrefixSensor(BaseSensorOperator):
    __doc__ = "\n    Waits for a prefix to exist. A prefix is the first part of a key,\n    thus enabling checking of constructs similar to glob airfl* or\n    SQL LIKE 'airfl%'. There is the possibility to precise a delimiter to\n    indicate the hierarchy or keys, meaning that the match will stop at that\n    delimiter. Current code accepts sane delimiters, i.e. characters that\n    are NOT special characters in the Python regex engine.\n\n    :param bucket_name: Name of the S3 bucket\n    :type bucket_name: str\n    :param prefix: The prefix being waited on. Relative path from bucket root level.\n    :type prefix: str\n    :param delimiter: The delimiter intended to show hierarchy.\n        Defaults to '/'.\n    :type delimiter: str\n    :param aws_conn_id: a reference to the s3 connection\n    :type aws_conn_id: str\n    :param verify: Whether or not to verify SSL certificates for S3 connection.\n        By default SSL certificates are verified.\n        You can provide the following values:\n\n        - ``False``: do not validate SSL certificates. SSL will still be used\n                 (unless use_ssl is False), but SSL certificates will not be\n                 verified.\n        - ``path/to/cert/bundle.pem``: A filename of the CA cert bundle to uses.\n                 You can specify this argument if you want to use a different\n                 CA cert bundle than the one used by botocore.\n    :type verify: bool or str\n    "
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