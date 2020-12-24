# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/collective/prettysociable/interfaces.py
# Compiled at: 2011-04-17 05:53:23
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

class IPrettySociableSpecific(IDefaultPloneLayer):
    """A marker interface that defines a Zope 3 browser layer."""
    pass