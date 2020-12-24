# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vagoth/interfaces/provisioner.py
# Compiled at: 2013-12-29 04:05:49
import zope.interface as ZI

class IProvisioner(ZI.Interface):
    """
    The provisioner is called to add a node to the cluster, and to
    remove a node from the cluster.

    It is the responsibility of the Provisioner to ensure that a node
    is correct and valid before adding it to Vagoth.

    Depending on how you want to use Vagoth, you could simply pass through
    the definition as-is to the registry, or you may want to convert
    "vm_size": "small" into a fully fledged definition complete
    with IPs, storage, etc.

    You may also like to hook this into some DNS and DHCP API to create
    entries for the host.

    vagoth.exceptions.ProvisioningException is the only exception
    that should be handled.  All other exceptions are undefined
    behaviour.

    If ProvisioningException is raised during the provision() call
    then the node has not been provisioned in the cluster.

    If ProvisioningException is raised during the deprovision() call,
    then the node remains in the cluster.
    """

    def __init__(manager, config):
        """Takes the manager, local config dict and the global config object"""
        pass

    def provision(node_id, node_name=None, node_type=None, tenant=None, definition=None, metadata=None, tags=None, unique_keys=None):
        """
        Do all required steps to provision the given node in Vagoth, including adding to the registry.
        Throw a ProvisioningException if there were any issues.
        """
        pass

    def deprovision(node_id):
        """
        Do any cleanup of resources etc. before this VM definition is
        removed from the cluster.
        """
        pass