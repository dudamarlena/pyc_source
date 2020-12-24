# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/twitter/get_public_timeline.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from command import TwitterCommand
from exception import TwitterAPIException

class GetPublicTimeLine(TwitterCommand):
    __domain__ = 'twitter'
    __operation__ = 'get-public-timeline'
    mode = None

    def __init__(self):
        TwitterCommand.__init__(self)

    def parse_parameters(self, **params):
        TwitterCommand.parse_parameters(self, **params)

    def run(self):
        self.get_twitter_connection()
        self._result = self.get_public_timeline()