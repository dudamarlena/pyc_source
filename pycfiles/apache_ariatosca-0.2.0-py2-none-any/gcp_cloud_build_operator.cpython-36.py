# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_cloud_build_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6628 bytes
__doc__ = 'Operators that integrat with Google Cloud Build service.'
from copy import deepcopy
import re
from urllib.parse import urlparse, unquote
import six
from airflow import AirflowException
from airflow.contrib.hooks.gcp_cloud_build_hook import CloudBuildHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
REGEX_REPO_PATH = re.compile('^/p/(?P<project_id>[^/]+)/r/(?P<repo_name>[^/]+)')

class BuildProcessor:
    """BuildProcessor"""

    def __init__(self, body):
        self.body = deepcopy(body)

    def _verify_source(self):
        is_storage = 'storageSource' in self.body['source']
        is_repo = 'repoSource' in self.body['source']
        sources_count = sum([is_storage, is_repo])
        if sources_count != 1:
            raise AirflowException('The source could not be determined. Please choose one data source from: storageSource and repoSource.')

    def _reformat_source(self):
        self._reformat_repo_source()
        self._reformat_storage_source()

    def _reformat_repo_source(self):
        if 'repoSource' not in self.body['source']:
            return
        source = self.body['source']['repoSource']
        if not isinstance(source, six.string_types):
            return
        self.body['source']['repoSource'] = self._convert_repo_url_to_dict(source)

    def _reformat_storage_source(self):
        if 'storageSource' not in self.body['source']:
            return
        source = self.body['source']['storageSource']
        if not isinstance(source, six.string_types):
            return
        self.body['source']['storageSource'] = self._convert_storage_url_to_dict(source)

    def process_body(self):
        """
        Processes the body passed in the constructor

        :return: the body.
        :type: dict
        """
        self._verify_source()
        self._reformat_source()
        return self.body

    @staticmethod
    def _convert_repo_url_to_dict(source):
        """
        Convert url to repository in Google Cloud Source to a format supported by the API

        Example valid input:

        .. code-block:: none

            https://source.developers.google.com/p/airflow-project/r/airflow-repo#branch-name

        """
        url_parts = urlparse(source)
        match = REGEX_REPO_PATH.search(url_parts.path)
        if url_parts.scheme != 'https' or url_parts.hostname != 'source.developers.google.com' or not match:
            raise AirflowException('Invalid URL. You must pass the URL in the format: https://source.developers.google.com/p/airflow-project/r/airflow-repo#branch-name')
        project_id = unquote(match.group('project_id'))
        repo_name = unquote(match.group('repo_name'))
        source_dict = {'projectId':project_id, 
         'repoName':repo_name,  'branchName':'master'}
        if url_parts.fragment:
            source_dict['branchName'] = url_parts.fragment
        return source_dict

    @staticmethod
    def _convert_storage_url_to_dict(storage_url):
        """
        Convert url to object in Google Cloud Storage to a format supported by the API

        Example valid input:

        .. code-block:: none

            gs://bucket-name/object-name.tar.gz

        """
        url_parts = urlparse(storage_url)
        if url_parts.scheme != 'gs' or not url_parts.hostname or not url_parts.path or url_parts.path == '/':
            raise AirflowException('Invalid URL. You must pass the URL in the format: gs://bucket-name/object-name.tar.gz#24565443')
        source_dict = {'bucket':url_parts.hostname, 
         'object':url_parts.path[1:]}
        if url_parts.fragment:
            source_dict['generation'] = url_parts.fragment
        return source_dict


class CloudBuildCreateBuildOperator(BaseOperator):
    """CloudBuildCreateBuildOperator"""
    template_fields = ('body', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, body, project_id=None, gcp_conn_id='google_cloud_default', api_version='v1', *args, **kwargs):
        (super(CloudBuildCreateBuildOperator, self).__init__)(*args, **kwargs)
        self.body = body
        self.project_id = project_id
        self.gcp_conn_id = gcp_conn_id
        self.api_version = api_version
        self._validate_inputs()

    def _validate_inputs(self):
        if not self.body:
            raise AirflowException("The required parameter 'body' is missing")

    def execute(self, context):
        hook = CloudBuildHook(gcp_conn_id=(self.gcp_conn_id), api_version=(self.api_version))
        body = BuildProcessor(body=(self.body)).process_body()
        return hook.create_build(body=body, project_id=(self.project_id))