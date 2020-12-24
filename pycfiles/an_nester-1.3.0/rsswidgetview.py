# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/anz/dashboard/browser/rsswidgetview.py
# Compiled at: 2010-09-26 21:53:54
import time, socket, cjson, feedparser
from Products.Five import BrowserView
from zope.interface import implements
from zope.component import getUtility
from Acquisition import aq_parent, aq_inner, aq_base
from zope.i18n import translate
from Products.CMFCore.utils import getToolByName
from plone.memoize.interfaces import ICacheChooser
from anz.dashboard.interfaces import IRssWidgetView
from anz.dashboard import MSG_FACTORY as _

class RssWidgetView(BrowserView):
    """ Provide RSS widget functions. """
    __module__ = __name__
    implements(IRssWidgetView)

    def entries(self, url, cachetime=900, retJson=True):
        """ Return fetched rss entries.
        
        @param url
        url of the rss feed
        
        @param cachetime
        time to keep the result in cache( in second, default is 900 )
        
        @retJson
        format return value to json format or not( default True )
        
        @return status of create process
        json data:
        {
            success: True,
            msg: 'Fetch rss entries success.',
            entries: [...]
        }
        
        """
        ret = {}
        try:
            items = []
            feed = self._fetchFeed(url, cachetime)
            if feed.has_key('bozo_exception'):
                ret['success'] = False
                ret['msg'] = str(feed['bozo_exception'])
            else:
                toLocalizedTime = self.context.restrictedTraverse('@@plone').toLocalizedTime
                for entry in feed.entries:
                    item = {}
                    item['title'] = entry.title
                    item['link'] = entry.link
                    item['summary'] = entry.summary
                    item['updated'] = toLocalizedTime(entry.updated, long_format=1)
                    items.append(item)

                ret['success'] = True
                ret['msg'] = translate(_('Fetch RSS entries success.'), context=self.request)
                ret['entries'] = items
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)

        return retJson and cjson.encode(ret) or ret

    def _fetchFeed(self, url, cachetime=900):
        now = time.time()
        chooser = getUtility(ICacheChooser)
        cache = chooser('anz.dashboard.widget_rss.feedcache')
        cached_data = cache.get(url, None)
        if cached_data is not None:
            (timestamp, feed) = cached_data
            if now - timestamp < cachetime:
                return feed
            socket.setdefaulttimeout(5)
            newfeed = feedparser.parse(url, etag=getattr(feed, 'etag', None), modified=getattr(feed, 'modified', None))
            if newfeed.status == 304:
                cache[url] = (
                 now + cachetime, feed)
                return feed
        socket.setdefaulttimeout(5)
        feed = feedparser.parse(url)
        cache[url] = (now + cachetime, feed)
        return feed