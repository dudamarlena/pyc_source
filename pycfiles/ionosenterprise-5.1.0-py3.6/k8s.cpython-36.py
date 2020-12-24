# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ionosenterprise/requests/k8s.py
# Compiled at: 2019-10-08 04:15:23
# Size of source mod 2**32: 2336 bytes
import json

class k8s:

    def get_k8s_cluster(self, k8s_cluster_id):
        """
        Retrieves a kubernetes cluster by its ID.

        :param      k8s_cluster_id: The unique ID of the cluster.
        :type       k8s_cluster_id: ``str``

        """
        response = self._perform_request('/k8s/%s' % k8s_cluster_id)
        return response

    def list_k8s_clusters(self, depth=1):
        """
        Retrieves the list of kubernetes clusters.

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request('/k8s?depth=' + str(depth))
        return response

    def create_k8s_cluster(self, name):
        """
        Creates a Kubernets cluster.

        :param      name: A Kubernetes Cluster Name. Valid Kubernetes
                          Cluster name must be 63 characters or less
                          and must be empty or begin and end with an
                          alphanumeric character ([a-z0-9A-Z]) with
                          dashes (-), underscores (_), dots (.), and
                          alphanumerics between.
        :type       name: ``str``

        """
        data = json.dumps(self._create_k8s_dict(name))
        response = self._perform_request(url='/k8s',
          method='POST',
          data=data)
        return response

    def delete_k8s_cluster(self, k8s_cluster_id):
        """
        Removes a kubernetes cluster.

        :param      k8s_cluster_id: The unique ID of the cluster.
        :type       k8s_cluster_id: ``str``

        """
        response = self._perform_request(url=('/k8s/%s' % k8s_cluster_id),
          method='DELETE')
        return response

    def update_k8s_cluster(self, k8s_cluster_id, **kwargs):
        """
        Replace all properties of a kubernetes cluster.

        :param      k8s_cluster_id: The unique ID of the cluster.
        :type       k8s_cluster_id: ``str``

        """
        data = {}
        for attr, value in kwargs.items():
            data[self._underscore_to_camelcase(attr)] = value

        response = self._perform_request(url=('/k8s/%s' % k8s_cluster_id),
          method='PUT',
          data=(json.dumps(data)))
        return response