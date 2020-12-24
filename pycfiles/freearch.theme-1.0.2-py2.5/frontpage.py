# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/freearch/theme/browser/frontpage.py
# Compiled at: 2008-06-19 11:34:27
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATNewsItem
from DateTime import DateTime
from plone.app.portlets.portlets.rss import RSSFeed

class FrontPageView(BrowserView):
    """ Render front page.
    
    Front page has three different slots:
        - News (all published site news items)
        - Blog (custom blog entry title RSS reader)
        - Customer references (custom content type created through-the-web using Plone Generic Content product)
        
    This view is called from the front page template. 
        
    Uses RSSFeed fetcher from portlets to obtain RSS feed items
    for the front page. Feed settings are currently hardcoded to this file,
    so you probably want edit the settings below.
    
    """
    template = ViewPageTemplateFile('templates/front_page_view.pt')

    def init_feeds(self):
        self.feeds = {'fi': RSSFeed('http://blog.redinnovation.com/feed/', 60), 
           'en': RSSFeed('http://blog.redinnovation.com/feed/', 60), 
           'en-us': RSSFeed('http://blog.redinnovation.com/feed/', 60), 
           'default': RSSFeed('http://blog.redinnovation.com/feed/', 60)}

    def __call__(self):
        if not hasattr(self, 'feeds'):
            self.init_feeds()
        return self.template()

    def recently_published_news(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        results = []
        for r in catalog(portal_type='News Item', review_state='published', sort_on='Date', sort_order='reverse', sort_limit=2):
            results.append(dict(date=r.Date, year=DateTime(r.Date).year(), month=DateTime(r.Date).month(), day=DateTime(r.Date).day(), news_obj=r.getObject(), url=r.getURL(), title=r.Title, description=r.Description))

        return results

    def get_references(self):
        """ Show all customer references published content on the front page. """
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        results = []
        for r in catalog(portal_type='CustomerReference', review_state='published', sort_on='Date', sort_order='reverse', sort_limit=4):
            results.append(dict(date=r.Date, year=DateTime(r.Date).year(), month=DateTime(r.Date).month(), day=DateTime(r.Date).day(), news_obj=r.getObject(), url=r.getURL(), title=r.Title, description=r.Description))

        return results

    def get_blog_feed(self, lang):
        """ Fetch blog feed from the remote server.
        
        feed.update() does nothing if we have a fresh cache.
        """
        if lang in self.feeds:
            feed = self.feeds[lang]
        else:
            return self.feeds['default']
        feed.update()
        items = feed.items
        for i in items:
            i['friendly_time'] = i['updated'].strftime('%Y-%m-%d')

        return items