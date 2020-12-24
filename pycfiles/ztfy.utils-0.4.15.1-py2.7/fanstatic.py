# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/tal/fanstatic.py
# Compiled at: 2012-06-20 10:07:04
__docformat__ = 'restructuredtext'
from zope.tales.expressions import StringExpr
from ztfy.utils.traversing import resolve

class FanstaticTalesExpression(StringExpr):

    def __call__(self, econtext):
        lib, res = self._expr.split('#')
        module = resolve(lib)
        resource = getattr(module, res)
        resource.need()
        return ''