# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/interfaces/tree.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 1246 bytes
"""PyAMS_utils.interfaces.tree module

The interfaces provided by this module are used to manage trees.
"""
from zope.interface import Interface, Attribute

class INode(Interface):
    __doc__ = 'Tree node interface'
    context = Attribute("Node's context")
    label = Attribute("Node's label")
    css_class = Attribute("Node's CSS class")
    order = Attribute("Node's order")

    def get_level(self):
        """Get depth level of current node"""
        pass

    def has_children(self, filter_value=None):
        """Check if current node has children"""
        pass

    def get_children(self, filter_value=None):
        """Get list of node children"""
        pass


class ITree(Interface):
    __doc__ = 'Tree interface'

    def get_root_nodes(self):
        """Get list of root nodes"""
        pass