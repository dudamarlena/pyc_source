# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_admin/hosts/helpers/helpernamespace.py
# Compiled at: 2018-01-31 14:44:08
from cloud_admin.hosts.helpers.dns_helpers import DnsHelpers
from cloud_admin.hosts.helpers.nc_helpers import NodeControllerHelpers
from cloud_admin.hosts.helpers.cc_helpers import ClusterControllerHelpers
from cloud_admin.hosts.helpers.clc_helpers import CloudControllerHelpers
from cloud_admin.hosts.helpers.sc_helpers import StorageControllerHelpers
from cloud_admin.hosts.helpers.midonethelpers import MidonetHelpers
from cloud_admin.hosts.helpers.osg_helpers import ObjectStorageGatewayHelpers

class HelperNamespace(object):

    def __init__(self, eucahost):
        self._eucahost = eucahost
        self.dns = DnsHelpers(eucahost)
        self.cloud_controller = CloudControllerHelpers(eucahost)
        self.cluster_controller = ClusterControllerHelpers(eucahost)
        self.midonet = MidonetHelpers(eucahost)
        self.node_controller = NodeControllerHelpers(eucahost)
        self.storage_controller = StorageControllerHelpers(eucahost)
        self.osg = ObjectStorageGatewayHelpers(eucahost)