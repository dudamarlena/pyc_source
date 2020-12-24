# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/customers/content/containers.py
# Compiled at: 2008-09-03 11:14:43
from zope.interface import implements
from Products.Archetypes.atapi import BaseBTreeFolder
from Products.Archetypes.atapi import registerType
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import ISessionsContainer
from easyshop.core.interfaces import ICustomersContainer

class CustomersContainer(BaseBTreeFolder):
    """A simple container to hold customers.
    """
    __module__ = __name__
    implements(ICustomersContainer)


class SessionsContainer(BaseBTreeFolder):
    """A simple container to hold session data.
    """
    __module__ = __name__
    implements(ISessionsContainer)


registerType(CustomersContainer, PROJECTNAME)
registerType(SessionsContainer, PROJECTNAME)