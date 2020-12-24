# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/collective/googlesystemstorage/interfaces.py
# Compiled at: 2010-03-24 19:39:07
"""
Interfaces exposed here
"""
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