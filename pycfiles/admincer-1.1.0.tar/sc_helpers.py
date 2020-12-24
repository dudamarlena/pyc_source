# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_admin/hosts/helpers/sc_helpers.py
# Compiled at: 2018-01-31 14:44:08
from cloud_admin.hosts.helpers import EucaMachineHelpers

class StorageControllerHelpers(EucaMachineHelpers):
    """
    Represents a machine hosting the storage controller service.
    """

    @property
    def storage_controller_service(self):
        for service in self.services:
            if service.type == 'storage':
                return service

        return

    def get_backend_ebs_volumes(self, ids):
        raise NotImplementedError('get_backend_ebs_volumes')

    def get_backend_ebs_snapshots(self, ids):
        raise NotImplementedError('get_backend_ebs_snapshots')

    def delete_ebs_backend_volume(self, id):
        raise NotImplementedError('delete_ebs_backend_volume')

    def create_ebs_backend_volume(self, id):
        raise NotImplementedError('create_ebs_backend_volume')