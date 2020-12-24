# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skypond/games/base/base_agent.py
# Compiled at: 2019-04-24 23:04:10
from __future__ import absolute_import

class Agent:

    def __init__(self):
        self.blind = False

    def react(self, observation):
        raise NotImplementedError('implement react in your agent')

    def describe(self):
        raise NotImplementedError('implement describe in your agent')