# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/galleriffic/interfaces.py
# Compiled at: 2010-01-04 03:43:54
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

class IGallerifficView(Interface):
    """ Marker interface"""
    __module__ = __name__


class IGallerifficSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """
    __module__ = __name__