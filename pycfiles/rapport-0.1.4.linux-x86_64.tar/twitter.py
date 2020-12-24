# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/rapport/plugins/twitter.py
# Compiled at: 2013-05-14 04:37:04
"""
Twitter plugin.
"""
import tweepy, rapport.plugin

class TwitterPlugin(rapport.plugin.Plugin):

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, *args, **kwargs):
        super(TwitterPlugin, self).__init__(*args, **kwargs)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def _get(self, timeline, timeframe):
        count = 50
        statuses = []
        for status in timeline(count=count):
            if timeframe.contains(status.created_at):
                statuses.append(status)

        return statuses

    def collect(self, timeframe):
        mentions = self._get(self.api.mentions_timeline, timeframe)
        tweets = self._get(self.api.user_timeline, timeframe)
        retweets = self._get(self.api.retweets_of_me, timeframe)
        return self._results({'mentions': mentions, 'tweets': tweets, 
           'retweets': retweets})


rapport.plugin.register('twitter', TwitterPlugin)