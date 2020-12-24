# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/nacl/feeds.py
# Compiled at: 2007-12-02 16:26:59
from salamoia.h2o.feedcollection import FeedCollection
from salamoia.h2o.logioni import Ione
from salamoia.h2o.container import Container

class FeedControl(object):
    __module__ = __name__

    def __init__(self):
        self.feeds = FeedCollection('/tmp/news.db')
        Ione.log('FeedControl init')
        super(FeedControl, self).__init__()

    def getNewsCollection(self, user):
        Ione.log('NewsCollection request for user ' + user)
        return Container(self.feeds.getFeed(user))

    def getNewsList(self, user):
        Ione.log('List of news request for ' + user)
        feed = self.feeds.getFeed(user)
        return feed.list()

    def getNews(self, user, title):
        Ione.log('NewsCollection request for user ' + user)
        feed = self.feeds.getFeed(user)
        return feed[title]


from salamoia.tests import *
runDocTests()