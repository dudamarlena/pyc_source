# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/ecs_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 9064 bytes
import sys, re
from datetime import datetime
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.contrib.hooks.aws_logs_hook import AwsLogsHook

class ECSOperator(BaseOperator):
    """ECSOperator"""
    ui_color = '#f0ede4'
    client = None
    arn = None
    template_fields = ('overrides', )

    @apply_defaults
    def __init__(self, task_definition, cluster, overrides, aws_conn_id=None, region_name=None, launch_type='EC2', group=None, placement_constraints=None, platform_version='LATEST', network_configuration=None, awslogs_group=None, awslogs_region=None, awslogs_stream_prefix=None, **kwargs):
        (super(ECSOperator, self).__init__)(**kwargs)
        self.aws_conn_id = aws_conn_id
        self.region_name = region_name
        self.task_definition = task_definition
        self.cluster = cluster
        self.overrides = overrides
        self.launch_type = launch_type
        self.group = group
        self.placement_constraints = placement_constraints
        self.platform_version = platform_version
        self.network_configuration = network_configuration
        self.awslogs_group = awslogs_group
        self.awslogs_stream_prefix = awslogs_stream_prefix
        self.awslogs_region = awslogs_region
        if self.awslogs_region is None:
            self.awslogs_region = region_name
        self.hook = self.get_hook()

    def execute(self, context):
        self.log.info('Running ECS Task - Task definition: %s - on cluster %s', self.task_definition, self.cluster)
        self.log.info('ECSOperator overrides: %s', self.overrides)
        self.client = self.hook.get_client_type('ecs',
          region_name=(self.region_name))
        run_opts = {'cluster':self.cluster, 
         'taskDefinition':self.task_definition, 
         'overrides':self.overrides, 
         'startedBy':self.owner, 
         'launchType':self.launch_type}
        if self.launch_type == 'FARGATE':
            run_opts['platformVersion'] = self.platform_version
        if self.group is not None:
            run_opts['group'] = self.group
        if self.placement_constraints is not None:
            run_opts['placementConstraints'] = self.placement_constraints
        if self.network_configuration is not None:
            run_opts['networkConfiguration'] = self.network_configuration
        response = (self.client.run_task)(**run_opts)
        failures = response['failures']
        if len(failures) > 0:
            raise AirflowException(response)
        self.log.info('ECS Task started: %s', response)
        self.arn = response['tasks'][0]['taskArn']
        self._wait_for_task_ended()
        self._check_success_task()
        self.log.info('ECS Task has been successfully executed: %s', response)

    def _wait_for_task_ended(self):
        waiter = self.client.get_waiter('tasks_stopped')
        waiter.config.max_attempts = sys.maxsize
        waiter.wait(cluster=(self.cluster),
          tasks=[
         self.arn])

    def _check_success_task(self):
        response = self.client.describe_tasks(cluster=(self.cluster),
          tasks=[
         self.arn])
        self.log.info('ECS Task stopped, check status: %s', response)
        if self.awslogs_group:
            if self.awslogs_stream_prefix:
                self.log.info('ECS Task logs output:')
                task_id = self.arn.split('/')[(-1)]
                stream_name = '{}/{}'.format(self.awslogs_stream_prefix, task_id)
                for event in self.get_logs_hook().get_log_events(self.awslogs_group, stream_name):
                    dt = datetime.fromtimestamp(event['timestamp'] / 1000.0)
                    self.log.info('[{}] {}'.format(dt.isoformat(), event['message']))

        if len(response.get('failures', [])) > 0:
            raise AirflowException(response)
        for task in response['tasks']:
            if re.match('Host EC2 \\(instance .+?\\) (stopped|terminated)\\.', task.get('stoppedReason', '')):
                raise AirflowException('The task was stopped because the host instance terminated: {}'.format(task.get('stoppedReason', '')))
            containers = task['containers']
            for container in containers:
                if container.get('lastStatus') == 'STOPPED':
                    if container['exitCode'] != 0:
                        raise AirflowException('This task is not in success state {}'.format(task))
                    else:
                        if container.get('lastStatus') == 'PENDING':
                            raise AirflowException('This task is still pending {}'.format(task))
                        elif 'error' in container.get('reason', '').lower():
                            raise AirflowException('This containers encounter an error during launching : {}'.format(container.get('reason', '').lower()))

    def get_hook(self):
        return AwsHook(aws_conn_id=(self.aws_conn_id))

    def get_logs_hook(self):
        return AwsLogsHook(aws_conn_id=(self.aws_conn_id),
          region_name=(self.awslogs_region))

    def on_kill(self):
        response = self.client.stop_task(cluster=(self.cluster),
          task=(self.arn),
          reason='Task killed by the user')
        self.log.info(response)