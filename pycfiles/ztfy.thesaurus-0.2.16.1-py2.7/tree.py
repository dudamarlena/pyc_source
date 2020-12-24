# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/interfaces/tree.py
# Compiled at: 2012-01-26 11:07:11
from zope.interface import Interface, Attribute
from ztfy.thesaurus import _

class INode(Interface):
    """Tree node interface"""
    context = Attribute(_("Node's context"))
    label = Attribute(_("Node's label"))
    cssClass = Attribute(_("Node's CSS class"))

    def getLevel(self):
        """Get depth level of current node"""
        pass

    def hasChildren(self):
        """Check if current node has childrens"""
        pass

    def getChildren(self):
        """Get list of node childrens"""
        pass


class ITree(Interface):
    """Tree interface"""

    def getRootNodes(self):
        """Get list of root nodes"""
        pass