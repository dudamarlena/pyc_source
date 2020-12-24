# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_admin/hosts/helpers/cc_helpers.py
# Compiled at: 2018-01-31 14:44:08
from cloud_admin.hosts.helpers import EucaMachineHelpers

class ClusterControllerHelpers(EucaMachineHelpers):
    """
    Represents a machine hosting the cluster controller service.
    """

    @property
    def cluster_controller_service(self):
        for service in self.services:
            if service.type == 'cluster':
                return service

        return

    def show_iptables(self):
        self.debug(self.sys('iptables-save', code=0, listformat=False))