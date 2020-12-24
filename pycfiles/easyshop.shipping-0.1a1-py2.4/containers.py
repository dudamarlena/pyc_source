# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shipping/content/containers.py
# Compiled at: 2008-09-03 11:15:19
from zope.interface import implements
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import registerType
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IShippingMethodsContainer
from easyshop.core.interfaces import IShippingPricesContainer

class ShippingPricesContainer(OrderedBaseFolder):
    """A simple container to hold shipping prices.
    """
    __module__ = __name__
    implements(IShippingPricesContainer)


class ShippingMethodsContainer(OrderedBaseFolder):
    """A simple container to hold shipping methods.
    """
    __module__ = __name__
    implements(IShippingMethodsContainer)


registerType(ShippingPricesContainer, PROJECTNAME)
registerType(ShippingMethodsContainer, PROJECTNAME)