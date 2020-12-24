# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/zope2/ZopeTwiddlerCopy.py
# Compiled at: 2008-07-24 14:48:01
from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import view
from Acquisition import Explicit
from Globals import InitializeClass
from twiddler.zope2.ZopeTwiddlerCopyElement import ZopeTwiddlerCopyElement

class ZopeTwiddlerCopy(Explicit):

    def __init__(self, t):
        self.t = t

    security = ClassSecurityInfo()
    security.declareObjectProtected(view)

    def get_output(self):
        return self.t.output

    output = property(get_output)

    def get_node(self):
        return self.t.node

    node = property(get_node)
    security.declareProtected(view, 'clone')

    def clone(self):
        """Return a clone of ZopeTwiddlerCopy"""
        return ZopeTwiddlerCopy(loads(dumps(self.t))).__of__(self)

    security.declareProtected(view, '__getitem__')

    def __getitem__(self, value):
        """Proxy for TwiddlerSearcher.__getitem__"""
        return ZopeTwiddlerCopyElement(self.t[value]).__of__(self)

    security.declareProtected(view, 'getBy')

    def getBy(self, **spec):
        """Proxy for TwiddlerSearcher.getBy"""
        return ZopeTwiddlerCopyElement(self.t.getBy(**spec)).__of__(self)

    security.declareProtected(view, 'execute')

    def execute(self, *args, **kw):
        """Calls an executor in the Twiddler in the context of this proxy"""
        if self.t.executor is not None:
            t = self.t.executor(*((self,) + args), **kw)
            del self.t.executor
            if t is not None:
                return t
        return self.t

    security.declareProtected(view, 'render')

    def render(self, *args, **kw):
        """Renders this Twiddler Copy"""
        t = self.execute(*args, **kw)
        return t.output(t.node, *args, **kw)


InitializeClass(ZopeTwiddlerCopy)