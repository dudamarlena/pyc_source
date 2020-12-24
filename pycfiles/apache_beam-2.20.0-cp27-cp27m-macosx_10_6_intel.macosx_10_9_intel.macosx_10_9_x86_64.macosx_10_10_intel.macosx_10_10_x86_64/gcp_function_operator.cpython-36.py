# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_function_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 13438 bytes
import re
from googleapiclient.errors import HttpError
from airflow import AirflowException
from airflow.contrib.utils.gcp_field_validator import GcpBodyFieldValidator, GcpFieldValidationException
from airflow.version import version
from airflow.models import BaseOperator
from airflow.contrib.hooks.gcp_function_hook import GcfHook
from airflow.utils.decorators import apply_defaults

def _validate_available_memory_in_mb(value):
    if int(value) <= 0:
        raise GcpFieldValidationException('The available memory has to be greater than 0')


def _validate_max_instances(value):
    if int(value) <= 0:
        raise GcpFieldValidationException('The max instances parameter has to be greater than 0')


CLOUD_FUNCTION_VALIDATION = [
 dict(name='name', regexp='^.+$'),
 dict(name='description', regexp='^.+$', optional=True),
 dict(name='entryPoint', regexp='^.+$', optional=True),
 dict(name='runtime', regexp='^.+$', optional=True),
 dict(name='timeout', regexp='^.+$', optional=True),
 dict(name='availableMemoryMb', custom_validation=_validate_available_memory_in_mb, optional=True),
 dict(name='labels', optional=True),
 dict(name='environmentVariables', optional=True),
 dict(name='network', regexp='^.+$', optional=True),
 dict(name='maxInstances', optional=True, custom_validation=_validate_max_instances),
 dict(name='source_code', type='union', fields=[
  dict(name='sourceArchiveUrl', regexp='^.+$'),
  dict(name='sourceRepositoryUrl', regexp='^.+$', api_version='v1beta2'),
  dict(name='sourceRepository', type='dict', fields=[
   dict(name='url', regexp='^.+$')]),
  dict(name='sourceUploadUrl')]),
 dict(name='trigger', type='union', fields=[
  dict(name='httpsTrigger', type='dict', fields=[]),
  dict(name='eventTrigger', type='dict', fields=[
   dict(name='eventType', regexp='^.+$'),
   dict(name='resource', regexp='^.+$'),
   dict(name='service', regexp='^.+$', optional=True),
   dict(name='failurePolicy', type='dict', optional=True, fields=[
    dict(name='retry', type='dict', optional=True)])])])]

class GcfFunctionDeployOperator(BaseOperator):
    """GcfFunctionDeployOperator"""
    template_fields = ('project_id', 'location', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, location, body, project_id=None, gcp_conn_id='google_cloud_default', api_version='v1', zip_path=None, validate_body=True, *args, **kwargs):
        self.project_id = project_id
        self.location = location
        self.body = body
        self.gcp_conn_id = gcp_conn_id
        self.api_version = api_version
        self.zip_path = zip_path
        self.zip_path_preprocessor = ZipPathPreprocessor(body, zip_path)
        self._field_validator = None
        if validate_body:
            self._field_validator = GcpBodyFieldValidator(CLOUD_FUNCTION_VALIDATION, api_version=api_version)
        self._hook = GcfHook(gcp_conn_id=(self.gcp_conn_id), api_version=(self.api_version))
        self._validate_inputs()
        (super(GcfFunctionDeployOperator, self).__init__)(*args, **kwargs)

    def _validate_inputs(self):
        if not self.location:
            raise AirflowException("The required parameter 'location' is missing")
        if not self.body:
            raise AirflowException("The required parameter 'body' is missing")
        self.zip_path_preprocessor.preprocess_body()

    def _validate_all_body_fields(self):
        if self._field_validator:
            self._field_validator.validate(self.body)

    def _create_new_function(self):
        self._hook.create_new_function(project_id=(self.project_id),
          location=(self.location),
          body=(self.body))

    def _update_function(self):
        self._hook.update_function(self.body['name'], self.body, self.body.keys())

    def _check_if_function_exists(self):
        name = self.body.get('name')
        if not name:
            raise GcpFieldValidationException("The 'name' field should be present in body: '{}'.".format(self.body))
        try:
            self._hook.get_function(name)
        except HttpError as e:
            status = e.resp.status
            if status == 404:
                return False
            raise e

        return True

    def _upload_source_code(self):
        return self._hook.upload_function_zip(project_id=(self.project_id), location=(self.location),
          zip_path=(self.zip_path))

    def _set_airflow_version_label(self):
        if 'labels' not in self.body.keys():
            self.body['labels'] = {}
        self.body['labels'].update({'airflow-version': 'v' + version.replace('.', '-').replace('+', '-')})

    def execute(self, context):
        if self.zip_path_preprocessor.should_upload_function():
            self.body[GCF_SOURCE_UPLOAD_URL] = self._upload_source_code()
        else:
            self._validate_all_body_fields()
            self._set_airflow_version_label()
            if not self._check_if_function_exists():
                self._create_new_function()
            else:
                self._update_function()


GCF_SOURCE_ARCHIVE_URL = 'sourceArchiveUrl'
GCF_SOURCE_UPLOAD_URL = 'sourceUploadUrl'
SOURCE_REPOSITORY = 'sourceRepository'
GCF_ZIP_PATH = 'zip_path'

class ZipPathPreprocessor:
    """ZipPathPreprocessor"""
    upload_function = None

    def __init__(self, body, zip_path):
        self.body = body
        self.zip_path = zip_path

    @staticmethod
    def _is_present_and_empty(dictionary, field):
        return field in dictionary and not dictionary[field]

    def _verify_upload_url_and_no_zip_path(self):
        if self._is_present_and_empty(self.body, GCF_SOURCE_UPLOAD_URL):
            if not self.zip_path:
                raise AirflowException("Parameter '{}' is empty in the body and argument '{}' is missing or empty. You need to have non empty '{}' when '{}' is present and empty.".format(GCF_SOURCE_UPLOAD_URL, GCF_ZIP_PATH, GCF_ZIP_PATH, GCF_SOURCE_UPLOAD_URL))

    def _verify_upload_url_and_zip_path(self):
        if GCF_SOURCE_UPLOAD_URL in self.body:
            if self.zip_path:
                self.upload_function = self.body[GCF_SOURCE_UPLOAD_URL] or True
            else:
                raise AirflowException("Only one of '{}' in body or '{}' argument allowed. Found both.".format(GCF_SOURCE_UPLOAD_URL, GCF_ZIP_PATH))

    def _verify_archive_url_and_zip_path(self):
        if GCF_SOURCE_ARCHIVE_URL in self.body:
            if self.zip_path:
                raise AirflowException("Only one of '{}' in body or '{}' argument allowed. Found both.".format(GCF_SOURCE_ARCHIVE_URL, GCF_ZIP_PATH))

    def should_upload_function(self):
        if self.upload_function is None:
            raise AirflowException('validate() method has to be invoked before should_upload_function')
        return self.upload_function

    def preprocess_body(self):
        self._verify_archive_url_and_zip_path()
        self._verify_upload_url_and_zip_path()
        self._verify_upload_url_and_no_zip_path()
        if self.upload_function is None:
            self.upload_function = False


FUNCTION_NAME_PATTERN = '^projects/[^/]+/locations/[^/]+/functions/[^/]+$'
FUNCTION_NAME_COMPILED_PATTERN = re.compile(FUNCTION_NAME_PATTERN)

class GcfFunctionDeleteOperator(BaseOperator):
    """GcfFunctionDeleteOperator"""
    template_fields = ('name', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, name, gcp_conn_id='google_cloud_default', api_version='v1', *args, **kwargs):
        self.name = name
        self.gcp_conn_id = gcp_conn_id
        self.api_version = api_version
        self._validate_inputs()
        self.hook = GcfHook(gcp_conn_id=(self.gcp_conn_id), api_version=(self.api_version))
        (super(GcfFunctionDeleteOperator, self).__init__)(*args, **kwargs)

    def _validate_inputs(self):
        if not self.name:
            raise AttributeError('Empty parameter: name')
        else:
            pattern = FUNCTION_NAME_COMPILED_PATTERN
        if not pattern.match(self.name):
            raise AttributeError('Parameter name must match pattern: {}'.format(FUNCTION_NAME_PATTERN))

    def execute(self, context):
        try:
            return self.hook.delete_function(self.name)
        except HttpError as e:
            status = e.resp.status
            if status == 404:
                self.log.info('The function does not exist in this project')
            else:
                self.log.error('An error occurred. Exiting.')
                raise e