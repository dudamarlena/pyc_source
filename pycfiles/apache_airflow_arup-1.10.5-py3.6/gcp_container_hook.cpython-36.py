# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/gcp_container_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 10871 bytes
import json, time
from airflow import AirflowException, version
from airflow.contrib.hooks.gcp_api_base_hook import GoogleCloudBaseHook
from google.api_core.exceptions import AlreadyExists, NotFound
from google.api_core.gapic_v1.method import DEFAULT
from google.cloud import container_v1, exceptions
from google.cloud.container_v1.gapic.enums import Operation
from google.cloud.container_v1.types import Cluster
from google.protobuf import json_format
from google.api_core.gapic_v1.client_info import ClientInfo
OPERATIONAL_POLL_INTERVAL = 15

class GKEClusterHook(GoogleCloudBaseHook):

    def __init__(self, gcp_conn_id='google_cloud_default', delegate_to=None, location=None):
        super(GKEClusterHook, self).__init__(gcp_conn_id=gcp_conn_id,
          delegate_to=delegate_to)
        self._client = None
        self.location = location

    def get_client(self):
        if self._client is None:
            credentials = self._get_credentials()
            client_info = ClientInfo(client_library_version=('airflow_v' + version.version))
            self._client = container_v1.ClusterManagerClient(credentials=credentials, client_info=client_info)
        return self._client

    @staticmethod
    def _dict_to_proto(py_dict, proto):
        """
        Converts a python dictionary to the proto supplied

        :param py_dict: The dictionary to convert
        :type py_dict: dict
        :param proto: The proto object to merge with dictionary
        :type proto: protobuf
        :return: A parsed python dictionary in provided proto format
        :raises:
            ParseError: On JSON parsing problems.
        """
        dict_json_str = json.dumps(py_dict)
        return json_format.Parse(dict_json_str, proto)

    def wait_for_operation(self, operation, project_id=None):
        """
        Given an operation, continuously fetches the status from Google Cloud until either
        completion or an error occurring

        :param operation: The Operation to wait for
        :type operation: google.cloud.container_V1.gapic.enums.Operation
        :param project_id: Google Cloud Platform project ID
        :type project_id: str
        :return: A new, updated operation fetched from Google Cloud
        """
        self.log.info('Waiting for OPERATION_NAME %s', operation.name)
        time.sleep(OPERATIONAL_POLL_INTERVAL)
        while operation.status != Operation.Status.DONE:
            if operation.status == Operation.Status.RUNNING or operation.status == Operation.Status.PENDING:
                time.sleep(OPERATIONAL_POLL_INTERVAL)
            else:
                raise exceptions.GoogleCloudError('Operation has failed with status: %s' % operation.status)
            operation = self.get_operation((operation.name), project_id=(project_id or self.project_id))

        return operation

    def get_operation(self, operation_name, project_id=None):
        """
        Fetches the operation from Google Cloud

        :param operation_name: Name of operation to fetch
        :type operation_name: str
        :param project_id: Google Cloud Platform project ID
        :type project_id: str
        :return: The new, updated operation from Google Cloud
        """
        return self.get_client().get_operation(project_id=(project_id or self.project_id), zone=(self.location),
          operation_id=operation_name)

    @staticmethod
    def _append_label(cluster_proto, key, val):
        """
        Append labels to provided Cluster Protobuf

        Labels must fit the regex ``[a-z]([-a-z0-9]*[a-z0-9])?`` (current
         airflow version string follows semantic versioning spec: x.y.z).

        :param cluster_proto: The proto to append resource_label airflow
            version to
        :type cluster_proto: google.cloud.container_v1.types.Cluster
        :param key: The key label
        :type key: str
        :param val:
        :type val: str
        :return: The cluster proto updated with new label
        """
        val = val.replace('.', '-').replace('+', '-')
        cluster_proto.resource_labels.update({key: val})
        return cluster_proto

    def delete_cluster(self, name, project_id=None, retry=DEFAULT, timeout=DEFAULT):
        """
        Deletes the cluster, including the Kubernetes endpoint and all
        worker nodes. Firewalls and routes that were configured during
        cluster creation are also deleted. Other Google Compute Engine
        resources that might be in use by the cluster (e.g. load balancer
        resources) will not be deleted if they weren’t present at the
        initial create time.

        :param name: The name of the cluster to delete
        :type name: str
        :param project_id: Google Cloud Platform project ID
        :type project_id: str
        :param retry: Retry object used to determine when/if to retry requests.
            If None is specified, requests will not be retried.
        :type retry: google.api_core.retry.Retry
        :param timeout: The amount of time, in seconds, to wait for the request to
            complete. Note that if retry is specified, the timeout applies to each
            individual attempt.
        :type timeout: float
        :return: The full url to the delete operation if successful, else None
        """
        self.log.info('Deleting (project_id=%s, zone=%s, cluster_id=%s)', self.project_id, self.location, name)
        try:
            op = self.get_client().delete_cluster(project_id=(project_id or self.project_id), zone=(self.location),
              cluster_id=name,
              retry=retry,
              timeout=timeout)
            op = self.wait_for_operation(op)
            return op.self_link
        except NotFound as error:
            self.log.info('Assuming Success: %s', error.message)

    def create_cluster(self, cluster, project_id=None, retry=DEFAULT, timeout=DEFAULT):
        """
        Creates a cluster, consisting of the specified number and type of Google Compute
        Engine instances.

        :param cluster: A Cluster protobuf or dict. If dict is provided, it must
            be of the same form as the protobuf message
            :class:`google.cloud.container_v1.types.Cluster`
        :type cluster: dict or google.cloud.container_v1.types.Cluster
        :param project_id: Google Cloud Platform project ID
        :type project_id: str
        :param retry: A retry object (``google.api_core.retry.Retry``) used to
            retry requests.
            If None is specified, requests will not be retried.
        :type retry: google.api_core.retry.Retry
        :param timeout: The amount of time, in seconds, to wait for the request to
            complete. Note that if retry is specified, the timeout applies to each
            individual attempt.
        :type timeout: float
        :return: The full url to the new, or existing, cluster
        :raises:
            ParseError: On JSON parsing problems when trying to convert dict
            AirflowException: cluster is not dict type nor Cluster proto type
        """
        if isinstance(cluster, dict):
            cluster_proto = Cluster()
            cluster = self._dict_to_proto(py_dict=cluster, proto=cluster_proto)
        else:
            if not isinstance(cluster, Cluster):
                raise AirflowException('cluster is not instance of Cluster proto or python dict')
        self._append_label(cluster, 'airflow-version', 'v' + version.version)
        self.log.info('Creating (project_id=%s, zone=%s, cluster_name=%s)', self.project_id, self.location, cluster.name)
        try:
            op = self.get_client().create_cluster(project_id=(project_id or self.project_id), zone=(self.location),
              cluster=cluster,
              retry=retry,
              timeout=timeout)
            op = self.wait_for_operation(op)
            return op.target_link
        except AlreadyExists as error:
            self.log.info('Assuming Success: %s', error.message)
            return self.get_cluster(name=(cluster.name)).self_link

    def get_cluster(self, name, project_id=None, retry=DEFAULT, timeout=DEFAULT):
        """
        Gets details of specified cluster

        :param name: The name of the cluster to retrieve
        :type name: str
        :param project_id: Google Cloud Platform project ID
        :type project_id: str
        :param retry: A retry object used to retry requests. If None is specified,
            requests will not be retried.
        :type retry: google.api_core.retry.Retry
        :param timeout: The amount of time, in seconds, to wait for the request to
            complete. Note that if retry is specified, the timeout applies to each
            individual attempt.
        :type timeout: float
        :return: google.cloud.container_v1.types.Cluster
        """
        self.log.info('Fetching cluster (project_id=%s, zone=%s, cluster_name=%s)', project_id or self.project_id, self.location, name)
        return self.get_client().get_cluster(project_id=(project_id or self.project_id), zone=(self.location),
          cluster_id=name,
          retry=retry,
          timeout=timeout).self_link