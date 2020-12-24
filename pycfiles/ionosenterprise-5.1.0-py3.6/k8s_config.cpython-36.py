# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ionosenterprise/requests/k8s_config.py
# Compiled at: 2019-10-08 04:15:23
# Size of source mod 2**32: 361 bytes


class k8s_config:

    def get_k8s_config(self, k8s_cluster_id):
        """
        Retrieves a kubernetes cluster config by its ID.

        :param      k8s_cluster_id: The unique ID of the cluster.
        :type       k8s_cluster_id: ``str``

        """
        response = self._perform_request('/k8s/%s/kubeconfig' % k8s_cluster_id)
        return response