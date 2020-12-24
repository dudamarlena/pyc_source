# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vagoth/virt/virtualmachine.py
# Compiled at: 2013-12-28 08:17:33
from ..node import Node

class VirtualMachine(Node):
    """
    `VirtualMachine` represents a VirtualMachine node type.

    It inherits vagoth.Node_

    Each method requests the scheduler to execute the related action.
    """

    @property
    def state(self):
        """Retrieve the state attribute from the metadata"""
        return self._doc.metadata.get('state', 'unknown')

    @state.setter
    def state(self, state):
        """Set the state attribute in the metadata"""
        self._doc.registry.update_metadata(self.node_id, {'state': state})
        self.refresh()

    def start(self, hint=None):
        """Schedule the start action"""
        self._manager.scheduler.action(self.node_id, 'vm_start', vm_name=self.node_id, hint=hint)

    def define(self, hint=None):
        """Schedule the define action"""
        self._manager.scheduler.action(self.node_id, 'vm_define', vm_name=self.node_id, hint=hint)

    def stop(self):
        """Schedule the stop action"""
        self._manager.scheduler.action(self.node_id, 'vm_stop', vm_name=self.node_id)

    def shutdown(self):
        """Schedule the shutdown action"""
        self._manager.scheduler.action(self.node_id, 'vm_shutdown', vm_name=self.node_id)

    def reboot(self):
        """Schedule the reboot action"""
        self._manager.scheduler.action(self.node_id, 'vm_reboot', vm_name=self.node_id)

    def undefine(self):
        """Schedule the undefine action"""
        self._manager.scheduler.action(self.node_id, 'vm_undefine', vm_name=self.node_id)

    def provision(self):
        """Schedule the provision action"""
        self._manager.scheduler.action(self.node_id, 'vm_provision', vm_name=self.node_id)

    def deprovision(self):
        """Schedule the deprovision action"""
        self._manager.scheduler.action(self.node_id, 'vm_deprovision', vm_name=self.node_id)

    def __str__(self):
        return self.node_id

    def __repr__(self):
        return '<VirtualMachine %s at %x>' % (self.node_id, id(self))