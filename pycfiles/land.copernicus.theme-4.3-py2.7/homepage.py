# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/theme/browser/homepage.py
# Compiled at: 2018-04-23 08:38:48
from Products.Five.browser import BrowserView
from land.copernicus.content.config import MAX_NUMBER_NEWS

class HomepageView(BrowserView):
    """ Homepage
    """

    def __call__(self):
        return self.index()

    def news(self, limit=MAX_NUMBER_NEWS):
        catalog = self.context.portal_catalog
        query = {'portal_type': 'News Item', 
           'sort_on': 'Date', 
           'sort_order': 'descending', 
           'review_state': 'published', 
           'sort_limit': limit}
        return catalog(**query)[:limit]

    def news_image(self, news_item):
        images = news_item.unrestrictedTraverse('images')
        img = images.scale('image', width=1320, height=500, direction='up')
        try:
            return img.url
        except AttributeError:
            return

        return