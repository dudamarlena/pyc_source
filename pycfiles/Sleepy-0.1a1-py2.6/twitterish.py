# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-i386/egg/sleepy/twitterish.py
# Compiled at: 2011-04-03 15:26:03
import twitter
from sleepy.shorties import Ago
from sleepy.lonsies import Entries

class Tweet(object):

    def __init__(self, d, user=None, use_cache=True):
        self.published = d.published
        self.message = d.text

    @property
    def ago(self):
        return Ago(self.published)


posts = Entries(entry_class=Tweet, user_config_key='twitter_user', cache_name='twitter_posts', createfunc=lambda user: twitter.Api().GetUserTimeline(user))