# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/carts/content/carts_container.py
# Compiled at: 2008-09-03 11:14:22
from zope.interface import implements
from Products.Archetypes.atapi import BaseBTreeFolder
from Products.Archetypes.atapi import registerType
from easyshop.carts.config import *
from easyshop.core.interfaces.carts import ICartsContainer

class CartsContainer(BaseBTreeFolder):
    """A simple container to hold carts.
    """
    __module__ = __name__
    implements(ICartsContainer)


registerType(CartsContainer, PROJECTNAME)