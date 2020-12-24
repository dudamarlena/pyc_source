# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/sagemaker_model_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2496 bytes
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.contrib.operators.sagemaker_base_operator import SageMakerBaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

class SageMakerModelOperator(SageMakerBaseOperator):
    """SageMakerModelOperator"""

    @apply_defaults
    def __init__(self, config, *args, **kwargs):
        (super(SageMakerModelOperator, self).__init__)(args, config=config, **kwargs)
        self.config = config

    def expand_role(self):
        if 'ExecutionRoleArn' in self.config:
            hook = AwsHook(self.aws_conn_id)
            self.config['ExecutionRoleArn'] = hook.expand_role(self.config['ExecutionRoleArn'])

    def execute(self, context):
        self.preprocess_config()
        self.log.info('Creating SageMaker Model %s.', self.config['ModelName'])
        response = self.hook.create_model(self.config)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise AirflowException('Sagemaker model creation failed: %s' % response)
        else:
            return {'Model': self.hook.describe_model(self.config['ModelName'])}