# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/haplugin/alembic/plugin.py
# Compiled at: 2015-02-27 04:04:31
# Size of source mod 2**32: 369 bytes
from hatak.plugin import Plugin
from haplugin.sql import SqlPlugin
from .commands import AlembicCommand, InitDatabase

class AlembicPlugin(Plugin):

    def add_commands(self, parent):
        parent.add_command(AlembicCommand())
        parent.add_command(InitDatabase())

    def add_depedency_plugins(self):
        self.app._validate_dependency_plugin(SqlPlugin)