# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/interfaces/tree.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 1246 bytes
__doc__ = 'PyAMS_utils.interfaces.tree module\n\nThe interfaces provided by this module are used to manage trees.\n'
from zope.interface import Interface, Attribute

class INode(Interface):
    """INode"""
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
    """ITree"""

    def get_root_nodes(self):
        """Get list of root nodes"""
        pass