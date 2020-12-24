# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/theme/browser/viewlets.py
# Compiled at: 2018-04-23 08:38:48
from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from land.copernicus.content.config import MAX_NUMBER_EVENTS
from land.copernicus.content.config import MAX_NUMBER_NEWS
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import ram
from time import time

class CopernicusFooterInfoViewlet(ViewletBase):
    render = ViewPageTemplateFile('footer_info.pt')

    @ram.cache(lambda *args: time() // 3600)
    def last_update(self):
        catalog = self.context.portal_catalog
        results = catalog.searchResults({'portal_type': ['LandItem', 'LandSection'], 'review_state': 'published', 
           'sort_on': 'modified', 
           'sort_order': 'descending'})
        last_update = None
        if results:
            last_update = results[0].ModificationDate
        return last_update


class CopernicusEventsViewlet(ViewletBase):
    render = ViewPageTemplateFile('events.pt')

    def events(self, limit=MAX_NUMBER_EVENTS):
        catalog = self.context.portal_catalog
        query = {'portal_type': 'Event', 
           'sort_on': 'start', 
           'sort_order': 'ascending', 
           'review_state': 'published', 
           'end': {'query': DateTime(), 
                   'range': 'min'}, 
           'sort_limit': limit}
        return catalog(**query)[:limit]


class CopernicusNewsViewlet(ViewletBase):
    render = ViewPageTemplateFile('news.pt')

    def news(self, limit=MAX_NUMBER_NEWS):
        catalog = self.context.portal_catalog
        query = {'portal_type': 'News Item', 
           'sort_on': 'Date', 
           'sort_order': 'descending', 
           'review_state': 'published', 
           'sort_limit': limit}
        return catalog(**query)[:limit]


class CopernicusSurveyViewlet(ViewletBase):
    """ Satisfaction survey [refs #93752]
        TODO: clean this when done.
    """
    render = ViewPageTemplateFile('survey.pt')

    @property
    def survey_url(self):
        return 'https://ec.europa.eu/eusurvey/runner/clms2018'