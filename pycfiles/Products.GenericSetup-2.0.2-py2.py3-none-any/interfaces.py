# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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