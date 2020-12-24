# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/awsbatch_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6305 bytes
import sys
from math import pow
from time import sleep
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook

class AWSBatchOperator(BaseOperator):
    """AWSBatchOperator"""
    ui_color = '#c3dae0'
    client = None
    arn = None
    template_fields = ('job_name', 'overrides')

    @apply_defaults
    def __init__(self, job_name, job_definition, job_queue, overrides, max_retries=4200, aws_conn_id=None, region_name=None, **kwargs):
        (super(AWSBatchOperator, self).__init__)(**kwargs)
        self.job_name = job_name
        self.aws_conn_id = aws_conn_id
        self.region_name = region_name
        self.job_definition = job_definition
        self.job_queue = job_queue
        self.overrides = overrides
        self.max_retries = max_retries
        self.jobId = None
        self.jobName = None
        self.hook = self.get_hook()

    def execute(self, context):
        self.log.info('Running AWS Batch Job - Job definition: %s - on queue %s', self.job_definition, self.job_queue)
        self.log.info('AWSBatchOperator overrides: %s', self.overrides)
        self.client = self.hook.get_client_type('batch',
          region_name=(self.region_name))
        try:
            response = self.client.submit_job(jobName=(self.job_name),
              jobQueue=(self.job_queue),
              jobDefinition=(self.job_definition),
              containerOverrides=(self.overrides))
            self.log.info('AWS Batch Job started: %s', response)
            self.jobId = response['jobId']
            self.jobName = response['jobName']
            self._wait_for_task_ended()
            self._check_success_task()
            self.log.info('AWS Batch Job has been successfully executed: %s', response)
        except Exception as e:
            self.log.info('AWS Batch Job has failed executed')
            raise AirflowException(e)

    def _wait_for_task_ended(self):
        """
        Try to use a waiter from the below pull request

            * https://github.com/boto/botocore/pull/1307

        If the waiter is not available apply a exponential backoff

            * docs.aws.amazon.com/general/latest/gr/api-retries.html
        """
        try:
            waiter = self.client.get_waiter('job_execution_complete')
            waiter.config.max_attempts = sys.maxsize
            waiter.wait(jobs=[self.jobId])
        except ValueError:
            retry = True
            retries = 0
            while retries < self.max_retries and retry:
                self.log.info('AWS Batch retry in the next %s seconds', retries)
                response = self.client.describe_jobs(jobs=[
                 self.jobId])
                if response['jobs'][(-1)]['status'] in ('SUCCEEDED', 'FAILED'):
                    retry = False
                sleep(1 + pow(retries * 0.1, 2))
                retries += 1

    def _check_success_task(self):
        response = self.client.describe_jobs(jobs=[
         self.jobId])
        self.log.info('AWS Batch stopped, check status: %s', response)
        if len(response.get('jobs')) < 1:
            raise AirflowException('No job found for {}'.format(response))
        for job in response['jobs']:
            job_status = job['status']
            if job_status == 'FAILED':
                reason = job['statusReason']
                raise AirflowException('Job failed with status {}'.format(reason))
            else:
                if job_status in ('SUBMITTED', 'PENDING', 'RUNNABLE', 'STARTING', 'RUNNING'):
                    raise AirflowException('This task is still pending {}'.format(job_status))

    def get_hook(self):
        return AwsHook(aws_conn_id=(self.aws_conn_id))

    def on_kill(self):
        response = self.client.terminate_job(jobId=(self.jobId),
          reason='Task killed by the user')
        self.log.info(response)