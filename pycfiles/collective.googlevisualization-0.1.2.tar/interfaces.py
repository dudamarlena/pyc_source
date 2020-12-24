# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/collective/googlesystemstorage/interfaces.py
# Compiled at: 2010-03-24 19:39:07
__doc__ = '\nInterfaces exposed here\n'
__author__ = 'federica'
__docformat__ = 'restructuredtext'
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.interface import Interface

class IFSSInfo(IAttributeAnnotatable):
    """Marker for FSSInfo"""
    __module__ = __name__


class IGoogleDocsManaged(Interface):
    """Marker interface for documents stored on Google Docs service"""
    __module__ = __name__