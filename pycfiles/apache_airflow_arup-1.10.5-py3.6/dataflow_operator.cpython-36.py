# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/dataflow_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 16940 bytes
import os, re, uuid, copy
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.contrib.hooks.gcp_dataflow_hook import DataFlowHook
from airflow.models import BaseOperator
from airflow.version import version
from airflow.utils.decorators import apply_defaults

class DataFlowJavaOperator(BaseOperator):
    __doc__ = "\n    Start a Java Cloud DataFlow batch job. The parameters of the operation\n    will be passed to the job.\n\n    **Example**: ::\n\n        default_args = {\n            'owner': 'airflow',\n            'depends_on_past': False,\n            'start_date':\n                (2016, 8, 1),\n            'email': ['alex@vanboxel.be'],\n            'email_on_failure': False,\n            'email_on_retry': False,\n            'retries': 1,\n            'retry_delay': timedelta(minutes=30),\n            'dataflow_default_options': {\n                'project': 'my-gcp-project',\n                'zone': 'us-central1-f',\n                'stagingLocation': 'gs://bucket/tmp/dataflow/staging/',\n            }\n        }\n\n        dag = DAG('test-dag', default_args=default_args)\n\n        task = DataFlowJavaOperator(\n            gcp_conn_id='gcp_default',\n            task_id='normalize-cal',\n            jar='{{var.value.gcp_dataflow_base}}pipeline-ingress-cal-normalize-1.0.jar',\n            options={\n                'autoscalingAlgorithm': 'BASIC',\n                'maxNumWorkers': '50',\n                'start': '{{ds}}',\n                'partitionType': 'DAY'\n\n            },\n            dag=dag)\n\n    .. seealso::\n        For more detail on job submission have a look at the reference:\n        https://cloud.google.com/dataflow/pipelines/specifying-exec-params\n\n    :param jar: The reference to a self executing DataFlow jar (templated).\n    :type jar: str\n    :param job_name: The 'jobName' to use when executing the DataFlow job\n        (templated). This ends up being set in the pipeline options, so any entry\n        with key ``'jobName'`` in ``options`` will be overwritten.\n    :type job_name: str\n    :param dataflow_default_options: Map of default job options.\n    :type dataflow_default_options: dict\n    :param options: Map of job specific options.\n    :type options: dict\n    :param gcp_conn_id: The connection ID to use connecting to Google Cloud\n        Platform.\n    :type gcp_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide delegation enabled.\n    :type delegate_to: str\n    :param poll_sleep: The time in seconds to sleep between polling Google\n        Cloud Platform for the dataflow job status while the job is in the\n        JOB_STATE_RUNNING state.\n    :type poll_sleep: int\n    :param job_class: The name of the dataflow job class to be executed, it\n        is often not the main class configured in the dataflow jar file.\n    :type job_class: str\n\n    ``jar``, ``options``, and ``job_name`` are templated so you can use variables in them.\n\n    Note that both\n    ``dataflow_default_options`` and ``options`` will be merged to specify pipeline\n    execution parameter, and ``dataflow_default_options`` is expected to save\n    high-level options, for instances, project and zone information, which\n    apply to all dataflow operators in the DAG.\n\n    It's a good practice to define dataflow_* parameters in the default_args of the dag\n    like the project, zone and staging location.\n\n    .. code-block:: python\n\n       default_args = {\n           'dataflow_default_options': {\n               'project': 'my-gcp-project',\n               'zone': 'europe-west1-d',\n               'stagingLocation': 'gs://my-staging-bucket/staging/'\n           }\n       }\n\n    You need to pass the path to your dataflow as a file reference with the ``jar``\n    parameter, the jar needs to be a self executing jar (see documentation here:\n    https://beam.apache.org/documentation/runners/dataflow/#self-executing-jar).\n    Use ``options`` to pass on options to your job.\n\n    .. code-block:: python\n\n       t1 = DataFlowJavaOperator(\n           task_id='datapflow_example',\n           jar='{{var.value.gcp_dataflow_base}}pipeline/build/libs/pipeline-example-1.0.jar',\n           options={\n               'autoscalingAlgorithm': 'BASIC',\n               'maxNumWorkers': '50',\n               'start': '{{ds}}',\n               'partitionType': 'DAY',\n               'labels': {'foo' : 'bar'}\n           },\n           gcp_conn_id='gcp-airflow-service-account',\n           dag=my-dag)\n\n    "
    template_fields = ['options', 'jar', 'job_name']
    ui_color = '#0273d4'

    @apply_defaults
    def __init__(self, jar, job_name='{{task.task_id}}', dataflow_default_options=None, options=None, gcp_conn_id='google_cloud_default', delegate_to=None, poll_sleep=10, job_class=None, *args, **kwargs):
        (super(DataFlowJavaOperator, self).__init__)(*args, **kwargs)
        dataflow_default_options = dataflow_default_options or {}
        options = options or {}
        options.setdefault('labels', {}).update({'airflow-version': 'v' + version.replace('.', '-').replace('+', '-')})
        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to
        self.jar = jar
        self.job_name = job_name
        self.dataflow_default_options = dataflow_default_options
        self.options = options
        self.poll_sleep = poll_sleep
        self.job_class = job_class

    def execute(self, context):
        bucket_helper = GoogleCloudBucketHelper(self.gcp_conn_id, self.delegate_to)
        self.jar = bucket_helper.google_cloud_to_local(self.jar)
        hook = DataFlowHook(gcp_conn_id=(self.gcp_conn_id), delegate_to=(self.delegate_to),
          poll_sleep=(self.poll_sleep))
        dataflow_options = copy.copy(self.dataflow_default_options)
        dataflow_options.update(self.options)
        hook.start_java_dataflow(self.job_name, dataflow_options, self.jar, self.job_class)


class DataflowTemplateOperator(BaseOperator):
    __doc__ = '\n    Start a Templated Cloud DataFlow batch job. The parameters of the operation\n    will be passed to the job.\n\n    :param template: The reference to the DataFlow template.\n    :type template: str\n    :param job_name: The \'jobName\' to use when executing the DataFlow template\n        (templated).\n    :param dataflow_default_options: Map of default job environment options.\n    :type dataflow_default_options: dict\n    :param parameters: Map of job specific parameters for the template.\n    :type parameters: dict\n    :param gcp_conn_id: The connection ID to use connecting to Google Cloud\n        Platform.\n    :type gcp_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide delegation enabled.\n    :type delegate_to: str\n    :param poll_sleep: The time in seconds to sleep between polling Google\n        Cloud Platform for the dataflow job status while the job is in the\n        JOB_STATE_RUNNING state.\n    :type poll_sleep: int\n\n    It\'s a good practice to define dataflow_* parameters in the default_args of the dag\n    like the project, zone and staging location.\n\n    .. seealso::\n        https://cloud.google.com/dataflow/docs/reference/rest/v1b3/LaunchTemplateParameters\n        https://cloud.google.com/dataflow/docs/reference/rest/v1b3/RuntimeEnvironment\n\n    .. code-block:: python\n\n       default_args = {\n           \'dataflow_default_options\': {\n               \'project\': \'my-gcp-project\',\n               \'region\': \'europe-west1\',\n               \'zone\': \'europe-west1-d\',\n               \'tempLocation\': \'gs://my-staging-bucket/staging/\',\n               }\n           }\n       }\n\n    You need to pass the path to your dataflow template as a file reference with the\n    ``template`` parameter. Use ``parameters`` to pass on parameters to your job.\n    Use ``environment`` to pass on runtime environment variables to your job.\n\n    .. code-block:: python\n\n       t1 = DataflowTemplateOperator(\n           task_id=\'datapflow_example\',\n           template=\'{{var.value.gcp_dataflow_base}}\',\n           parameters={\n               \'inputFile\': "gs://bucket/input/my_input.txt",\n               \'outputFile\': "gs://bucket/output/my_output.txt"\n           },\n           gcp_conn_id=\'gcp-airflow-service-account\',\n           dag=my-dag)\n\n    ``template``, ``dataflow_default_options``, ``parameters``, and ``job_name`` are\n    templated so you can use variables in them.\n\n    Note that ``dataflow_default_options`` is expected to save high-level options\n    for project information, which apply to all dataflow operators in the DAG.\n\n        .. seealso::\n            https://cloud.google.com/dataflow/docs/reference/rest/v1b3\n            /LaunchTemplateParameters\n            https://cloud.google.com/dataflow/docs/reference/rest/v1b3/RuntimeEnvironment\n            For more detail on job template execution have a look at the reference:\n            https://cloud.google.com/dataflow/docs/templates/executing-templates\n    '
    template_fields = ['parameters', 'dataflow_default_options', 'template', 'job_name']
    ui_color = '#0273d4'

    @apply_defaults
    def __init__(self, template, job_name='{{task.task_id}}', dataflow_default_options=None, parameters=None, gcp_conn_id='google_cloud_default', delegate_to=None, poll_sleep=10, *args, **kwargs):
        (super(DataflowTemplateOperator, self).__init__)(*args, **kwargs)
        dataflow_default_options = dataflow_default_options or {}
        parameters = parameters or {}
        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to
        self.dataflow_default_options = dataflow_default_options
        self.poll_sleep = poll_sleep
        self.template = template
        self.job_name = job_name
        self.parameters = parameters

    def execute(self, context):
        hook = DataFlowHook(gcp_conn_id=(self.gcp_conn_id), delegate_to=(self.delegate_to),
          poll_sleep=(self.poll_sleep))
        hook.start_template_dataflow(self.job_name, self.dataflow_default_options, self.parameters, self.template)


class DataFlowPythonOperator(BaseOperator):
    __doc__ = '\n    Launching Cloud Dataflow jobs written in python. Note that both\n    dataflow_default_options and options will be merged to specify pipeline\n    execution parameter, and dataflow_default_options is expected to save\n    high-level options, for instances, project and zone information, which\n    apply to all dataflow operators in the DAG.\n\n    .. seealso::\n        For more detail on job submission have a look at the reference:\n        https://cloud.google.com/dataflow/pipelines/specifying-exec-params\n\n    :param py_file: Reference to the python dataflow pipeline file.py, e.g.,\n        /some/local/file/path/to/your/python/pipeline/file. (templated)\n    :type py_file: str\n    :param job_name: The \'job_name\' to use when executing the DataFlow job\n        (templated). This ends up being set in the pipeline options, so any entry\n        with key ``\'jobName\'`` or ``\'job_name\'`` in ``options`` will be overwritten.\n    :type job_name: str\n    :param py_options: Additional python options, e.g., ["-m", "-v"].\n    :type pyt_options: list[str]\n    :param dataflow_default_options: Map of default job options.\n    :type dataflow_default_options: dict\n    :param options: Map of job specific options.\n    :type options: dict\n    :param gcp_conn_id: The connection ID to use connecting to Google Cloud\n        Platform.\n    :type gcp_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide  delegation enabled.\n    :type delegate_to: str\n    :param poll_sleep: The time in seconds to sleep between polling Google\n        Cloud Platform for the dataflow job status while the job is in the\n        JOB_STATE_RUNNING state.\n    :type poll_sleep: int\n    '
    template_fields = ['options', 'dataflow_default_options', 'job_name', 'py_file']

    @apply_defaults
    def __init__(self, py_file, job_name='{{task.task_id}}', py_options=None, dataflow_default_options=None, options=None, gcp_conn_id='google_cloud_default', delegate_to=None, poll_sleep=10, *args, **kwargs):
        (super(DataFlowPythonOperator, self).__init__)(*args, **kwargs)
        self.py_file = py_file
        self.job_name = job_name
        self.py_options = py_options or []
        self.dataflow_default_options = dataflow_default_options or {}
        self.options = options or {}
        self.options.setdefault('labels', {}).update({'airflow-version': 'v' + version.replace('.', '-').replace('+', '-')})
        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to
        self.poll_sleep = poll_sleep

    def execute(self, context):
        """Execute the python dataflow job."""
        bucket_helper = GoogleCloudBucketHelper(self.gcp_conn_id, self.delegate_to)
        self.py_file = bucket_helper.google_cloud_to_local(self.py_file)
        hook = DataFlowHook(gcp_conn_id=(self.gcp_conn_id), delegate_to=(self.delegate_to),
          poll_sleep=(self.poll_sleep))
        dataflow_options = self.dataflow_default_options.copy()
        dataflow_options.update(self.options)
        camel_to_snake = lambda name: re.sub('[A-Z]', lambda x: '_' + x.group(0).lower(), name)
        formatted_options = {camel_to_snake(key):dataflow_options[key] for key in dataflow_options}
        hook.start_python_dataflow(self.job_name, formatted_options, self.py_file, self.py_options)


class GoogleCloudBucketHelper(object):
    __doc__ = 'GoogleCloudStorageHook helper class to download GCS object.'
    GCS_PREFIX_LENGTH = 5

    def __init__(self, gcp_conn_id='google_cloud_default', delegate_to=None):
        self._gcs_hook = GoogleCloudStorageHook(gcp_conn_id, delegate_to)

    def google_cloud_to_local(self, file_name):
        """
        Checks whether the file specified by file_name is stored in Google Cloud
        Storage (GCS), if so, downloads the file and saves it locally. The full
        path of the saved file will be returned. Otherwise the local file_name
        will be returned immediately.

        :param file_name: The full path of input file.
        :type file_name: str
        :return: The full path of local file.
        :rtype: str
        """
        if not file_name.startswith('gs://'):
            return file_name
        else:
            path_components = file_name[self.GCS_PREFIX_LENGTH:].split('/')
            if len(path_components) < 2:
                raise Exception('Invalid Google Cloud Storage (GCS) object path: {}'.format(file_name))
            bucket_id = path_components[0]
            object_id = '/'.join(path_components[1:])
            local_file = '/tmp/dataflow{}-{}'.format(str(uuid.uuid4())[:8], path_components[(-1)])
            self._gcs_hook.download(bucket_id, object_id, local_file)
            if os.stat(local_file).st_size > 0:
                return local_file
        raise Exception('Failed to download Google Cloud Storage (GCS) object: {}'.format(file_name))