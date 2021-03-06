# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/core/feeds.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = '\n    pocoo.pkg.core.feeds\n    ~~~~~~~~~~~~~~~~~~~~\n\n    Provides RSS Feeds.\n\n    :copyright: 2006 by Armin Ronacher.\n    :license: GNU GPL, see LICENSE for more details.\n'
from pocoo import Component
from pocoo.http import PageNotFound, Response
from pocoo.application import RequestHandler
from pocoo.db import meta
from pocoo.utils.feed import Feed
from pocoo.pkg.core.db import forums, posts, users
from pocoo.pkg.core.textfmt import parse_and_translate

class FeedProvider(Component):
    __module__ = __name__
    identifier = 'unknown'

    def get_feed(self, req, parameter):
        """
        Return a dict in the following form::

        {'title':       'Title of this feed',
         'description': 'Description of this feed',
         'items':       [{
             'title':       'title of this item',
             'link':        'relative link of this item',
             'author':      'author of this item',
             'description': 'description of this item',
             'pub_date':    'date of this item'
         }]}

        Can raise a `FeedNotFound` exception.
        """
        pass

    @property
    def url(self):
        return self.ctx.make_url('feeds/%s.xml' % self.identifier)


class FeedNotFound(Exception):
    __module__ = __name__


class ThreadFeed(FeedProvider):
    __module__ = __name__
    identifier = 'thread'

    def get_feed(self, req, post_id):
        _ = req.gettext
        try:
            post_id = int(post_id)
        except:
            raise FeedNotFound()

        row = self.ctx.engine.execute(meta.select([posts.c.root_post_id], posts.c.post_id == post_id)).fetchone()
        if row is None:
            raise FeedNotFound()
        root_post_id = row[0]
        result = self.ctx.engine.execute(meta.select([posts.c.post_id, posts.c.title, posts.c.text, posts.c.timestamp, users.c.username], (posts.c.root_post_id == root_post_id) & (users.c.user_id == posts.c.author_id), order_by=[meta.desc(posts.c.post_id)], limit=10))
        return {'title': _('Last Posts in Thread %d') % root_post_id, 'description': _('The last 10 posts in Thread %d') % root_post_id, 'items': [ {'title': post['title'], 'link': 'post/%d' % post['post_id'], 'description': parse_and_translate(req, post['text']), 'author': post['username'], 'pub_date': post['timestamp']} for post in result ]}


class ForumFeed(FeedProvider):
    __module__ = __name__
    identifier = 'forum'

    def get_feed(self, req, forum_id):
        _ = req.gettext
        try:
            forum_id = int(forum_id)
        except:
            raise FeedNotFound()

        if self.ctx.engine.execute(meta.select([forums.c.forum_id], forums.c.forum_id == forum_id)).fetchone() is None:
            raise FeedNotFound()
        result = self.ctx.engine.execute(meta.select([posts.c.post_id, posts.c.title, posts.c.text, posts.c.timestamp, users.c.username], (posts.c.forum_id == forum_id) & (users.c.user_id == posts.c.author_id), order_by=[meta.desc(posts.c.post_id)], limit=10))
        return {'title': _('Last Posts in Forum %d') % forum_id, 'description': _('The last 10 posts of forum %d') % forum_id, 'items': [ {'title': post['title'], 'link': 'post/%d' % post['post_id'], 'description': parse_and_translate(req, post['text']), 'author': post['username'], 'pub_date': post['timestamp']} for post in result ]}


class RecentChangesFeed(FeedProvider):
    __module__ = __name__
    identifier = 'recent'

    def get_title(self, req):
        _ = req.gettext
        return _('Recent Changes')

    def get_description(self, req):
        _ = req.gettext
        return _('The recent posts')

    def get_feed(self, req, parameter):
        _ = req.gettext
        if parameter:
            raise FeedNotFound()
        result = self.ctx.engine.execute(meta.select([posts.c.post_id, posts.c.title, posts.c.text, posts.c.timestamp, users.c.username], users.c.user_id == posts.c.author_id, order_by=[meta.desc(posts.c.post_id)], limit=10))
        return {'title': _('Recent Changes'), 'description': _('The most recent posts'), 'items': [ {'title': post['title'], 'link': 'post/%d' % post['post_id'], 'description': parse_and_translate(req, post['text']), 'author': post['username'], 'pub_date': post['timestamp']} for post in result ]}


class FeedDisplay(RequestHandler):
    __module__ = __name__
    handler_regexes = ['^feeds/(?P<feed>[a-z0-9_-]+)\\.xml$', '^feeds/(?P<feed>[a-z0-9_-]+)/(?P<parameter>.+)\\.xml$']

    def handle_request(self, req, feed, parameter=None):
        for feed_provider in self.ctx.get_components(FeedProvider):
            if feed_provider.identifier == feed:
                data = feed_provider.get_feed(req, parameter)
                feed = Feed(self.ctx, data['title'], data['description'], self.ctx.make_external_url(''))
                try:
                    for item in data['items']:
                        feed.add_item(**item)

                except FeedNotFound:
                    return PageNotFound()
                else:
                    resp = Response(feed.generate())
                    resp['Content-Type'] = 'text/xml'
                    return resp

        return PageNotFound()