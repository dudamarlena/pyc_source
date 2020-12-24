# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vagoth/virt/hypervisor.py
# Compiled at: 2013-12-28 07:56:08
from ..node import Node

class Hypervisor(Node):
    """
    A basic Hypervisor class.  A hypervisor has a driver

    It inherits vagoth.Node_
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

    @property
    def children(self):
        """Return the children of this hypervisor"""
        return self._manager.get_nodes_with_parent(self._node_id)

    @property
    def driver_name(self):
        """Return the driver name for this hypervisor, or default"""
        driver_name = self.definition.get('driver', 'default')
        assert isinstance(driver_name, basestring)
        return driver_name

    @property
    def driver(self):
        """Return the driver for this hypervisor"""
        return self._manager.config.make_factory('virt/drivers/%s' % (self.driver_name,), self._manager)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Hypervisor %s at %x>' % (self.node_id, id(self))