# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Work/interfaces.py
# Compiled at: 2011-06-07 12:12:56
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from Products.Work import WorkMessageFactory as _
from plone.theme.interfaces import IDefaultPloneLayer

class IWork(Interface):
    """Marker interface
    """
    pass


class IWorkSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer 
       for this product.
    """
    pass