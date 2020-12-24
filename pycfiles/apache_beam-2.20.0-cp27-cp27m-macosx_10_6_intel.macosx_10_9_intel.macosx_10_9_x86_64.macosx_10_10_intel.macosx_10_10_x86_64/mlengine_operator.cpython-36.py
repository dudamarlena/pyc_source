# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/mlengine_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 23612 bytes
import re
from googleapiclient.errors import HttpError
from airflow.contrib.hooks.gcp_mlengine_hook import MLEngineHook
from airflow.exceptions import AirflowException
from airflow.operators import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.utils.log.logging_mixin import LoggingMixin
log = LoggingMixin().log

def _normalize_mlengine_job_id(job_id):
    """
    Replaces invalid MLEngine job_id characters with '_'.

    This also adds a leading 'z' in case job_id starts with an invalid
    character.

    Args:
        job_id: A job_id str that may have invalid characters.

    Returns:
        A valid job_id representation.
    """
    match = re.search('\\d|\\{{2}', job_id)
    if match:
        if match.start() == 0:
            job = 'z_{}'.format(job_id)
    else:
        job = job_id
    tracker = 0
    cleansed_job_id = ''
    for m in re.finditer('\\{{2}.+?\\}{2}', job):
        cleansed_job_id += re.sub('[^0-9a-zA-Z]+', '_', job[tracker:m.start()])
        cleansed_job_id += job[m.start():m.end()]
        tracker = m.end()

    cleansed_job_id += re.sub('[^0-9a-zA-Z]+', '_', job[tracker:])
    return cleansed_job_id


class MLEngineBatchPredictionOperator(BaseOperator):
    """MLEngineBatchPredictionOperator"""
    template_fields = [
     '_project_id',
     '_job_id',
     '_region',
     '_input_paths',
     '_output_path',
     '_model_name',
     '_version_name',
     '_uri']

    @apply_defaults
    def __init__(self, project_id, job_id, region, data_format, input_paths, output_path, model_name=None, version_name=None, uri=None, max_worker_count=None, runtime_version=None, signature_name=None, gcp_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        (super(MLEngineBatchPredictionOperator, self).__init__)(*args, **kwargs)
        self._project_id = project_id
        self._job_id = job_id
        self._region = region
        self._data_format = data_format
        self._input_paths = input_paths
        self._output_path = output_path
        self._model_name = model_name
        self._version_name = version_name
        self._uri = uri
        self._max_worker_count = max_worker_count
        self._runtime_version = runtime_version
        self._signature_name = signature_name
        self._gcp_conn_id = gcp_conn_id
        self._delegate_to = delegate_to
        if not self._project_id:
            raise AirflowException('Google Cloud project id is required.')
        if not self._job_id:
            raise AirflowException('An unique job id is required for Google MLEngine prediction job.')
        if self._uri:
            if self._model_name or self._version_name:
                raise AirflowException('Ambiguous model origin: Both uri and model/version name are provided.')
        if self._version_name:
            if not self._model_name:
                raise AirflowException('Missing model: Batch prediction expects a model name when a version name is provided.')
        if not (self._uri or self._model_name):
            raise AirflowException('Missing model origin: Batch prediction expects a model, a model & version combination, or a URI to a savedModel.')

    def execute(self, context):
        job_id = _normalize_mlengine_job_id(self._job_id)
        prediction_request = {'jobId':job_id, 
         'predictionInput':{'dataFormat':self._data_format, 
          'inputPaths':self._input_paths, 
          'outputPath':self._output_path, 
          'region':self._region}}
        if self._uri:
            prediction_request['predictionInput']['uri'] = self._uri
        else:
            if self._model_name:
                origin_name = 'projects/{}/models/{}'.format(self._project_id, self._model_name)
                prediction_request['predictionInput']['modelName'] = self._version_name or origin_name
            else:
                prediction_request['predictionInput']['versionName'] = origin_name + '/versions/{}'.format(self._version_name)
        if self._max_worker_count:
            prediction_request['predictionInput']['maxWorkerCount'] = self._max_worker_count
        if self._runtime_version:
            prediction_request['predictionInput']['runtimeVersion'] = self._runtime_version
        if self._signature_name:
            prediction_request['predictionInput']['signatureName'] = self._signature_name
        hook = MLEngineHook(self._gcp_conn_id, self._delegate_to)

        def check_existing_job(existing_job):
            return existing_job.get('predictionInput', None) == prediction_request['predictionInput']

        try:
            finished_prediction_job = hook.create_job(self._project_id, prediction_request, check_existing_job)
        except HttpError:
            raise

        if finished_prediction_job['state'] != 'SUCCEEDED':
            self.log.error('MLEngine batch prediction job failed: %s', str(finished_prediction_job))
            raise RuntimeError(finished_prediction_job['errorMessage'])
        return finished_prediction_job['predictionOutput']


class MLEngineModelOperator(BaseOperator):
    """MLEngineModelOperator"""
    template_fields = [
     '_model']

    @apply_defaults
    def __init__(self, project_id, model, operation='create', gcp_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        (super(MLEngineModelOperator, self).__init__)(*args, **kwargs)
        self._project_id = project_id
        self._model = model
        self._operation = operation
        self._gcp_conn_id = gcp_conn_id
        self._delegate_to = delegate_to

    def execute(self, context):
        hook = MLEngineHook(gcp_conn_id=(self._gcp_conn_id),
          delegate_to=(self._delegate_to))
        if self._operation == 'create':
            return hook.create_model(self._project_id, self._model)
        if self._operation == 'get':
            return hook.get_model(self._project_id, self._model['name'])
        raise ValueError('Unknown operation: {}'.format(self._operation))


class MLEngineVersionOperator(BaseOperator):
    """MLEngineVersionOperator"""
    template_fields = [
     '_model_name',
     '_version_name',
     '_version']

    @apply_defaults
    def __init__(self, project_id, model_name, version_name=None, version=None, operation='create', gcp_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        (super(MLEngineVersionOperator, self).__init__)(*args, **kwargs)
        self._project_id = project_id
        self._model_name = model_name
        self._version_name = version_name
        self._version = version or {}
        self._operation = operation
        self._gcp_conn_id = gcp_conn_id
        self._delegate_to = delegate_to

    def execute(self, context):
        if 'name' not in self._version:
            self._version['name'] = self._version_name
        else:
            hook = MLEngineHook(gcp_conn_id=(self._gcp_conn_id),
              delegate_to=(self._delegate_to))
            if self._operation == 'create':
                if not self._version:
                    raise ValueError('version attribute of {} could not be empty'.format(self.__class__.__name__))
                return hook.create_version(self._project_id, self._model_name, self._version)
            if self._operation == 'set_default':
                return hook.set_default_version(self._project_id, self._model_name, self._version['name'])
            if self._operation == 'list':
                return hook.list_versions(self._project_id, self._model_name)
            if self._operation == 'delete':
                return hook.delete_version(self._project_id, self._model_name, self._version['name'])
        raise ValueError('Unknown operation: {}'.format(self._operation))


class MLEngineTrainingOperator(BaseOperator):
    """MLEngineTrainingOperator"""
    template_fields = [
     '_project_id',
     '_job_id',
     '_package_uris',
     '_training_python_module',
     '_training_args',
     '_region',
     '_scale_tier',
     '_master_type',
     '_runtime_version',
     '_python_version',
     '_job_dir']

    @apply_defaults
    def __init__(self, project_id, job_id, package_uris, training_python_module, training_args, region, scale_tier=None, master_type=None, runtime_version=None, python_version=None, job_dir=None, gcp_conn_id='google_cloud_default', delegate_to=None, mode='PRODUCTION', *args, **kwargs):
        (super(MLEngineTrainingOperator, self).__init__)(*args, **kwargs)
        self._project_id = project_id
        self._job_id = job_id
        self._package_uris = package_uris
        self._training_python_module = training_python_module
        self._training_args = training_args
        self._region = region
        self._scale_tier = scale_tier
        self._master_type = master_type
        self._runtime_version = runtime_version
        self._python_version = python_version
        self._job_dir = job_dir
        self._gcp_conn_id = gcp_conn_id
        self._delegate_to = delegate_to
        self._mode = mode
        if not self._project_id:
            raise AirflowException('Google Cloud project id is required.')
        if not self._job_id:
            raise AirflowException('An unique job id is required for Google MLEngine training job.')
        if not package_uris:
            raise AirflowException('At least one python package is required for MLEngine Training job.')
        if not training_python_module:
            raise AirflowException('Python module name to run after installing required packages is required.')
        if not self._region:
            raise AirflowException('Google Compute Engine region is required.')
        if self._scale_tier is not None:
            if self._scale_tier.upper() == 'CUSTOM':
                if not self._master_type:
                    raise AirflowException('master_type must be set when scale_tier is CUSTOM')

    def execute(self, context):
        job_id = _normalize_mlengine_job_id(self._job_id)
        training_request = {'jobId':job_id, 
         'trainingInput':{'scaleTier':self._scale_tier, 
          'packageUris':self._package_uris, 
          'pythonModule':self._training_python_module, 
          'region':self._region, 
          'args':self._training_args}}
        if self._runtime_version:
            training_request['trainingInput']['runtimeVersion'] = self._runtime_version
        if self._python_version:
            training_request['trainingInput']['pythonVersion'] = self._python_version
        if self._job_dir:
            training_request['trainingInput']['jobDir'] = self._job_dir
        if self._scale_tier is not None:
            if self._scale_tier.upper() == 'CUSTOM':
                training_request['trainingInput']['masterType'] = self._master_type
        if self._mode == 'DRY_RUN':
            self.log.info('In dry_run mode.')
            self.log.info('MLEngine Training job request is: %s', training_request)
            return
        hook = MLEngineHook(gcp_conn_id=(self._gcp_conn_id),
          delegate_to=(self._delegate_to))

        def check_existing_job(existing_job):
            return existing_job.get('trainingInput', None) == training_request['trainingInput']

        try:
            finished_training_job = hook.create_job(self._project_id, training_request, check_existing_job)
        except HttpError:
            raise

        if finished_training_job['state'] != 'SUCCEEDED':
            self.log.error('MLEngine training job failed: %s', str(finished_training_job))
            raise RuntimeError(finished_training_job['errorMessage'])