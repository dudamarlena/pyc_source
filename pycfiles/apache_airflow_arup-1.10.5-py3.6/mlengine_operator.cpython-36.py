# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = '\n    Start a Google Cloud ML Engine prediction job.\n\n    NOTE: For model origin, users should consider exactly one from the\n    three options below:\n\n    1. Populate ``uri`` field only, which should be a GCS location that\n       points to a tensorflow savedModel directory.\n    2. Populate ``model_name`` field only, which refers to an existing\n       model, and the default version of the model will be used.\n    3. Populate both ``model_name`` and ``version_name`` fields, which\n       refers to a specific version of a specific model.\n\n    In options 2 and 3, both model and version name should contain the\n    minimal identifier. For instance, call::\n\n        MLEngineBatchPredictionOperator(\n            ...,\n            model_name=\'my_model\',\n            version_name=\'my_version\',\n            ...)\n\n    if the desired model version is\n    ``projects/my_project/models/my_model/versions/my_version``.\n\n    See https://cloud.google.com/ml-engine/reference/rest/v1/projects.jobs\n    for further documentation on the parameters.\n\n    :param project_id: The Google Cloud project name where the\n        prediction job is submitted. (templated)\n    :type project_id: str\n\n    :param job_id: A unique id for the prediction job on Google Cloud\n        ML Engine. (templated)\n    :type job_id: str\n\n    :param data_format: The format of the input data.\n        It will default to \'DATA_FORMAT_UNSPECIFIED\' if is not provided\n        or is not one of ["TEXT", "TF_RECORD", "TF_RECORD_GZIP"].\n    :type data_format: str\n\n    :param input_paths: A list of GCS paths of input data for batch\n        prediction. Accepting wildcard operator ``*``, but only at the end. (templated)\n    :type input_paths: list[str]\n\n    :param output_path: The GCS path where the prediction results are\n        written to. (templated)\n    :type output_path: str\n\n    :param region: The Google Compute Engine region to run the\n        prediction job in. (templated)\n    :type region: str\n\n    :param model_name: The Google Cloud ML Engine model to use for prediction.\n        If version_name is not provided, the default version of this\n        model will be used.\n        Should not be None if version_name is provided.\n        Should be None if uri is provided. (templated)\n    :type model_name: str\n\n    :param version_name: The Google Cloud ML Engine model version to use for\n        prediction.\n        Should be None if uri is provided. (templated)\n    :type version_name: str\n\n    :param uri: The GCS path of the saved model to use for prediction.\n        Should be None if model_name is provided.\n        It should be a GCS path pointing to a tensorflow SavedModel. (templated)\n    :type uri: str\n\n    :param max_worker_count: The maximum number of workers to be used\n        for parallel processing. Defaults to 10 if not specified.\n    :type max_worker_count: int\n\n    :param runtime_version: The Google Cloud ML Engine runtime version to use\n        for batch prediction.\n    :type runtime_version: str\n\n    :param signature_name: The name of the signature defined in the SavedModel\n        to use for this job.\n    :type signature_name: str\n\n    :param gcp_conn_id: The connection ID used for connection to Google\n        Cloud Platform.\n    :type gcp_conn_id: str\n\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must\n        have domain-wide delegation enabled.\n    :type delegate_to: str\n\n    :raises: ``ValueError``: if a unique model/version origin cannot be\n        determined.\n    '
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
    __doc__ = '\n    Operator for managing a Google Cloud ML Engine model.\n\n    :param project_id: The Google Cloud project name to which MLEngine\n        model belongs. (templated)\n    :type project_id: str\n    :param model: A dictionary containing the information about the model.\n        If the `operation` is `create`, then the `model` parameter should\n        contain all the information about this model such as `name`.\n\n        If the `operation` is `get`, the `model` parameter\n        should contain the `name` of the model.\n    :type model: dict\n    :param operation: The operation to perform. Available operations are:\n\n        * ``create``: Creates a new model as provided by the `model` parameter.\n        * ``get``: Gets a particular model where the name is specified in `model`.\n    :type operation: str\n    :param gcp_conn_id: The connection ID to use when fetching connection info.\n    :type gcp_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide delegation enabled.\n    :type delegate_to: str\n    '
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
    __doc__ = '\n    Operator for managing a Google Cloud ML Engine version.\n\n    :param project_id: The Google Cloud project name to which MLEngine\n        model belongs.\n    :type project_id: str\n\n    :param model_name: The name of the Google Cloud ML Engine model that the version\n        belongs to. (templated)\n    :type model_name: str\n\n    :param version_name: A name to use for the version being operated upon.\n        If not None and the `version` argument is None or does not have a value for\n        the `name` key, then this will be populated in the payload for the\n        `name` key. (templated)\n    :type version_name: str\n\n    :param version: A dictionary containing the information about the version.\n        If the `operation` is `create`, `version` should contain all the\n        information about this version such as name, and deploymentUrl.\n        If the `operation` is `get` or `delete`, the `version` parameter\n        should contain the `name` of the version.\n        If it is None, the only `operation` possible would be `list`. (templated)\n    :type version: dict\n\n    :param operation: The operation to perform. Available operations are:\n\n        *   ``create``: Creates a new version in the model specified by `model_name`,\n            in which case the `version` parameter should contain all the\n            information to create that version\n            (e.g. `name`, `deploymentUrl`).\n\n        *   ``get``: Gets full information of a particular version in the model\n            specified by `model_name`.\n            The name of the version should be specified in the `version`\n            parameter.\n\n        *   ``list``: Lists all available versions of the model specified\n            by `model_name`.\n\n        *   ``delete``: Deletes the version specified in `version` parameter from the\n            model specified by `model_name`).\n            The name of the version should be specified in the `version`\n            parameter.\n    :type operation: str\n\n    :param gcp_conn_id: The connection ID to use when fetching connection info.\n    :type gcp_conn_id: str\n\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide delegation enabled.\n    :type delegate_to: str\n    '
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
    __doc__ = "\n    Operator for launching a MLEngine training job.\n\n    :param project_id: The Google Cloud project name within which MLEngine\n        training job should run (templated).\n    :type project_id: str\n\n    :param job_id: A unique templated id for the submitted Google MLEngine\n        training job. (templated)\n    :type job_id: str\n\n    :param package_uris: A list of package locations for MLEngine training job,\n        which should include the main training program + any additional\n        dependencies. (templated)\n    :type package_uris: str\n\n    :param training_python_module: The Python module name to run within MLEngine\n        training job after installing 'package_uris' packages. (templated)\n    :type training_python_module: str\n\n    :param training_args: A list of templated command line arguments to pass to\n        the MLEngine training program. (templated)\n    :type training_args: str\n\n    :param region: The Google Compute Engine region to run the MLEngine training\n        job in (templated).\n    :type region: str\n\n    :param scale_tier: Resource tier for MLEngine training job. (templated)\n    :type scale_tier: str\n\n    :param master_type: Cloud ML Engine machine name.\n        Must be set when scale_tier is CUSTOM. (templated)\n    :type master_type: str\n\n    :param runtime_version: The Google Cloud ML runtime version to use for\n        training. (templated)\n    :type runtime_version: str\n\n    :param python_version: The version of Python used in training. (templated)\n    :type python_version: str\n\n    :param job_dir: A Google Cloud Storage path in which to store training\n        outputs and other data needed for training. (templated)\n    :type job_dir: str\n\n    :param gcp_conn_id: The connection ID to use when fetching connection info.\n    :type gcp_conn_id: str\n\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide delegation enabled.\n    :type delegate_to: str\n\n    :param mode: Can be one of 'DRY_RUN'/'CLOUD'. In 'DRY_RUN' mode, no real\n        training job will be launched, but the MLEngine training job request\n        will be printed out. In 'CLOUD' mode, a real MLEngine training job\n        creation request will be issued.\n    :type mode: str\n    "
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