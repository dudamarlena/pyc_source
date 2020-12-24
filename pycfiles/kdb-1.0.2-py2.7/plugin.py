# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kdb/plugin.py
# Compiled at: 2014-04-26 09:00:59
"""Base Plugin

This module provides the basic infastructure for kdb
plugins. Plugins should sub-class BasePlugin.
"""
from circuits import BaseComponent

class BasePlugin(BaseComponent):
    channel = 'bot'

    def init(self, bot, data, config):
        self.bot = bot
        self.data = data
        self.config = config