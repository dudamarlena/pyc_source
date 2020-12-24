# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/base/interfaces/container.py
# Compiled at: 2013-09-22 06:56:17
__docformat__ = 'restructuredtext'
from zope.container.interfaces import IContainer
from zope.interface import Interface

class IOrderedContainerOrder(Interface):
    """Ordered containers interface"""

    def updateOrder(self, order):
        """Reset items in given order"""
        pass

    def moveUp(self, key):
        """Move given item up"""
        pass

    def moveDown(self, key):
        """Move given item down"""
        pass

    def moveFirst(self, key):
        """Move given item to first position"""
        pass

    def moveLast(self, key):
        """Move given item to last position"""
        pass


class IOrderedContainer(IOrderedContainerOrder, IContainer):
    """Marker interface for ordered containers"""
    pass