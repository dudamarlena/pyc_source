# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/twitter/send_tweet.py
# Compiled at: 2012-10-12 07:02:39
from coils.foundation import *
from coils.core import *
from command import TwitterCommand

class TweetCommand(TwitterCommand):
    __domain__ = 'twitter'
    __operation__ = 'tweet'

    def __init__(self):
        TwitterCommand.__init__(self)

    def parse_parameters(self, **params):
        TwitterCommand.parse_parameters(self, **params)

    def run(self):
        self._result = False