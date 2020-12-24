# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/gcp_cloud_build_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4813 bytes
"""Hook for Google Cloud Build service"""
import time
from googleapiclient.discovery import build
from airflow import AirflowException
from airflow.contrib.hooks.gcp_api_base_hook import GoogleCloudBaseHook
TIME_TO_SLEEP_IN_SECONDS = 5

class CloudBuildHook(GoogleCloudBaseHook):
    __doc__ = '\n    Hook for the Google Cloud Build APIs.\n\n    All the methods in the hook where project_id is used must be called with\n    keyword arguments rather than positional.\n\n    :param api_version: API version used (for example v1 or v1beta1).\n    :type api_version: str\n    :param gcp_conn_id: The connection ID to use when fetching connection info.\n    :type gcp_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide delegation enabled.\n    :type delegate_to: str\n    '
    _conn = None

    def __init__(self, api_version='v1', gcp_conn_id='google_cloud_default', delegate_to=None):
        super(CloudBuildHook, self).__init__(gcp_conn_id, delegate_to)
        self.api_version = api_version

    def get_conn(self):
        """
        Retrieves the connection to Cloud Functions.

        :return: Google Cloud Build services object.
        """
        if not self._conn:
            http_authorized = self._authorize()
            self._conn = build('cloudbuild', (self.api_version), http=http_authorized, cache_discovery=False)
        return self._conn

    @GoogleCloudBaseHook.fallback_to_default_project_id
    def create_build(self, body, project_id=None):
        """
        Starts a build with the specified configuration.

        :param body: The request body.
            See: https://cloud.google.com/cloud-build/docs/api/reference/rest/Shared.Types/Build
        :type body: dict
        :param project_id: Optional, Google Cloud Project project_id where the function belongs.
            If set to None or missing, the default project_id from the GCP connection is used.
        :type project_id: str
        :return: None
        """
        service = self.get_conn()
        response = service.projects().builds().create(projectId=project_id,
          body=body).execute(num_retries=(self.num_retries))
        operation_name = response['name']
        self._wait_for_operation_to_complete(operation_name=operation_name)
        build_id = response['metadata']['build']['id']
        result = service.projects().builds().get(projectId=project_id,
          id=build_id).execute(num_retries=(self.num_retries))
        return result

    def _wait_for_operation_to_complete(self, operation_name):
        """
        Waits for the named operation to complete - checks status of the
        asynchronous call.

        :param operation_name: The name of the operation.
        :type operation_name: str
        :return: The response returned by the operation.
        :rtype: dict
        :exception: AirflowException in case error is returned.
        """
        service = self.get_conn()
        while True:
            operation_response = service.operations().get(name=operation_name).execute(num_retries=(self.num_retries))
            if operation_response.get('done'):
                response = operation_response.get('response')
                error = operation_response.get('error')
                if error:
                    raise AirflowException(str(error))
                return response
            time.sleep(TIME_TO_SLEEP_IN_SECONDS)