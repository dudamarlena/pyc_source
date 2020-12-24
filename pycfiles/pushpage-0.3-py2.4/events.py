# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pushpage/events.py
# Compiled at: 2006-10-05 16:04:27
""" PushPage events

$Id: events.py,v 1.1 2006/10/05 20:04:27 tseaver Exp $
"""
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