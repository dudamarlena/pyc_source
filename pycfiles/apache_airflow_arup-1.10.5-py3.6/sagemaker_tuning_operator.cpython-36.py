# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/sagemaker_tuning_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4191 bytes
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.contrib.operators.sagemaker_base_operator import SageMakerBaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

class SageMakerTuningOperator(SageMakerBaseOperator):
    __doc__ = "\n    Initiate a SageMaker hyperparameter tuning job.\n\n    This operator returns The ARN of the tuning job created in Amazon SageMaker.\n\n    :param config: The configuration necessary to start a tuning job (templated).\n\n        For details of the configuration parameter see\n        :py:meth:`SageMaker.Client.create_hyper_parameter_tuning_job`\n    :type config: dict\n    :param aws_conn_id: The AWS connection ID to use.\n    :type aws_conn_id: str\n    :param wait_for_completion: Set to True to wait until the tuning job finishes.\n    :type wait_for_completion: bool\n    :param check_interval: If wait is set to True, the time interval, in seconds,\n        that this operation waits to check the status of the tuning job.\n    :type check_interval: int\n    :param max_ingestion_time: If wait is set to True, the operation fails\n        if the tuning job doesn't finish within max_ingestion_time seconds. If you\n        set this parameter to None, the operation does not timeout.\n    :type max_ingestion_time: int\n    "
    integer_fields = [
     [
      'HyperParameterTuningJobConfig', 'ResourceLimits', 'MaxNumberOfTrainingJobs'],
     [
      'HyperParameterTuningJobConfig', 'ResourceLimits', 'MaxParallelTrainingJobs'],
     [
      'TrainingJobDefinition', 'ResourceConfig', 'InstanceCount'],
     [
      'TrainingJobDefinition', 'ResourceConfig', 'VolumeSizeInGB'],
     [
      'TrainingJobDefinition', 'StoppingCondition', 'MaxRuntimeInSeconds']]

    @apply_defaults
    def __init__(self, config, wait_for_completion=True, check_interval=30, max_ingestion_time=None, *args, **kwargs):
        (super(SageMakerTuningOperator, self).__init__)(args, config=config, **kwargs)
        self.config = config
        self.wait_for_completion = wait_for_completion
        self.check_interval = check_interval
        self.max_ingestion_time = max_ingestion_time

    def expand_role(self):
        if 'TrainingJobDefinition' in self.config:
            config = self.config['TrainingJobDefinition']
            if 'RoleArn' in config:
                hook = AwsHook(self.aws_conn_id)
                config['RoleArn'] = hook.expand_role(config['RoleArn'])

    def execute(self, context):
        self.preprocess_config()
        self.log.info('Creating SageMaker Hyper-Parameter Tuning Job %s', self.config['HyperParameterTuningJobName'])
        response = self.hook.create_tuning_job((self.config),
          wait_for_completion=(self.wait_for_completion),
          check_interval=(self.check_interval),
          max_ingestion_time=(self.max_ingestion_time))
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise AirflowException('Sagemaker Tuning Job creation failed: %s' % response)
        else:
            return {'Tuning': self.hook.describe_tuning_job(self.config['HyperParameterTuningJobName'])}