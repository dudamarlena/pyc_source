# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/zope2/ZopeTwiddlerCopyElement.py
# Compiled at: 2008-07-24 14:48:01
from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import view
from Acquisition import Explicit
from Globals import InitializeClass
from twiddler.interfaces import IElement
from twiddler.zope2.ZopeTwiddlerRepeater import ZopeTwiddlerRepeater
from zope.interface import implements

class ZopeTwiddlerCopyElement(Explicit):
    implements(IElement)

    def __init__(self, e):
        self.e = e

    security = ClassSecurityInfo()
    security.declareObjectProtected(view)

    def get_node(self):
        return self.e.node

    node = property(get_node)
    security.declareProtected(view, '__getitem__')

    def __getitem__(self, value):
        """Proxy for TwiddlerSearcher.__getitem__"""
        return ZopeTwiddlerCopyElement(self.e[value]).__of__(self)

    security.declareProtected(view, 'getBy')

    def getBy(self, **spec):
        """Proxy for TwiddlerSearcher.getBy"""
        return ZopeTwiddlerCopyElement(self.e.getBy(**spec)).__of__(self)

    security.declareProtected(view, 'replace')

    def replace(self, *args, **kw):
        """Proxy for TwiddlerElement.replace"""
        self.e.replace(*args, **kw)

    security.declareProtected(view, 'repeater')

    def repeater(self, *args, **kw):
        """Proxy for TwiddlerElement.repeater"""
        return ZopeTwiddlerRepeater(self.e).__of__(self)

    security.declareProtected(view, 'clone')

    def clone(self):
        """Proxy for TwiddlerElement.clone"""
        return ZopeTwiddlerCopyElement(self.e.clone()).__of__(self)

    security.declareProtected(view, 'remove')

    def remove(self, *args, **kw):
        """Proxy for TwiddlerElement.remove"""
        self.e.remove(*args, **kw)


InitializeClass(ZopeTwiddlerCopyElement)