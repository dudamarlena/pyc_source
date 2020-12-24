# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vtwt/following.py
# Compiled at: 2010-06-09 19:13:06
import sys
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.plugin import IPlugin
from zope.interface import implements
from jersey import log
from vtwt import cli

class FollowingOptions(cli.Options):
    optFlags = [
     [
      'long', 'l', 'Print more user information.']]


class Following(cli.Command):

    @inlineCallbacks
    def execute(self):
        try:
            friends = yield self.vtwt.getFollowees()
            self._printFriends(friends)
        except Exception, e:
            print >> sys.stderr, self.failWhale(e)
            raise SystemError(1)

    def _printFriends(self, friends):
        for friend in friends:
            self._printFriend(friend)

    def _printFriend(self, friend):
        if self.config['long']:
            fmt = '{0.screen_name} ({0.name})'
        else:
            fmt = '{0.screen_name}'
        print fmt.format(friend)


class FollowingLoader(cli.CommandFactory):
    implements(IPlugin)
    description = 'List friends'
    name = 'following'
    shortcut = 'F'
    options = FollowingOptions
    command = Following


loader = FollowingLoader()