# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vtwt/unfollow.py
# Compiled at: 2010-06-09 19:13:13
import os, sys
from twisted.internet.defer import inlineCallbacks
from twisted.plugin import IPlugin
from zope.interface import implements
from jersey import log
from vtwt import cli

class UnFollowOptions(cli.Options):

    def parseArgs(self, *names):
        if not names:
            raise usage.error('No one to unfollow ;(')
        self['losers'] = names


class UnFollower(cli.Command):

    @inlineCallbacks
    def execute(self):
        users = []
        for loser in self.config['losers']:
            try:
                user = yield self.vtwt.unfollow(loser)
            except Exception, e:
                print >> sys.stderr, self.failWhale(e)
            else:
                self._printLoser(loser)

    def _printLoser(self, user):
        print ('{u}').format(c=self.config, u=user)


class UnFollowLoader(cli.CommandFactory):
    implements(IPlugin)
    description = 'Un-follow the given user'
    name = 'unfollow'
    shortcut = 'u'
    options = UnFollowOptions
    command = UnFollower


loader = UnFollowLoader()