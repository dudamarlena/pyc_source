# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/security/schema.py
# Compiled at: 2012-06-20 11:58:16
from zope.schema.interfaces import ITextLine
from zope.interface import implements
from zope.schema import TextLine

class IPrincipal(ITextLine):
    """Marker interface to define principal ID field"""
    pass


class IPrincipalList(ITextLine):
    """Marker interface to define a list of principal IDs"""
    pass


class Principal(TextLine):
    """Schema field to store a principal ID"""
    _type = (
     str, unicode, list, tuple)
    implements(IPrincipal)


class PrincipalList(TextLine):
    """Schema field to store a list of principal IDs"""
    _type = (
     str, unicode, list, tuple)
    implements(IPrincipalList)