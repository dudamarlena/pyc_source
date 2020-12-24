# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_container_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 13157 bytes
import os, subprocess, tempfile
from airflow import AirflowException
from airflow.contrib.hooks.gcp_container_hook import GKEClusterHook
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class GKEClusterDeleteOperator(BaseOperator):
    """GKEClusterDeleteOperator"""
    template_fields = [
     'project_id', 'gcp_conn_id', 'name', 'location', 'api_version']

    @apply_defaults
    def __init__(self, project_id, name, location, gcp_conn_id='google_cloud_default', api_version='v2', *args, **kwargs):
        (super(GKEClusterDeleteOperator, self).__init__)(*args, **kwargs)
        self.project_id = project_id
        self.gcp_conn_id = gcp_conn_id
        self.location = location
        self.api_version = api_version
        self.name = name

    def _check_input(self):
        if not all([self.project_id, self.name, self.location]):
            self.log.error('One of (project_id, name, location) is missing or incorrect')
            raise AirflowException('Operator has incorrect or missing input.')

    def execute(self, context):
        self._check_input()
        hook = GKEClusterHook(gcp_conn_id=(self.gcp_conn_id), location=(self.location))
        delete_result = hook.delete_cluster(name=(self.name), project_id=(self.project_id))
        return delete_result


class GKEClusterCreateOperator(BaseOperator):
    """GKEClusterCreateOperator"""
    template_fields = [
     'project_id', 'gcp_conn_id', 'location', 'api_version', 'body']

    @apply_defaults
    def __init__(self, project_id, location, body=None, gcp_conn_id='google_cloud_default', api_version='v2', *args, **kwargs):
        (super(GKEClusterCreateOperator, self).__init__)(*args, **kwargs)
        if body is None:
            body = {}
        self.project_id = project_id
        self.gcp_conn_id = gcp_conn_id
        self.location = location
        self.api_version = api_version
        self.body = body

    def _check_input(self):
        if all([self.project_id, self.location, self.body]):
            if isinstance(self.body, dict):
                if 'name' in self.body:
                    if 'initial_node_count' in self.body:
                        return
            if self.body.name:
                if self.body.initial_node_count:
                    return
        self.log.error("One of (project_id, location, body, body['name'], body['initial_node_count']) is missing or incorrect")
        raise AirflowException('Operator has incorrect or missing input.')

    def execute(self, context):
        self._check_input()
        hook = GKEClusterHook(gcp_conn_id=(self.gcp_conn_id), location=(self.location))
        create_op = hook.create_cluster(cluster=(self.body), project_id=(self.project_id))
        return create_op


KUBE_CONFIG_ENV_VAR = 'KUBECONFIG'
G_APP_CRED = 'GOOGLE_APPLICATION_CREDENTIALS'

class GKEPodOperator(KubernetesPodOperator):
    """GKEPodOperator"""
    template_fields = ('project_id', 'location', 'cluster_name') + KubernetesPodOperator.template_fields

    @apply_defaults
    def __init__(self, project_id, location, cluster_name, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(GKEPodOperator, self).__init__)(*args, **kwargs)
        self.project_id = project_id
        self.location = location
        self.cluster_name = cluster_name
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        key_file = None
        if self.gcp_conn_id:
            from airflow.hooks.base_hook import BaseHook
            extras = BaseHook.get_connection(self.gcp_conn_id).extra_dejson
            key_file = self._set_env_from_extras(extras=extras)
        with tempfile.NamedTemporaryFile() as (conf_file):
            os.environ[KUBE_CONFIG_ENV_VAR] = conf_file.name
            subprocess.check_call([
             'gcloud', 'container', 'clusters', 'get-credentials',
             self.cluster_name,
             '--zone', self.location,
             '--project', self.project_id])
            if key_file:
                key_file.close()
            self.config_file = os.environ[KUBE_CONFIG_ENV_VAR]
            super(GKEPodOperator, self).execute(context)

    def _set_env_from_extras(self, extras):
        """
        Sets the environment variable `GOOGLE_APPLICATION_CREDENTIALS` with either:

        - The path to the keyfile from the specified connection id
        - A generated file's path if the user specified JSON in the connection id. The
            file is assumed to be deleted after the process dies due to how mkstemp()
            works.

        The environment variable is used inside the gcloud command to determine correct
        service account to use.
        """
        key_path = self._get_field(extras, 'key_path', False)
        keyfile_json_str = self._get_field(extras, 'keyfile_dict', False)
        if not key_path:
            if not keyfile_json_str:
                self.log.info('Using gcloud with application default credentials.')
        else:
            if key_path:
                os.environ[G_APP_CRED] = key_path
            else:
                service_key = tempfile.NamedTemporaryFile(delete=False)
                service_key.write(keyfile_json_str.encode('utf-8'))
                os.environ[G_APP_CRED] = service_key.name
                return service_key

    def _get_field(self, extras, field, default=None):
        """
        Fetches a field from extras, and returns it. This is some Airflow
        magic. The google_cloud_platform hook type adds custom UI elements
        to the hook page, which allow admins to specify service_account,
        key_path, etc. They get formatted as shown below.
        """
        long_f = 'extra__google_cloud_platform__{}'.format(field)
        if long_f in extras:
            return extras[long_f]
        else:
            self.log.info('Field %s not found in extras.', field)
            return default