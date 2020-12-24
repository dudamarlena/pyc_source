# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/haplugin/toster/plugin.py
# Compiled at: 2014-09-29 16:39:03
# Size of source mod 2**32: 287 bytes
from hatak.plugin import Plugin
from .commands import TosterCommand

class TosterPlugin(Plugin):

    def __init__(self, fixtures):
        super().__init__()
        self.fixtures = fixtures

    def add_commands(self, parent):
        parent.add_command(TosterCommand(self.fixtures))