# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/ATMediaPage/interfaces/browserlayer.py
# Compiled at: 2010-05-23 05:23:00
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

class IATMediaPageSpecific(IDefaultPloneLayer):
    """A marker interface that defines a Zope 3 browser layer."""
    pass