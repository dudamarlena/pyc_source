# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vtwt/block.py
# Compiled at: 2010-06-09 19:12:53
import sys
from twisted.internet.defer import inlineCallbacks, gatherResults
from twisted.plugin import IPlugin
from twisted.python import usage
from zope.interface import implements
from jersey import log
from vtwt import cli

class BlockOptions(cli.Options):

    def parseArgs(self, *names):
        if not names:
            raise usage.error('No one to block ;(')
        self['blockees'] = names


class Blocker(cli.Command):

    @inlineCallbacks
    def execute(self):
        for blockee in self.config['blockees']:
            try:
                yield self._block(blockee)
            except Exception, e:
                print >> sys.stderr, self.failWhale(e)

    @inlineCallbacks
    def _block(self, user):
        yield self.vtwt.block(user)
        print ('{0}').format(user)


class BlockLoader(cli.CommandFactory):
    implements(IPlugin)
    description = 'Block the given user'
    name = 'block'
    shortcut = 'B'
    options = BlockOptions
    command = Blocker


loader = BlockLoader()