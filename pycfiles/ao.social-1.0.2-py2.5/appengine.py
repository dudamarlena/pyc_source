# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ao/social/appengine.py
# Compiled at: 2010-03-23 14:22:02
import ao.shorturl
from google.appengine.api import memcache
from google.appengine.ext import db

class ShortUrl(db.Model):
    """Stores the short URL tokens in the datastore."""
    context = db.ReferenceProperty(collection_name='shorturl')


class AppEngineShortUrlHandler(ao.shorturl.BaseShortUrlHandler):
    """Short URL handler for Google App Engine.

    Uses the Datastore to store URLs and tokens, and the Memcache API for
    caching tokens.

    """

    def cache_context(self, url, context):
        """Store the context's key name and kind in memcache."""
        memcache.add(url, str(context.key()), self.url_cache_time)

    def get_context_from_cache(self, url):
        """Get the token from memcache."""
        key = memcache.get(url)
        if key is None:
            raise LookupError('Context key not found in the cache.')
        return db.get(key)

    def get_context_from_db(self, url):
        """Get the context from the datastore."""
        mapping = ShortUrl.get_by_key_name(url)
        if mapping is None:
            raise LookupError('Context not found in the datastore.')
        return mapping.context

    def assign_url(self, context):
        """Create a new URL for the context and assign it to the context."""
        url = ShortUrl(key_name=self.generate_url(), context=context)
        url.put()

    def construct_url(self, context, request=None):
        """Construct the short url for the given context."""
        if context.shorturl.count() == 0:
            self.assign_url(context)
        return self.url_pattern(context.shorturl[0].key().name())