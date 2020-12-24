# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """DataFlowJavaOperator"""
    template_fields = [
     'options', 'jar', 'job_name']
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
    """DataflowTemplateOperator"""
    template_fields = [
     'parameters', 'dataflow_default_options', 'template', 'job_name']
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
    """DataFlowPythonOperator"""
    template_fields = [
     'options', 'dataflow_default_options', 'job_name', 'py_file']

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
    """GoogleCloudBucketHelper"""
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