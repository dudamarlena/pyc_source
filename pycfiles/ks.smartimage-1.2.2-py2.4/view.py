# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/smartimage/smartimagecache/browser/view.py
# Compiled at: 2008-12-23 17:55:58
"""Stat view

$Id: view.py 12472 2007-10-26 19:21:11Z anton $
"""
__author__ = 'Anton Oprya'
__license__ = 'ZPL'
__version__ = '$Revision: 12472 $'
__date__ = '$Date: 2007-10-26 22:21:11 +0300 (Fri, 26 Oct 2007) $'
from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from ks.smartimage.smartimageadapter.interfaces import ISmartImageAdapter
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from ks.smartimage.interfaces import ISmartImage
from zope.interface import providedBy
from logging import getLogger
logger = getLogger('ks.smartimage')

class Stat(BrowserView):
    __module__ = __name__
    stat_view = ViewPageTemplateFile('stat.pt')

    def __init__(self, context, request):
        super(Stat, self).__init__(context, request)
        self.context = context
        self.request = request

    def clearSmartImageCache(self, *kv, **kw):
        while len(self.context) > 0:
            for key in self.context.keys():
                del self.context[key]

        return self.stat_view(self, *kv, **kw)

    def reindexSmartImageCache(self, *kv, **kw):
        res = set()
        while len(self.context) > 0:
            for key in self.context.keys():
                try:
                    res.add(int(key.split('-')[(-1)]))
                except ValueError, msg:
                    logger.warning('%(key)s is wrong name for SmartImageCache element', dict(key=key), exc_info=True)

                del self.context[key]

        ids = getUtility(IIntIds, context=self.context)
        for id in res:
            try:
                ob = ids.getObject(id)
                for sc in self.context.scales:
                    smim = ISmartImageAdapter(ob)
                    smim.savetoCache(sc.name)

            except:
                logger.warning('Lookup %(id)s error', dict(id=id), exc_info=True)

        return self.stat_view(self, *kv, **kw)

    def reindexalternativeSmartImageCache(self, *kv, **kw):
        ids = getUtility(IIntIds, context=self.context)
        for (id, kr) in ids.items():
            try:
                ob = ids.getObject(id)
                if ISmartImage.providedBy(ob):
                    for sc in self.context.scales:
                        smim = ISmartImageAdapter(ob)
                        smim.savetoCache(sc.name)

            except:
                logger.warning('Lookup %(id)s error', dict(id=id), exc_info=True)

        return self.stat_view(self, *kv, **kw)