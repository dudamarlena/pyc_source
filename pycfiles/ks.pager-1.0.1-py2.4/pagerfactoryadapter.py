# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/pager/pagerfactoryadapter/pagerfactoryadapter.py
# Compiled at: 2007-11-08 12:36:38
"""SiteUrl adapters for the Zope 3 based issue package

$Id: pagerfactoryadapter.py 1270 2007-08-17 17:01:42Z anton $
"""
__author__ = 'Anatoly Bubenkov'
__license__ = 'ZPL'
__version__ = '$Revision: 1270 $'
__date__ = '$Date: 2007-08-17 20:01:42 +0300 (Пт, 17 авг 2007) $'
from zope.interface import implements
from zope.publisher.browser import BrowserView
from ks.pager.interfaces import IPagerFactory, IPagerParams, IPager, IPagedSource
from zope.component import getMultiAdapter

class PagerFactoryAdapter(BrowserView):
    """Pager Factory View"""
    __module__ = __name__
    implements(IPagerFactory)

    def __call__(self):
        """See IPagerFactory interface"""
        return self

    def init(self, iterable, *kv, **kw):
        """See IPagerFactory interface"""
        params = getMultiAdapter([self.context, self.request], interface=IPagerParams, context=self.context)
        paged_iterable = IPagedSource(iterable)
        res = getMultiAdapter([paged_iterable, params, self.request], interface=IPager, context=self.context)
        res.init(*kv, **kw)
        return res