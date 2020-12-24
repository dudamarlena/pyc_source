# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vagoth/virt/drivers/dummy.py
# Compiled at: 2013-10-02 06:44:30
from ..utils.mc_json_rpc import mcollective_call
from ..exceptions import DriverException
ERRMSG = 'Cannot manage VMs on a Hypervisor using DummyDriver'

class DummyDriver(object):
    """
    The Dummy Driver never has info and raises a DriverException if you try to use it.
    """

    def __init__(self, manager, local_config):
        self.config = local_config

    def provision(self, node, vm):
        """Request a node to define & provision a VM"""
        raise DriverException(ERRMSG)

    def define(self, node, vm):
        """Request node to define a VM"""
        raise DriverException(ERRMSG)

    def undefine(self, node, vm):
        """Request node to undefine a VM"""
        raise DriverException(ERRMSG)

    def deprovision(self, node, vm):
        """Request node to undefine & deprovision a VM"""
        raise DriverException(ERRMSG)

    def start(self, node, vm):
        """Request node to start the VM"""
        raise DriverException(ERRMSG)

    def reboot(self, node, vm):
        """Request node to reboot the VM"""
        raise DriverException(ERRMSG)

    def stop(self, node, vm):
        """Request node to stop (forcefully) the VM"""
        raise DriverException(ERRMSG)

    def shutdown(self, node, vm):
        """Request node to shutdown (nicely) the VM"""
        raise DriverException(ERRMSG)

    def info(self, node, vm):
        """Request information about the given VM from the node"""
        return {}

    def status(self, node=None):
        """Request information about all VMs from the node"""
        return []

    def migrate(self, node, vm, destination_node):
        """Request the node to migrate the given VM to the destination node"""
        return NotImplemented