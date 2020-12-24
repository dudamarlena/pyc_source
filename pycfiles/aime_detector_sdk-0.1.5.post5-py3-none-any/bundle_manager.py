# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/grad03/fengl/AIMES_project/aimes.bundle/src/aimes/bundle/bundle_manager.py
# Compiled at: 2015-08-31 13:40:26
import os, sys, time, logging, radical.utils as ru
from aimes.bundle.resource_bundle import ResourceBundle

def ip2id(ip):
    return ip.replace('.', '_')


class BundleManager(ru.Daemon):

    def __init__(self, session, _reconnect=False):
        super(BundleManager, self).__init__()
        self._session = session
        self._controller = None
        self._uid = None
        if _reconnect:
            return
        else:
            bundle_description = {}
            bundle = ResourceBundle.create(bundle_description=bundle_description, bundle_manager_id=self._uid)
            self.resource_bundle_list = {'default': bundle}
            return

    def list_resource_bundles(self):
        return self.resource_bundle_list.keys()

    def create_resource_bundle(self, resource_bundle_configuration):
        pass

    def get_resource_bundle(self, rb_id):
        return self.resource_bundle_list[rb_id]

    def get_data(self, origin=None):
        ret = dict()
        ret['cluster_list'] = self.get_cluster_list()
        ret['cluster_config'] = dict()
        ret['cluster_workload'] = dict()
        ret['cluster_bandwidth'] = dict()
        for cluster_ip in ret['cluster_list']:
            cluster_id = ip2id(cluster_ip)
            ret['cluster_config'][cluster_id] = self.get_cluster_configuration(cluster_ip)
            ret['cluster_workload'][cluster_id] = self.get_cluster_workload(cluster_ip)
            ret['cluster_bandwidth'][cluster_id] = self.get_cluster_bandwidth(cluster_ip)

        return ret