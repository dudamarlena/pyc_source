# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/sagemaker_tuning_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4191 bytes
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.contrib.operators.sagemaker_base_operator import SageMakerBaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

class SageMakerTuningOperator(SageMakerBaseOperator):
    """SageMakerTuningOperator"""
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