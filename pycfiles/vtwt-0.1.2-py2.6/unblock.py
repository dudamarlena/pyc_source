# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vtwt/unblock.py
# Compiled at: 2010-06-09 19:13:11
import sys
from twisted.internet.defer import inlineCallbacks, gatherResults
from twisted.plugin import IPlugin
from twisted.python import usage
from zope.interface import implements
from jersey import log
from vtwt import cli

class UnBlockOptions(cli.Options):

    def parseArgs(self, *names):
        if not names:
            raise usage.error('No one to unblock ;(')
        self['unblockees'] = names


class UnBlocker(cli.Command):

    @inlineCallbacks
    def execute(self):
        for unblockee in self.config['unblockees']:
            try:
                yield self._unblock(unblockee)
            except Exception, e:
                print >> sys.stderr, self.failWhale(e)

    @inlineCallbacks
    def _unblock(self, user):
        yield self.vtwt.unblock(user)
        print ('{0}').format(user)


class UnBlockLoader(cli.CommandFactory):
    implements(IPlugin)
    description = 'Un-block the given user'
    name = 'unblock'
    shortcut = 'B'
    options = UnBlockOptions
    command = UnBlocker


loader = UnBlockLoader()