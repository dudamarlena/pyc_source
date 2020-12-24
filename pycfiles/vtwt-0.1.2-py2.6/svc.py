# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vtwt/svc.py
# Compiled at: 2010-07-12 20:04:40
import os, sys
from twisted.application.service import Service
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from oauth import oauth
from jersey import log
from twittytwister.twitter import TwitterFeed
from vtwt.util import recodeText

class VtwtService(Service):
    oauthConsumer = oauth.OAuthConsumer('xkCemphqejlUZ9W11MUMsA', 'QsnJx6SDhH6SjWNG95jcUR3FnKyFWFoOvDcf90E')
    baseUrl = 'https://api.twitter.com'

    def __init__(self, accessToken):
        self.name = ('vtwt:{0}').format(accessToken.key)
        self.accessToken = accessToken
        self._twt = self._buildTwitterClient(accessToken)

    def _buildTwitterClient(self, token):
        return TwitterFeed(consumer=self.oauthConsumer, token=token, base_url=self.baseUrl)

    @inlineCallbacks
    def getTimeline(self, user=None, params={}):
        """Get recent updates from a user's timeline.
        """
        log.trace(('Getting {0} timeline').format(user or 'home'))
        messages = []

        def addMessage(msg):
            msg.text = self._recodeText(msg.text)
            messages.insert(0, msg)

        if user in (None, 'home'):
            yield self._twt.home_timeline(addMessage, params)
        else:
            yield self._twt.user_timeline(addMessage, user, params)
        returnValue(messages)
        return

    def _recodeText(self, text):
        """Recode HTML entities refs; e.g. '&amp;' to '&'
        
        Work around buggy Twitter clients that mangle retweets such that
        &amp;lt;3 recodes to <3 (instead of &lt;3).
        """
        return recodeText(recodeText(text))

    def tweet(self, text):
        return self._twt.update(text)

    @inlineCallbacks
    def retweet(self, msgId):
        msgs = []
        yield self._twt.retweet(msgId, msgs.append)
        returnValue(msgs[0])

    @inlineCallbacks
    def follow(self, user):
        """Follow a user.  Return a dictionary representing the user.
        """
        users = []
        yield self._twt.follow_user(user, users.append)
        returnValue(users[0])

    @inlineCallbacks
    def unfollow(self, user):
        """Unfollow a user.  Return a dictionary representing the user.
        """
        users = []
        yield self._twt.unfollow_user(user, users.append)
        returnValue(users[0])

    def block(self, user):
        """Block a user.
        """
        users = []
        return self._twt.block(user)

    def unblock(self, user):
        """Unblock a user.
        """
        return self._twt.unblock(user)

    @inlineCallbacks
    def getFollowers(self, user=None):
        """Get a list of followers (optionally, for another user).
        """
        followers = []
        yield self._twt.list_followers(lambda f: followers.insert(0, f), user)
        returnValue(followers)

    @inlineCallbacks
    def getFollowees(self, user=None):
        """Get a list of users following 
        """
        followees = []
        yield self._twt.list_friends(lambda f: followees.insert(0, f), user)
        returnValue(followees)