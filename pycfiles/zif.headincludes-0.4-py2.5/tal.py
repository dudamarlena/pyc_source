# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zif/headincludes/tal.py
# Compiled at: 2010-03-12 11:12:03
"""Resource Library Expression Type

$Id: tal.py 3268 2005-08-22 23:31:27Z benji $
"""
from zope.tales.expressions import StringExpr
import resourcelibrary

class ResourceLibraryExpression(StringExpr):
    """Resource library expression handler class"""

    def __call__(self, econtext):
        resourcelibrary.need(self._expr)
        return ''