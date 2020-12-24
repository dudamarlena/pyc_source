# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/sagemaker_training_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4033 bytes
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.contrib.operators.sagemaker_base_operator import SageMakerBaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

class SageMakerTrainingOperator(SageMakerBaseOperator):
    __doc__ = "\n    Initiate a SageMaker training job.\n\n    This operator returns The ARN of the training job created in Amazon SageMaker.\n\n    :param config: The configuration necessary to start a training job (templated).\n\n        For details of the configuration parameter see :py:meth:`SageMaker.Client.create_training_job`\n    :type config: dict\n    :param aws_conn_id: The AWS connection ID to use.\n    :type aws_conn_id: str\n    :param wait_for_completion: If wait is set to True, the time interval, in seconds,\n        that the operation waits to check the status of the training job.\n    :type wait_for_completion: bool\n    :param print_log: if the operator should print the cloudwatch log during training\n    :type print_log: bool\n    :param check_interval: if wait is set to be true, this is the time interval\n        in seconds which the operator will check the status of the training job\n    :type check_interval: int\n    :param max_ingestion_time: If wait is set to True, the operation fails if the training job\n        doesn't finish within max_ingestion_time seconds. If you set this parameter to None,\n        the operation does not timeout.\n    :type max_ingestion_time: int\n    "
    integer_fields = [
     [
      'ResourceConfig', 'InstanceCount'],
     [
      'ResourceConfig', 'VolumeSizeInGB'],
     [
      'StoppingCondition', 'MaxRuntimeInSeconds']]

    @apply_defaults
    def __init__(self, config, wait_for_completion=True, print_log=True, check_interval=30, max_ingestion_time=None, *args, **kwargs):
        (super(SageMakerTrainingOperator, self).__init__)(args, config=config, **kwargs)
        self.wait_for_completion = wait_for_completion
        self.print_log = print_log
        self.check_interval = check_interval
        self.max_ingestion_time = max_ingestion_time

    def expand_role(self):
        if 'RoleArn' in self.config:
            hook = AwsHook(self.aws_conn_id)
            self.config['RoleArn'] = hook.expand_role(self.config['RoleArn'])

    def execute(self, context):
        self.preprocess_config()
        self.log.info('Creating SageMaker Training Job %s.', self.config['TrainingJobName'])
        response = self.hook.create_training_job((self.config),
          wait_for_completion=(self.wait_for_completion),
          print_log=(self.print_log),
          check_interval=(self.check_interval),
          max_ingestion_time=(self.max_ingestion_time))
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise AirflowException('Sagemaker Training Job creation failed: %s' % response)
        else:
            return {'Training': self.hook.describe_training_job(self.config['TrainingJobName'])}