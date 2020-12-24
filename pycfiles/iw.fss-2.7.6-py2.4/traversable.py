# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/traversable.py
# Compiled at: 2008-10-23 05:55:17
from zope.traversing.adapters import DefaultTraversable
from utils import getFieldValue

class FSSTraversable(DefaultTraversable):
    __module__ = __name__

    def traverse(self, name, furtherPath):
        obj = self._subject
        field = obj.getField(name)
        if field:
            return getFieldValue(obj, name)
        return super(FSSTraversable, self).traverse(name, furtherPath)