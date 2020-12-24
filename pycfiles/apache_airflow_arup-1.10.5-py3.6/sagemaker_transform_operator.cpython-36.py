# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/sagemaker_transform_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5020 bytes
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.contrib.operators.sagemaker_base_operator import SageMakerBaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

class SageMakerTransformOperator(SageMakerBaseOperator):
    __doc__ = "\n    Initiate a SageMaker transform job.\n\n    This operator returns The ARN of the model created in Amazon SageMaker.\n\n    :param config: The configuration necessary to start a transform job (templated).\n\n        If you need to create a SageMaker transform job based on an existed SageMaker model::\n\n            config = transform_config\n\n        If you need to create both SageMaker model and SageMaker Transform job::\n\n            config = {\n                'Model': model_config,\n                'Transform': transform_config\n            }\n\n        For details of the configuration parameter of transform_config see\n        :py:meth:`SageMaker.Client.create_transform_job`\n\n        For details of the configuration parameter of model_config, See:\n        :py:meth:`SageMaker.Client.create_model`\n\n    :type config: dict\n    :param aws_conn_id: The AWS connection ID to use.\n    :type aws_conn_id: string\n    :param wait_for_completion: Set to True to wait until the transform job finishes.\n    :type wait_for_completion: bool\n    :param check_interval: If wait is set to True, the time interval, in seconds,\n        that this operation waits to check the status of the transform job.\n    :type check_interval: int\n    :param max_ingestion_time: If wait is set to True, the operation fails\n        if the transform job doesn't finish within max_ingestion_time seconds. If you\n        set this parameter to None, the operation does not timeout.\n    :type max_ingestion_time: int\n    "

    @apply_defaults
    def __init__(self, config, wait_for_completion=True, check_interval=30, max_ingestion_time=None, *args, **kwargs):
        (super(SageMakerTransformOperator, self).__init__)(args, config=config, **kwargs)
        self.config = config
        self.wait_for_completion = wait_for_completion
        self.check_interval = check_interval
        self.max_ingestion_time = max_ingestion_time
        self.create_integer_fields()

    def create_integer_fields(self):
        self.integer_fields = [
         [
          'Transform', 'TransformResources', 'InstanceCount'],
         [
          'Transform', 'MaxConcurrentTransforms'],
         [
          'Transform', 'MaxPayloadInMB']]
        if 'Transform' not in self.config:
            for field in self.integer_fields:
                field.pop(0)

    def expand_role(self):
        if 'Model' not in self.config:
            return
        config = self.config['Model']
        if 'ExecutionRoleArn' in config:
            hook = AwsHook(self.aws_conn_id)
            config['ExecutionRoleArn'] = hook.expand_role(config['ExecutionRoleArn'])

    def execute(self, context):
        self.preprocess_config()
        model_config = self.config.get('Model')
        transform_config = self.config.get('Transform', self.config)
        if model_config:
            self.log.info('Creating SageMaker Model %s for transform job', model_config['ModelName'])
            self.hook.create_model(model_config)
        else:
            self.log.info('Creating SageMaker transform Job %s.', transform_config['TransformJobName'])
            response = self.hook.create_transform_job(transform_config,
              wait_for_completion=(self.wait_for_completion),
              check_interval=(self.check_interval),
              max_ingestion_time=(self.max_ingestion_time))
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise AirflowException('Sagemaker transform Job creation failed: %s' % response)
            else:
                return {'Model':self.hook.describe_model(transform_config['ModelName']),  'Transform':self.hook.describe_transform_job(transform_config['TransformJobName'])}