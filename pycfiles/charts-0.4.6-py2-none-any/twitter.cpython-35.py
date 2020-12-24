# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\Remote\chartpy\chartpy\twitter.py
# Compiled at: 2018-01-30 05:54:38
# Size of source mod 2**32: 1957 bytes
from __future__ import division
__author__ = 'saeedamen'
from twython import Twython
from chartpy.chartconstants import ChartConstants
cc = ChartConstants()

class Twitter:

    def __init__(self, *args, **kwargs):
        pass

    def set_key(self, TWITTER_APP_KEY, TWITTER_APP_SECRET, TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_TOKEN_SECRET):
        self.twitter = Twython(TWITTER_APP_KEY, TWITTER_APP_SECRET, TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_TOKEN_SECRET)

    def auto_set_key(self):
        self.twitter = Twython(cc.TWITTER_APP_KEY, cc.TWITTER_APP_SECRET, cc.TWITTER_OAUTH_TOKEN, cc.TWITTER_OAUTH_TOKEN_SECRET)

    def update_status(self, msg, link=None, picture=None):
        chars_lim = 140
        if link is not None:
            chars_lim = chars_lim - 22 * link
        if picture is not None:
            chars_lim = chars_lim - 23
        if len(msg) > chars_lim:
            return
        if picture is None:
            self.twitter.update_status(status=msg)
        else:
            photo = open(picture, 'rb')
            response = self.twitter.upload_media(media=photo)
            self.twitter.update_status(status=msg, media_ids=[response['media_id']])