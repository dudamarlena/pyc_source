# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/adverlet/tales.py
# Compiled at: 2008-12-22 07:00:12
__license__ = 'GPL v.3'
from StringIO import StringIO
from zope.interface import implements
from zope.tales.expressions import StringExpr
from zope.component import queryUtility, getMultiAdapter
from interfaces import ITALESAdverletExpression, IAdverlet

class TALESAdverletExpression(StringExpr):
    __module__ = __name__
    implements(ITALESAdverletExpression)

    def __call__(self, econtext):
        name = super(TALESAdverletExpression, self).__call__(econtext)
        adverlet = queryUtility(IAdverlet, name)
        if not adverlet:
            return
        source = adverlet.source
        if source:
            return not adverlet.newlines and source or ('').join([ '%s <br />' % s for s in StringIO(source).readlines() ])
        default = adverlet.default
        if not default:
            return
        view = getMultiAdapter((econtext.vars['context'], econtext.vars['request']), name=default)
        return view()