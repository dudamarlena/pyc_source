# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_compute_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 21624 bytes
from copy import deepcopy
from googleapiclient.errors import HttpError
from airflow import AirflowException
from airflow.contrib.hooks.gcp_compute_hook import GceHook
from airflow.contrib.utils.gcp_field_sanitizer import GcpBodyFieldSanitizer
from airflow.contrib.utils.gcp_field_validator import GcpBodyFieldValidator
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from json_merge_patch import merge

class GceBaseOperator(BaseOperator):
    """GceBaseOperator"""

    @apply_defaults
    def __init__(self, zone, resource_id, project_id=None, gcp_conn_id='google_cloud_default', api_version='v1', *args, **kwargs):
        self.project_id = project_id
        self.zone = zone
        self.resource_id = resource_id
        self.gcp_conn_id = gcp_conn_id
        self.api_version = api_version
        self._validate_inputs()
        self._hook = GceHook(gcp_conn_id=(self.gcp_conn_id), api_version=(self.api_version))
        (super(GceBaseOperator, self).__init__)(*args, **kwargs)

    def _validate_inputs(self):
        if self.project_id == '':
            raise AirflowException("The required parameter 'project_id' is missing")
        else:
            if not self.zone:
                raise AirflowException("The required parameter 'zone' is missing")
            raise self.resource_id or AirflowException("The required parameter 'resource_id' is missing")

    def execute(self, context):
        pass


class GceInstanceStartOperator(GceBaseOperator):
    """GceInstanceStartOperator"""
    template_fields = ('project_id', 'zone', 'resource_id', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, zone, resource_id, project_id=None, gcp_conn_id='google_cloud_default', api_version='v1', *args, **kwargs):
        (super(GceInstanceStartOperator, self).__init__)(args, project_id=project_id, zone=zone, resource_id=resource_id, gcp_conn_id=gcp_conn_id, api_version=api_version, **kwargs)

    def execute(self, context):
        return self._hook.start_instance(zone=(self.zone), resource_id=(self.resource_id),
          project_id=(self.project_id))


class GceInstanceStopOperator(GceBaseOperator):
    """GceInstanceStopOperator"""
    template_fields = ('project_id', 'zone', 'resource_id', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, zone, resource_id, project_id=None, gcp_conn_id='google_cloud_default', api_version='v1', *args, **kwargs):
        (super(GceInstanceStopOperator, self).__init__)(args, project_id=project_id, zone=zone, resource_id=resource_id, gcp_conn_id=gcp_conn_id, api_version=api_version, **kwargs)

    def execute(self, context):
        self._hook.stop_instance(zone=(self.zone), resource_id=(self.resource_id),
          project_id=(self.project_id))


SET_MACHINE_TYPE_VALIDATION_SPECIFICATION = [
 dict(name='machineType', regexp='^.+$')]

class GceSetMachineTypeOperator(GceBaseOperator):
    """GceSetMachineTypeOperator"""
    template_fields = ('project_id', 'zone', 'resource_id', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, zone, resource_id, body, project_id=None, gcp_conn_id='google_cloud_default', api_version='v1', validate_body=True, *args, **kwargs):
        self.body = body
        self._field_validator = None
        if validate_body:
            self._field_validator = GcpBodyFieldValidator(SET_MACHINE_TYPE_VALIDATION_SPECIFICATION,
              api_version=api_version)
        (super(GceSetMachineTypeOperator, self).__init__)(args, project_id=project_id, zone=zone, resource_id=resource_id, gcp_conn_id=gcp_conn_id, api_version=api_version, **kwargs)

    def _validate_all_body_fields(self):
        if self._field_validator:
            self._field_validator.validate(self.body)

    def execute(self, context):
        self._validate_all_body_fields()
        return self._hook.set_machine_type(zone=(self.zone), resource_id=(self.resource_id),
          body=(self.body),
          project_id=(self.project_id))


GCE_INSTANCE_TEMPLATE_VALIDATION_PATCH_SPECIFICATION = [
 dict(name='name', regexp='^.+$'),
 dict(name='description', optional=True),
 dict(name='properties', type='dict', optional=True, fields=[
  dict(name='description', optional=True),
  dict(name='tags', optional=True, fields=[
   dict(name='items', optional=True)]),
  dict(name='machineType', optional=True),
  dict(name='canIpForward', optional=True),
  dict(name='networkInterfaces', optional=True),
  dict(name='disks', optional=True),
  dict(name='metadata', optional=True, fields=[
   dict(name='fingerprint', optional=True),
   dict(name='items', optional=True),
   dict(name='kind', optional=True)]),
  dict(name='serviceAccounts', optional=True),
  dict(name='scheduling', optional=True, fields=[
   dict(name='onHostMaintenance', optional=True),
   dict(name='automaticRestart', optional=True),
   dict(name='preemptible', optional=True),
   dict(name='nodeAffinitites', optional=True)]),
  dict(name='labels', optional=True),
  dict(name='guestAccelerators', optional=True),
  dict(name='minCpuPlatform', optional=True)])]
GCE_INSTANCE_TEMPLATE_FIELDS_TO_SANITIZE = [
 'kind',
 'id',
 'name',
 'creationTimestamp',
 'properties.disks.sha256',
 'properties.disks.kind',
 'properties.disks.sourceImageEncryptionKey.sha256',
 'properties.disks.index',
 'properties.disks.licenses',
 'properties.networkInterfaces.kind',
 'properties.networkInterfaces.accessConfigs.kind',
 'properties.networkInterfaces.name',
 'properties.metadata.kind',
 'selfLink']

class GceInstanceTemplateCopyOperator(GceBaseOperator):
    """GceInstanceTemplateCopyOperator"""
    template_fields = ('project_id', 'resource_id', 'request_id', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, resource_id, body_patch, project_id=None, request_id=None, gcp_conn_id='google_cloud_default', api_version='v1', validate_body=True, *args, **kwargs):
        self.body_patch = body_patch
        self.request_id = request_id
        self._field_validator = None
        if 'name' not in self.body_patch:
            raise AirflowException("The body '{}' should contain at least name for the new operator in the 'name' field".format(body_patch))
        if validate_body:
            self._field_validator = GcpBodyFieldValidator(GCE_INSTANCE_TEMPLATE_VALIDATION_PATCH_SPECIFICATION,
              api_version=api_version)
        self._field_sanitizer = GcpBodyFieldSanitizer(GCE_INSTANCE_TEMPLATE_FIELDS_TO_SANITIZE)
        (super(GceInstanceTemplateCopyOperator, self).__init__)(args, project_id=project_id, zone='global', resource_id=resource_id, gcp_conn_id=gcp_conn_id, api_version=api_version, **kwargs)

    def _validate_all_body_fields(self):
        if self._field_validator:
            self._field_validator.validate(self.body_patch)

    def execute(self, context):
        self._validate_all_body_fields()
        try:
            existing_template = self._hook.get_instance_template(resource_id=(self.body_patch['name']),
              project_id=(self.project_id))
            self.log.info('The %s template already existed. It was likely created by previous run of the operator. Assuming success.', existing_template)
            return existing_template
        except HttpError as e:
            if not e.resp.status == 404:
                raise e

        old_body = self._hook.get_instance_template(resource_id=(self.resource_id), project_id=(self.project_id))
        new_body = deepcopy(old_body)
        self._field_sanitizer.sanitize(new_body)
        new_body = merge(new_body, self.body_patch)
        self.log.info('Calling insert instance template with updated body: %s', new_body)
        self._hook.insert_instance_template(body=new_body, request_id=(self.request_id),
          project_id=(self.project_id))
        return self._hook.get_instance_template(resource_id=(self.body_patch['name']), project_id=(self.project_id))


class GceInstanceGroupManagerUpdateTemplateOperator(GceBaseOperator):
    """GceInstanceGroupManagerUpdateTemplateOperator"""
    template_fields = ('project_id', 'resource_id', 'zone', 'request_id', 'source_template',
                       'destination_template', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, resource_id, zone, source_template, destination_template, project_id=None, update_policy=None, request_id=None, gcp_conn_id='google_cloud_default', api_version='beta', *args, **kwargs):
        self.zone = zone
        self.source_template = source_template
        self.destination_template = destination_template
        self.request_id = request_id
        self.update_policy = update_policy
        self._change_performed = False
        if api_version == 'v1':
            raise AirflowException('Api version v1 does not have update/patch operations for Instance Group Managers. Use beta api version or above')
        (super(GceInstanceGroupManagerUpdateTemplateOperator, self).__init__)(args, project_id=project_id, zone=self.zone, resource_id=resource_id, gcp_conn_id=gcp_conn_id, api_version=api_version, **kwargs)

    def _possibly_replace_template(self, dictionary):
        if dictionary.get('instanceTemplate') == self.source_template:
            dictionary['instanceTemplate'] = self.destination_template
            self._change_performed = True

    def execute(self, context):
        old_instance_group_manager = self._hook.get_instance_group_manager(zone=(self.zone),
          resource_id=(self.resource_id),
          project_id=(self.project_id))
        patch_body = {}
        if 'versions' in old_instance_group_manager:
            patch_body['versions'] = old_instance_group_manager['versions']
        if 'instanceTemplate' in old_instance_group_manager:
            patch_body['instanceTemplate'] = old_instance_group_manager['instanceTemplate']
        if self.update_policy:
            patch_body['updatePolicy'] = self.update_policy
        self._possibly_replace_template(patch_body)
        if 'versions' in patch_body:
            for version in patch_body['versions']:
                self._possibly_replace_template(version)

        if self._change_performed or self.update_policy:
            self.log.info('Calling patch instance template with updated body: {}'.format(patch_body))
            return self._hook.patch_instance_group_manager(zone=(self.zone),
              resource_id=(self.resource_id),
              body=patch_body,
              request_id=(self.request_id),
              project_id=(self.project_id))
        else:
            return True