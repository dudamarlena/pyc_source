# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/command/remove.py
# Compiled at: 2015-02-16 11:20:10
# Size of source mod 2**32: 717 bytes
from . import Command
from . import CommandError
from ..package import Package, find_package

class RemoveCommand(Command):
    __doc__ = 'Remove an installed plugin'

    def execute(self):
        plugin = self.args.plugin
        if '.' not in plugin:
            raise CommandError('plugin must contain almost author.plugin')
        plugin_dir = self.config.get('plugin_dir', None)
        if not plugin_dir or len(plugin_dir) == 0:
            raise CommandError('Missing plugin_dir in configuration')
        for x in find_package(path=plugin_dir, pattern=plugin):
            self.log.info('Removed plugin %s' % (str(x),))
            x.remove()