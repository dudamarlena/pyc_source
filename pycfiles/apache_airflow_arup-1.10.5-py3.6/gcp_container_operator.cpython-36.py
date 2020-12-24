# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = "\n    Deletes the cluster, including the Kubernetes endpoint and all worker nodes.\n\n    To delete a certain cluster, you must specify the ``project_id``, the ``name``\n    of the cluster, the ``location`` that the cluster is in, and the ``task_id``.\n\n    **Operator Creation**: ::\n\n        operator = GKEClusterDeleteOperator(\n                    task_id='cluster_delete',\n                    project_id='my-project',\n                    location='cluster-location'\n                    name='cluster-name')\n\n    .. seealso::\n        For more detail about deleting clusters have a look at the reference:\n        https://google-cloud-python.readthedocs.io/en/latest/container/gapic/v1/api.html#google.cloud.container_v1.ClusterManagerClient.delete_cluster\n\n    :param project_id: The Google Developers Console [project ID or project number]\n    :type project_id: str\n    :param name: The name of the resource to delete, in this case cluster name\n    :type name: str\n    :param location: The name of the Google Compute Engine zone in which the cluster\n        resides.\n    :type location: str\n    :param gcp_conn_id: The connection ID to use connecting to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :param api_version: The api version to use\n    :type api_version: str\n    "
    template_fields = ['project_id', 'gcp_conn_id', 'name', 'location', 'api_version']

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
    __doc__ = "\n    Create a Google Kubernetes Engine Cluster of specified dimensions\n    The operator will wait until the cluster is created.\n\n    The **minimum** required to define a cluster to create is:\n\n    ``dict()`` ::\n        cluster_def = {'name': 'my-cluster-name',\n                       'initial_node_count': 1}\n\n    or\n\n    ``Cluster`` proto ::\n        from google.cloud.container_v1.types import Cluster\n\n        cluster_def = Cluster(name='my-cluster-name', initial_node_count=1)\n\n    **Operator Creation**: ::\n\n        operator = GKEClusterCreateOperator(\n                    task_id='cluster_create',\n                    project_id='my-project',\n                    location='my-location'\n                    body=cluster_def)\n\n    .. seealso::\n        For more detail on about creating clusters have a look at the reference:\n        :class:`google.cloud.container_v1.types.Cluster`\n\n    :param project_id: The Google Developers Console [project ID or project number]\n    :type project_id: str\n    :param location: The name of the Google Compute Engine zone in which the cluster\n        resides.\n    :type location: str\n    :param body: The Cluster definition to create, can be protobuf or python dict, if\n        dict it must match protobuf message Cluster\n    :type body: dict or google.cloud.container_v1.types.Cluster\n    :param gcp_conn_id: The connection ID to use connecting to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :param api_version: The api version to use\n    :type api_version: str\n    "
    template_fields = ['project_id', 'gcp_conn_id', 'location', 'api_version', 'body']

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
    __doc__ = "\n    Executes a task in a Kubernetes pod in the specified Google Kubernetes\n    Engine cluster\n\n    This Operator assumes that the system has gcloud installed and either\n    has working default application credentials or has configured a\n    connection id with a service account.\n\n    The **minimum** required to define a cluster to create are the variables\n    ``task_id``, ``project_id``, ``location``, ``cluster_name``, ``name``,\n    ``namespace``, and ``image``\n\n    **Operator Creation**: ::\n\n        operator = GKEPodOperator(task_id='pod_op',\n                                  project_id='my-project',\n                                  location='us-central1-a',\n                                  cluster_name='my-cluster-name',\n                                  name='task-name',\n                                  namespace='default',\n                                  image='perl')\n\n    .. seealso::\n        For more detail about application authentication have a look at the reference:\n        https://cloud.google.com/docs/authentication/production#providing_credentials_to_your_application\n\n    :param project_id: The Google Developers Console project id\n    :type project_id: str\n    :param location: The name of the Google Kubernetes Engine zone in which the\n        cluster resides, e.g. 'us-central1-a'\n    :type location: str\n    :param cluster_name: The name of the Google Kubernetes Engine cluster the pod\n        should be spawned in\n    :type cluster_name: str\n    :param gcp_conn_id: The google cloud connection id to use. This allows for\n        users to specify a service account.\n    :type gcp_conn_id: str\n    "
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