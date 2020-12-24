# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vtwt/follow.py
# Compiled at: 2010-07-11 04:27:43
import sys
from twisted.internet.defer import inlineCallbacks
from twisted.plugin import IPlugin
from zope.interface import implements
from jersey import log
from vtwt import cli

class FollowOptions(cli.Options):

    def parseArgs(self, *names):
        if not names:
            raise cli.UsageError('No one to follow ;(')
        self['friends'] = names


class Follower(cli.Command):

    @inlineCallbacks
    def execute(self):
        users = []
        for friend in self.config['friends']:
            try:
                user = yield self.vtwt.follow(friend)
                self._printFollowee(user)
            except Exception, e:
                print >> sys.stderr, self.failWhale(e)

    def _printFollowee(self, user):
        print ('{u.screen_name}').format(c=self.config, u=user)


class FollowLoader(cli.CommandFactory):
    implements(IPlugin)
    description = 'Follow the given user'
    name = 'follow'
    shortcut = 'f'
    options = FollowOptions
    command = Follower


loader = FollowLoader()