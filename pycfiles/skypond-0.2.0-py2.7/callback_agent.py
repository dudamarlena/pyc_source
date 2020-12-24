# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skypond/games/base/callback_agent.py
# Compiled at: 2019-05-01 22:23:33
from __future__ import absolute_import
from .base_agent import Agent

class CallbackAgent(Agent):

    def __init__(self, react_callback):
        super().__init__()
        self.react_callback = react_callback

    def react(self, observation):
        return self.react_callback(observation)

    def describe(self):
        return dict(username='shim')