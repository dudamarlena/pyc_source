# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vagoth/interfaces/driver.py
# Compiled at: 2013-12-29 04:17:57
import zope.interface as ZI

class IDriver(ZI.Interface):
    """
    Interface required for managing VMs on a single server.

    If you want to use the vagoth.virt.virtualmachine_ and
    vagoth.virt.hypervisor_ as-is with your hypervisor API,
    you can implement your own driver using IDriver.

    For example, you could write a driver to manage Xen, VMWare or RHEV VMs,
    or even to manage VMs in remote clouds.
    """

    def __init__(manager, config):
        """
        """
        pass

    def provision(node, vm):
        """
        Request the node to provision the VM (eg. define then re-init)
        """
        pass

    def define(node, vm):
        """
        Request the node to define the VM
        """
        pass

    def undefine(node, vm):
        """
        Request the node to undefine the VM
        """
        pass

    def deprovision(node, vm):
        """
        Request the node to deprovision the VM (eg. undefine & wipe disks)
        """
        pass

    def start(node, vm):
        """
        Request the node to start the VM (ie. power-on)
        """
        pass

    def reboot(node, vm):
        """
        Request the node to reboot the VM (poweroff/poweron)
        """
        pass

    def stop(node, vm):
        """
        Request the node to stop the VM (power-off)
        """
        pass

    def shutdown(node, vm):
        """
        Request the node to nicely shutdown the VM (eg. ACPI poweroff)
        """
        pass

    def info(node, vm):
        """
        Request the information dict about this VM.
        It should include "definition" with a dict, as well as "state",
        and possibly others.
        """
        pass

    def status(node=None):
        """
        Request the "status" for the entire node. This should include a
        "vms" dict, containing the info for each VM.
        """
        pass

    def migrate(node, vm, destination_node):
        """
        Request the node to migrate the VM to the destination_node.
        """
        pass