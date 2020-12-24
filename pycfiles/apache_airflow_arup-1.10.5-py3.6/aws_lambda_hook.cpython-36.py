# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/aws_lambda_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2350 bytes
from airflow.contrib.hooks.aws_hook import AwsHook

class AwsLambdaHook(AwsHook):
    __doc__ = '\n    Interact with AWS Lambda\n\n    :param function_name: AWS Lambda Function Name\n    :type function_name: str\n    :param region_name: AWS Region Name (example: us-west-2)\n    :type region_name: str\n    :param log_type: Tail Invocation Request\n    :type log_type: str\n    :param qualifier: AWS Lambda Function Version or Alias Name\n    :type qualifier: str\n    :param invocation_type: AWS Lambda Invocation Type (RequestResponse, Event etc)\n    :type invocation_type: str\n    '

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