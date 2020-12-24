# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/azure_container_instances_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 14394 bytes
from collections import namedtuple
from typing import Sequence, Dict
from time import sleep
import re
from airflow.contrib.hooks.azure_container_instance_hook import AzureContainerInstanceHook
from airflow.contrib.hooks.azure_container_registry_hook import AzureContainerRegistryHook
from airflow.contrib.hooks.azure_container_volume_hook import AzureContainerVolumeHook
from airflow.exceptions import AirflowException, AirflowTaskTimeout
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from azure.mgmt.containerinstance.models import EnvironmentVariable, VolumeMount, ResourceRequests, ResourceRequirements, Container, ContainerGroup
from msrestazure.azure_exceptions import CloudError
Volume = namedtuple('Volume', [
 'conn_id', 'account_name', 'share_name', 'mount_path', 'read_only'])
DEFAULT_ENVIRONMENT_VARIABLES = {}
DEFAULT_SECURED_VARIABLES = []
DEFAULT_VOLUMES = []
DEFAULT_MEMORY_IN_GB = 2.0
DEFAULT_CPU = 1.0

class AzureContainerInstancesOperator(BaseOperator):
    """AzureContainerInstancesOperator"""
    template_fields = ('name', 'image', 'command', 'environment_variables')

    @apply_defaults
    def __init__(self, ci_conn_id, registry_conn_id, resource_group, name, image, region, environment_variables=None, secured_variables=None, volumes=None, memory_in_gb=None, cpu=None, gpu=None, command=None, remove_on_error=True, fail_if_exists=True, *args, **kwargs):
        (super(AzureContainerInstancesOperator, self).__init__)(*args, **kwargs)
        self.ci_conn_id = ci_conn_id
        self.resource_group = resource_group
        self.name = self._check_name(name)
        self.image = image
        self.region = region
        self.registry_conn_id = registry_conn_id
        self.environment_variables = environment_variables or DEFAULT_ENVIRONMENT_VARIABLES
        self.secured_variables = secured_variables or DEFAULT_SECURED_VARIABLES
        self.volumes = volumes or DEFAULT_VOLUMES
        self.memory_in_gb = memory_in_gb or DEFAULT_MEMORY_IN_GB
        self.cpu = cpu or DEFAULT_CPU
        self.gpu = gpu
        self.command = command
        self.remove_on_error = remove_on_error
        self.fail_if_exists = fail_if_exists
        self._ci_hook = None

    def execute(self, context):
        self._check_name(self.name)
        self._ci_hook = AzureContainerInstanceHook(self.ci_conn_id)
        if self.fail_if_exists:
            self.log.info('Testing if container group already exists')
            if self._ci_hook.exists(self.resource_group, self.name):
                raise AirflowException('Container group exists')
        else:
            if self.registry_conn_id:
                registry_hook = AzureContainerRegistryHook(self.registry_conn_id)
                image_registry_credentials = [registry_hook.connection]
            else:
                image_registry_credentials = None
        environment_variables = []
        for key, value in self.environment_variables.items():
            if key in self.secured_variables:
                e = EnvironmentVariable(name=key, secure_value=value)
            else:
                e = EnvironmentVariable(name=key, value=value)
            environment_variables.append(e)

        volumes = []
        volume_mounts = []
        for conn_id, account_name, share_name, mount_path, read_only in self.volumes:
            hook = AzureContainerVolumeHook(conn_id)
            mount_name = 'mount-%d' % len(volumes)
            volumes.append(hook.get_file_volume(mount_name, share_name, account_name, read_only))
            volume_mounts.append(VolumeMount(name=mount_name, mount_path=mount_path,
              read_only=read_only))

        exit_code = 1
        try:
            try:
                self.log.info('Starting container group with %.1f cpu %.1f mem', self.cpu, self.memory_in_gb)
                if self.gpu:
                    self.log.info('GPU count: %.1f, GPU SKU: %s', self.gpu.count, self.gpu.sku)
                resources = ResourceRequirements(requests=ResourceRequests(memory_in_gb=(self.memory_in_gb),
                  cpu=(self.cpu),
                  gpu=(self.gpu)))
                container = Container(name=(self.name),
                  image=(self.image),
                  resources=resources,
                  command=(self.command),
                  environment_variables=environment_variables,
                  volume_mounts=volume_mounts)
                container_group = ContainerGroup(location=(self.region),
                  containers=[
                 container],
                  image_registry_credentials=image_registry_credentials,
                  volumes=volumes,
                  restart_policy='Never',
                  os_type='Linux')
                self._ci_hook.create_or_update(self.resource_group, self.name, container_group)
                self.log.info('Container group started %s/%s', self.resource_group, self.name)
                exit_code = self._monitor_logging(self._ci_hook, self.resource_group, self.name)
                self.log.info('Container had exit code: %s', exit_code)
                if exit_code != 0:
                    raise AirflowException('Container had a non-zero exit code, %s' % exit_code)
                return exit_code
            except CloudError:
                self.log.exception('Could not start container group')
                raise AirflowException('Could not start container group')

        finally:
            if exit_code == 0 or self.remove_on_error:
                self.on_kill()

    def on_kill(self):
        if self.remove_on_error:
            self.log.info('Deleting container group')
            try:
                self._ci_hook.delete(self.resource_group, self.name)
            except Exception:
                self.log.exception('Could not delete container group')

    def _monitor_logging(self, ci_hook, resource_group, name):
        last_state = None
        last_message_logged = None
        last_line_logged = None
        while True:
            try:
                cg_state = self._ci_hook.get_state(resource_group, name)
                instance_view = cg_state.containers[0].instance_view
                if instance_view is not None:
                    c_state = instance_view.current_state
                    state, exit_code, detail_status = c_state.state, c_state.exit_code, c_state.detail_status
                    messages = [event.message for event in instance_view.events]
                    last_message_logged = self._log_last(messages, last_message_logged)
                else:
                    state = cg_state.provisioning_state
                    exit_code = 0
                    detail_status = 'Provisioning'
                if state != last_state:
                    self.log.info('Container group state changed to %s', state)
                    last_state = state
                if state in ('Running', 'Terminated'):
                    try:
                        logs = self._ci_hook.get_logs(resource_group, name)
                        last_line_logged = self._log_last(logs, last_line_logged)
                    except CloudError:
                        self.log.exception('Exception while getting logs from container instance, retrying...')

                if state == 'Terminated':
                    self.log.info('Container exited with detail_status %s', detail_status)
                    return exit_code
                if state == 'Failed':
                    self.log.info('Azure provision failure')
                    return 1
            except AirflowTaskTimeout:
                raise
            except CloudError as err:
                if 'ResourceNotFound' in str(err):
                    self.log.warning('ResourceNotFound, container is probably removed by another process (make sure that the name is unique).')
                    return 1
                self.log.exception('Exception while getting container groups')
            except Exception:
                self.log.exception('Exception while getting container groups')

        sleep(1)

    def _log_last(self, logs, last_line_logged):
        if logs:
            last_line_index = 0
            for i in range(len(logs) - 1, -1, -1):
                if logs[i] == last_line_logged:
                    last_line_index = i + 1
                    break

            for line in logs[last_line_index:]:
                self.log.info(line.rstrip())

            return logs[(-1)]

    @staticmethod
    def _check_name(name):
        if '{{' in name:
            return name
        else:
            regex_check = re.match('[a-z0-9]([-a-z0-9]*[a-z0-9])?', name)
            if regex_check is None or regex_check.group() != name:
                raise AirflowException('ACI name must match regex [a-z0-9]([-a-z0-9]*[a-z0-9])? (like "my-name")')
            if len(name) > 63:
                raise AirflowException('ACI name cannot be longer than 63 characters')
            return name