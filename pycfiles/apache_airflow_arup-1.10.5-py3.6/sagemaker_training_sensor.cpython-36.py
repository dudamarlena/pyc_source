# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/sagemaker_training_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4259 bytes
import time
from airflow.contrib.hooks.sagemaker_hook import SageMakerHook, LogState
from airflow.contrib.sensors.sagemaker_base_sensor import SageMakerBaseSensor
from airflow.utils.decorators import apply_defaults

class SageMakerTrainingSensor(SageMakerBaseSensor):
    __doc__ = '\n    Asks for the state of the training state until it reaches a terminal state.\n    If it fails the sensor errors, failing the task.\n\n    :param job_name: name of the SageMaker training job to check the state of\n    :type job_name: str\n    :param print_log: if the operator should print the cloudwatch log\n    :type print_log: bool\n    '
    template_fields = [
     'job_name']
    template_ext = ()

    @apply_defaults
    def __init__(self, job_name, print_log=True, *args, **kwargs):
        (super(SageMakerTrainingSensor, self).__init__)(*args, **kwargs)
        self.job_name = job_name
        self.print_log = print_log
        self.positions = {}
        self.stream_names = []
        self.instance_count = None
        self.state = None
        self.last_description = None
        self.last_describe_job_call = None
        self.log_resource_inited = False

    def init_log_resource(self, hook):
        description = hook.describe_training_job(self.job_name)
        self.instance_count = description['ResourceConfig']['InstanceCount']
        status = description['TrainingJobStatus']
        job_already_completed = status not in self.non_terminal_states()
        self.state = LogState.TAILING if not job_already_completed else LogState.COMPLETE
        self.last_description = description
        self.last_describe_job_call = time.time()
        self.log_resource_inited = True

    def non_terminal_states(self):
        return SageMakerHook.non_terminal_states

    def failed_states(self):
        return SageMakerHook.failed_states

    def get_sagemaker_response(self):
        sagemaker_hook = SageMakerHook(aws_conn_id=(self.aws_conn_id))
        if self.print_log:
            if not self.log_resource_inited:
                self.init_log_resource(sagemaker_hook)
            self.state, self.last_description, self.last_describe_job_call = sagemaker_hook.describe_training_job_with_log(self.job_name, self.positions, self.stream_names, self.instance_count, self.state, self.last_description, self.last_describe_job_call)
        else:
            self.last_description = sagemaker_hook.describe_training_job(self.job_name)
        status = self.state_from_response(self.last_description)
        if status not in self.non_terminal_states():
            if status not in self.failed_states():
                billable_time = (self.last_description['TrainingEndTime'] - self.last_description['TrainingStartTime']) * self.last_description['ResourceConfig']['InstanceCount']
                self.log.info('Billable seconds: %s', int(billable_time.total_seconds()) + 1)
        return self.last_description

    def get_failed_reason_from_response(self, response):
        return response['FailureReason']

    def state_from_response(self, response):
        return response['TrainingJobStatus']