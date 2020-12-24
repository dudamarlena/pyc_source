# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/taxes/content/taxes_container.py
# Compiled at: 2008-09-03 11:15:45
from zope.interface import implements
from Products.Archetypes.atapi import *
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import ITaxesContainer

class TaxesContainer(OrderedBaseFolder):
    """A simple container to hold taxes.
    """
    __module__ = __name__
    implements(ITaxesContainer)


registerType(TaxesContainer, PROJECTNAME)