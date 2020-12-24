# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_admin/hosts/helpers/clc_helpers.py
# Compiled at: 2018-01-31 14:44:08
from cloud_admin.hosts.helpers import EucaMachineHelpers

class CloudControllerHelpers(EucaMachineHelpers):
    """
    Helper methods for the machine hosting the cluster controller service.
    """

    @property
    def cloud_controller_service(self):
        for service in self.services:
            if service.type == 'eucalyptus':
                return service

        return