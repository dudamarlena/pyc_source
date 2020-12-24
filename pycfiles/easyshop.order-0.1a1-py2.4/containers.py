# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/order/content/containers.py
# Compiled at: 2008-09-03 11:15:08
from zope.interface import implements
from Products.Archetypes.atapi import BaseBTreeFolder
from Products.Archetypes.atapi import registerType
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IOrdersContainer

class OrdersContainer(BaseBTreeFolder):
    """A simple container to hold orders.
    """
    __module__ = __name__
    implements(IOrdersContainer)


registerType(OrdersContainer, PROJECTNAME)