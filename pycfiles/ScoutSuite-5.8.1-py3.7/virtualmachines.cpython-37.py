# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/azure/facade/virtualmachines.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 2533 bytes
from azure.mgmt.compute import ComputeManagementClient
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently

class VirtualMachineFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        return ComputeManagementClient((self.credentials.arm_credentials), subscription_id=subscription_id)

    async def get_instances(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(lambda : list(client.virtual_machines.list_all()))
        except Exception as e:
            try:
                print_exception('Failed to retrieve virtual machines: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_instance_extensions(self, subscription_id: str, instance_name: str, resource_group: str):
        try:
            client = self.get_client(subscription_id)
            extensions = await run_concurrently(lambda : client.virtual_machine_extensions.list(resource_group, instance_name))
            return list(extensions.value)
        except Exception as e:
            try:
                print_exception('Failed to retrieve virtual machine extensions: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_disks(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(lambda : list(client.disks.list()))
        except Exception as e:
            try:
                print_exception('Failed to retrieve disks: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_snapshots(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(lambda : list(client.snapshots.list()))
        except Exception as e:
            try:
                print_exception('Failed to retrieve snapshots: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_images(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(lambda : list(client.images.list()))
        except Exception as e:
            try:
                print_exception('Failed to retrieve images: {}'.format(e))
                return []
            finally:
                e = None
                del e