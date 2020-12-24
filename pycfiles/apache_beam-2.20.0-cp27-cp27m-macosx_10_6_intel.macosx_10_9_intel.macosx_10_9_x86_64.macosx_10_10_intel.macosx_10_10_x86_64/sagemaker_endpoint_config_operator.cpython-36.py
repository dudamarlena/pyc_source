# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/sagemaker_endpoint_config_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2467 bytes
from airflow.contrib.operators.sagemaker_base_operator import SageMakerBaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

class SageMakerEndpointConfigOperator(SageMakerBaseOperator):
    """SageMakerEndpointConfigOperator"""
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