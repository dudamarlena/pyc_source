# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vtwt/followers.py
# Compiled at: 2010-06-09 19:13:03
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.plugin import IPlugin
from zope.interface import implements
from jersey import log
from vtwt import cli

class FollowersOptions(cli.Options):
    optFlags = [
     [
      'long', 'l', 'Print more user information.']]


class Followers(cli.Command):

    @inlineCallbacks
    def execute(self):
        try:
            followers = yield self.vtwt.getFollowers()
        except Exception, e:
            print >> sys.stderr, self.failWhale(e)
        else:
            self._printFollowers(followers)

    def _printFollowers(self, followers):
        for follower in followers:
            self._printFollower(follower)

    def _printFollower(self, follower):
        if self.config['long']:
            followerFmt = '{0.screen_name} ({0.name})'
        else:
            followerFmt = '{0.screen_name}'
        print followerFmt.format(follower)


class FollowersLoader(cli.CommandFactory):
    implements(IPlugin)
    description = 'List followers'
    name = 'followers'
    shortcut = None
    options = FollowersOptions
    command = Followers


loader = FollowersLoader()