# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/pager/pagedsourceadapter/pagedsourceadapter.py
# Compiled at: 2007-11-08 12:36:38
"""SiteUrl adapters for the Zope 3 based pager package

$Id: pagedsourceadapter.py 1440 2007-09-29 15:24:49Z anatoly $
"""
__author__ = 'Anatoly Bubenkov'
__license__ = 'ZPL'
__version__ = '$Revision: 1440 $'
__date__ = '$Date: 2007-09-29 18:24:49 +0300 (Сб, 29 сен 2007) $'
from zope.interface import Interface, implements
from zope.cachedescriptors.property import CachedProperty
from ks.pager.interfaces import IPagedSource
from zope.component import adapts

class PagedSourceAdapter(object):
    __module__ = __name__
    adapts(Interface)
    implements(IPagedSource)

    def __init__(self, context):
        self.context = context

    def getChunk(self, start, chunkSize, *kv, **kw):
        """See IPagedSource interface"""
        if self.context is None:
            return []
        if self.getCount():
            return self.context[start:start + chunkSize]
        return []

    def getCount(self, *kv, **kw):
        """See IPagedSource interface"""
        return len(list(self.context))