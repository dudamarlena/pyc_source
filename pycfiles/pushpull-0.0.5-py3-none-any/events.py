# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pushpage/events.py
# Compiled at: 2006-10-05 16:04:27
__doc__ = ' PushPage events\n\n$Id: events.py,v 1.1 2006/10/05 20:04:27 tseaver Exp $\n'
from zope.interface import implements
from pushpage.interfaces import IPushPageEvent
from pushpage.interfaces import IPushPageNamespaceInit
from pushpage.interfaces import IPushPageRendered

class PushPageNamespaceInit(object):
    __module__ = __name__
    implements(IPushPageNamespaceInit)

    def __init__(self, page, namespace):
        self.page = page
        self.namespace = namespace


class PushPageRendered(object):
    __module__ = __name__
    implements(IPushPageRendered)

    def __init__(self, page, rendered):
        self.page = page
        self.rendered = rendered