# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/matej/workarea/plone.hud/plone.app.hud/src/plone/app/hud/hud_security_advisories.py
# Compiled at: 2013-08-26 15:59:46
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from datetime import datetime
from plone.app.hud import _
from plone.hud.panel import HUDPanelView
from plone.memoize.ram import RAMCacheAdapter
from plone.memoize.volatile import cache
from plone.registry import Record
from plone.registry import field
from plone.registry.interfaces import IRegistry
from time import mktime
from zope.component import getUtility
from zope.ramcache import ram
import feedparser, hashlib, logging
feed_cache = ram.RAMCache()
feed_cache.update(maxAge=86400, maxEntries=10)
logger = logging.getLogger('plone.app.hud.hud_security_advisories')

class SecurityAdvisoriesView(HUDPanelView):
    panel_template = ViewPageTemplateFile('hud_security_advisories.pt')
    title = _('Security Advisories')
    FEED_URL = 'http://plone.org/products/plone/security/advisories/all-advisories/RSS'
    HASH_RECORD = 'plone.app.hud.hud_security_advisories.hash_list'

    def render(self):
        if 'invalidate_cache' in self.request.form:
            feed_cache.invalidateAll()
        if 'toggle_mark' in self.request.form:
            self.toggle_mark = self.request.form['toggle_mark']
        else:
            self.toggle_mark = None
        self.registry = getUtility(IRegistry)
        if self.HASH_RECORD not in self.registry:
            hash_field = field.List(title='Feed Hash List', value_type=field.ASCII(title='Hash'))
            self.registry.records[self.HASH_RECORD] = Record(hash_field, value=[])
        self.feed_data = self.get_feed_data()
        return self.panel_template()

    @cache(lambda method, self: 'cache_key', get_cache=lambda fun, *args, **kwargs: RAMCacheAdapter(feed_cache))
    def parse_feed(self):
        logger.info(('Parsing feed from url: {0}').format(self.FEED_URL))
        self.sa_dict = feedparser.parse(self.FEED_URL)
        return self.sa_dict

    def get_feed_data(self):
        feed_dict = self.parse_feed()
        result = []
        hash_list = []
        if 'entries' not in feed_dict:
            return None
        else:
            for entry in feed_dict['entries']:
                item = self._get_item(entry)
                if item['marked_as_read']:
                    hash_list += [item['hash']]
                result += [item]

            self.registry[self.HASH_RECORD] = hash_list
            return sorted(result, key=lambda item: item['updated'], reverse=True)

    def _get_subitem(self, entry, name):
        subitem = entry[name] if name in entry else None
        subitem = unicode(subitem)
        return subitem

    def _get_item(self, entry):
        title = self._get_subitem(entry, 'title')
        summary = self._get_subitem(entry, 'summary')
        link = self._get_subitem(entry, 'link')
        updated = self._get_subitem(entry, 'updated')
        updated_parsed = entry['updated_parsed'] if 'updated_parsed' in entry else None
        sha_obj = hashlib.sha1()
        sha_obj.update(title.encode('utf8'))
        sha_obj.update(summary.encode('utf8'))
        sha_obj.update(updated.encode('utf8'))
        shahash = sha_obj.hexdigest()
        marked_as_read = shahash in self.registry[self.HASH_RECORD]
        if self.toggle_mark == shahash:
            marked_as_read = not marked_as_read
        updated_datetime = datetime.fromtimestamp(mktime(updated_parsed))
        localized_time = self.context.toLocalizedTime(updated_datetime)
        item = {'title': title, 
           'hash': shahash, 
           'marked_as_read': marked_as_read, 
           'localized_time': localized_time, 
           'updated': updated_datetime, 
           'summary': summary, 
           'link': link}
        return item