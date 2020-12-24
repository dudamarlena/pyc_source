# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/aws_lambda_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2350 bytes
from airflow.contrib.hooks.aws_hook import AwsHook

class AwsLambdaHook(AwsHook):
    """AwsLambdaHook"""

    def __init__(self, function_name, region_name=None, log_type='None', qualifier='$LATEST', invocation_type='RequestResponse', *args, **kwargs):
        self.function_name = function_name
        self.region_name = region_name
        self.log_type = log_type
        self.invocation_type = invocation_type
        self.qualifier = qualifier
        (super(AwsLambdaHook, self).__init__)(*args, **kwargs)

    def get_conn(self):
        self.conn = self.get_client_type('lambda', self.region_name)
        return self.conn

    def invoke_lambda(self, payload):
        """
        Invoke Lambda Function
        """
        awslambda_conn = self.get_conn()
        response = awslambda_conn.invoke(FunctionName=(self.function_name),
          InvocationType=(self.invocation_type),
          LogType=(self.log_type),
          Payload=payload,
          Qualifier=(self.qualifier))
        return response