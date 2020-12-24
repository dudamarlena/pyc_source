# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./log.py
# Compiled at: 2015-02-18 10:58:13
"""Internal write plugin which log all values and
events using ``DEBUG`` severity.
"""
from drove.plugin import Plugin

class LogPlugin(Plugin):

    def write(self, channel):
        for data in channel.receive('internal.log'):
            self.log.debug(str(data))