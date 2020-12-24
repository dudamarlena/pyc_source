# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/sagemaker_transform_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2251 bytes
from airflow.contrib.hooks.sagemaker_hook import SageMakerHook
from airflow.contrib.sensors.sagemaker_base_sensor import SageMakerBaseSensor
from airflow.utils.decorators import apply_defaults

class SageMakerTransformSensor(SageMakerBaseSensor):
    __doc__ = '\n    Asks for the state of the transform state until it reaches a terminal state.\n    The sensor will error if the job errors, throwing a AirflowException\n    containing the failure reason.\n\n    :param job_name: job_name of the transform job instance to check the state of\n    :type job_name: string\n    '
    template_fields = [
     'job_name']
    template_ext = ()

    @apply_defaults
    def __init__(self, job_name, *args, **kwargs):
        (super(SageMakerTransformSensor, self).__init__)(*args, **kwargs)
        self.job_name = job_name

    def non_terminal_states(self):
        return SageMakerHook.non_terminal_states

    def failed_states(self):
        return SageMakerHook.failed_states

    def get_sagemaker_response(self):
        sagemaker = SageMakerHook(aws_conn_id=(self.aws_conn_id))
        self.log.info('Poking Sagemaker Transform Job %s', self.job_name)
        return sagemaker.describe_transform_job(self.job_name)

    def get_failed_reason_from_response(self, response):
        return response['FailureReason']

    def state_from_response(self, response):
        return response['TransformJobStatus']