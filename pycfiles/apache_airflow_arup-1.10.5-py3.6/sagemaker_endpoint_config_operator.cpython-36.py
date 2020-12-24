# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/sagemaker_endpoint_config_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2467 bytes
from airflow.contrib.operators.sagemaker_base_operator import SageMakerBaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

class SageMakerEndpointConfigOperator(SageMakerBaseOperator):
    __doc__ = '\n    Create a SageMaker endpoint config.\n\n    This operator returns The ARN of the endpoint config created in Amazon SageMaker\n\n    :param config: The configuration necessary to create an endpoint config.\n\n        For details of the configuration parameter see :py:meth:`SageMaker.Client.create_endpoint_config`\n    :type config: dict\n    :param aws_conn_id: The AWS connection ID to use.\n    :type aws_conn_id: str\n    '
    integer_fields = [
     [
      'ProductionVariants', 'InitialInstanceCount']]

    @apply_defaults
    def __init__(self, config, *args, **kwargs):
        (super(SageMakerEndpointConfigOperator, self).__init__)(args, config=config, **kwargs)
        self.config = config

    def execute(self, context):
        self.preprocess_config()
        self.log.info('Creating SageMaker Endpoint Config %s.', self.config['EndpointConfigName'])
        response = self.hook.create_endpoint_config(self.config)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise AirflowException('Sagemaker endpoint config creation failed: %s' % response)
        else:
            return {'EndpointConfig': self.hook.describe_endpoint_config(self.config['EndpointConfigName'])}