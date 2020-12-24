# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/utilities/types.py
# Compiled at: 2009-04-26 22:17:24
from persistent import Persistent
from zope.interface import implements
from interfaces import INormativaTypes

class NormativaTypes(Persistent):
    __module__ = __name__
    implements(INormativaTypes)
    types = []

    def get_types(self):
        return [ a.encode('utf-8') for a in self.types ]