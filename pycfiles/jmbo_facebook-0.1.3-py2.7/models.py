# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jmbo_facebook/models.py
# Compiled at: 2013-05-14 10:38:30
import datetime, urllib2
from django.db import models
from django.core.cache import cache
from django.utils import simplejson
from jmbo.models import ModelBase

class Update(ModelBase):
    """Purely a wrapper that allows us to use jmbo-foundry's listings for 
    updates."""

    def __init__(self, update, page):
        attrs = ('message', 'created_time', 'updated_time', 'from')
        for attr in attrs:
            setattr(self, attr, update.get(attr))

        self.page_object = page

    @property
    def as_leaf_class(self):
        return self

    def save(self):
        raise NotImplemented


class Page(ModelBase):
    facebook_id = models.CharField(max_length=64, editable=False, unique=True)
    access_token = models.CharField(max_length=255, editable=False)

    def fetch(self, force=False):
        cache_key = 'jmbo_facebook_page_%s' % self.slug
        cached = cache.get(cache_key, None)
        if cached is not None:
            return cached
        else:
            updates = []
            url = 'https://graph.facebook.com/%s/feed?access_token=%s' % (
             self.facebook_id, self.access_token)
            try:
                response = urllib2.urlopen(url)
            except Exception as e:
                pass

            json = simplejson.loads(response.read())
            for di in json['data']:
                if di['type'] not in ('status', 'photo'):
                    continue
                if di['from']['id'] != self.facebook_id:
                    continue
                if not di.get('message'):
                    continue
                di['created_time'] = datetime.datetime.strptime(di['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
                di['updated_time'] = datetime.datetime.strptime(di['updated_time'], '%Y-%m-%dT%H:%M:%S+0000')
                updates.append(di)

            cache.set(cache_key, updates, 1200)
            return updates

    @property
    def updates(self):

        class MyList(list):
            """Slightly emulate QuerySet API so jmbo-foundry listings work"""

            @property
            def exists(self):
                return len(self) > 0

        result = []
        for update in self.fetch():
            result.append(Update(update, page=self))

        return MyList(result)