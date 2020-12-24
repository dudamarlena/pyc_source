# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/zope2/ZopeTwiddlerRepeater.py
# Compiled at: 2008-07-24 14:48:01
from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import view
from Acquisition import Explicit
from Globals import InitializeClass
from twiddler.interfaces import IRepeater
from zope.interface import implements

class ZopeTwiddlerRepeater(Explicit):
    implements(IRepeater)

    def __init__(self, e):
        self.r = e.repeater()

    security = ClassSecurityInfo()
    security.declareObjectProtected(view)
    security.declareProtected(view, 'repeat')

    def repeat(self, *args, **kw):
        """Proxy for TwiddlerRepeater.repeat"""
        from twiddler.zope2.ZopeTwiddlerCopyElement import ZopeTwiddlerCopyElement
        return ZopeTwiddlerCopyElement(self.r.repeat(*args, **kw)).__of__(self)


InitializeClass(ZopeTwiddlerRepeater)