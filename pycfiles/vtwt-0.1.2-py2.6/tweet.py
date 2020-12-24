# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vtwt/tweet.py
# Compiled at: 2010-07-12 22:43:32
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.plugin import IPlugin
from twisted.python.text import greedyWrap
from zope.interface import implements
from jersey import log
from vtwt import cli

class TweetOptions(cli.Options):

    def parseArgs(self, *tokens):
        self['tweet'] = (' ').join(tokens)
        if not tokens:
            raise cli.UsageError('Nothing to tweet.')


class Tweeter(cli.Command):

    @inlineCallbacks
    def execute(self):
        try:
            text = self.config['tweet']
            msgId = yield self.vtwt.tweet(text)
            wrapped = self._wrapText(text, len(str(msgId)))
            print ('{0}  {1}').format(msgId, wrapped)
        except Exception, e:
            print >> sys.stderr, self.failWhale(e)

    def _wrapText(self, text, paddingLen):
        width = self.config.parent['COLUMNS'] - paddingLen
        joiner = '\n' + str(' ' * paddingLen)
        return joiner.join(greedyWrap(text, width))


class TweetLoader(cli.CommandFactory):
    implements(IPlugin)
    description = 'Tweet something'
    name = 'tweet'
    shortcut = 't'
    options = TweetOptions
    command = Tweeter


loader = TweetLoader()