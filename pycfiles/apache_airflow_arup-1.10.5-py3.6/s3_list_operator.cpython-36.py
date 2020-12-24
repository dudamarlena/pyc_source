# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/s3_list_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3694 bytes
from typing import Iterable
from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class S3ListOperator(BaseOperator):
    __doc__ = "\n    List all objects from the bucket with the given string prefix in name.\n\n    This operator returns a python list with the name of objects which can be\n    used by `xcom` in the downstream task.\n\n    :param bucket: The S3 bucket where to find the objects. (templated)\n    :type bucket: str\n    :param prefix: Prefix string to filters the objects whose name begin with\n        such prefix. (templated)\n    :type prefix: str\n    :param delimiter: the delimiter marks key hierarchy. (templated)\n    :type delimiter: str\n    :param aws_conn_id: The connection ID to use when connecting to S3 storage.\n    :type aws_conn_id: str\n    :param verify: Whether or not to verify SSL certificates for S3 connection.\n        By default SSL certificates are verified.\n        You can provide the following values:\n\n        - ``False``: do not validate SSL certificates. SSL will still be used\n                 (unless use_ssl is False), but SSL certificates will not be\n                 verified.\n        - ``path/to/cert/bundle.pem``: A filename of the CA cert bundle to uses.\n                 You can specify this argument if you want to use a different\n                 CA cert bundle than the one used by botocore.\n    :type verify: bool or str\n\n\n    **Example**:\n        The following operator would list all the files\n        (excluding subfolders) from the S3\n        ``customers/2018/04/`` key in the ``data`` bucket. ::\n\n            s3_file = S3ListOperator(\n                task_id='list_3s_files',\n                bucket='data',\n                prefix='customers/2018/04/',\n                delimiter='/',\n                aws_conn_id='aws_customers_conn'\n            )\n    "
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