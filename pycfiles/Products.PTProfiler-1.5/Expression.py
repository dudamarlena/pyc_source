# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.freebsd-7.1-PRERELEASE-i386/egg/Products/ProxyIndex/Expression.py
# Compiled at: 2008-08-28 10:38:51
__doc__ = ' Expressions in a web-configurable workflow.\n\n$Id: Expression.py,v 1.2 2003/05/09 10:51:01 hazmat Exp $\n'
import Globals
from Globals import Persistent
from Acquisition import aq_inner, aq_parent
from AccessControl import getSecurityManager, ClassSecurityInfo
from Products.PageTemplates.Expressions import getEngine, SafeMapping
from Products.PageTemplates.Expressions import SecureModuleImporter

class Expression(Persistent):
    __module__ = __name__
    text = ''
    _v_compiled = None
    security = ClassSecurityInfo()

    def __init__(self, text):
        self.text = text
        self._v_compiled = getEngine().compile(text)

    def __call__(self, econtext):
        compiled = self._v_compiled
        if compiled is None:
            compiled = self._v_compiled = getEngine().compile(self.text)
        res = compiled(econtext)
        if isinstance(res, Exception):
            raise res
        return res


Globals.InitializeClass(Expression)

def createExprContext(object):
    """
    An expression context provides names for TALES expressions.
    """
    data = {'object': object, 'nothing': None, 'request': getattr(object, 'REQUEST', None), 'modules': SecureModuleImporter}
    return getEngine().getContext(data)