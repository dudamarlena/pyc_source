# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/sagemaker_training_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4259 bytes
import time
from airflow.contrib.hooks.sagemaker_hook import SageMakerHook, LogState
from airflow.contrib.sensors.sagemaker_base_sensor import SageMakerBaseSensor
from airflow.utils.decorators import apply_defaults

class SageMakerTrainingSensor(SageMakerBaseSensor):
    """SageMakerTrainingSensor"""
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