# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/schema.py
# Compiled at: 2012-06-26 16:33:07
__docformat__ = 'restructuredtext'
from zope.schema.interfaces import IInt
from zope.interface import implements
from zope.schema import Int

class IInternalReference(IInt):
    """Marker interface for internal object reference"""
    pass


class InternalReference(Int):
    """Custom schema field for internal object reference"""
    implements(IInternalReference)