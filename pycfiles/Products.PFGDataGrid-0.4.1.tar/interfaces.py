# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Person/interfaces.py
# Compiled at: 2011-06-07 12:12:26
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from Products.Person import PersonMessageFactory as _
from plone.theme.interfaces import IDefaultPloneLayer

class IPerson(Interface):
    """Marker interface
    """


class IPersonSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer 
       for this product.
    """