# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/command/list.py
# Compiled at: 2015-02-16 11:14:43
# Size of source mod 2**32: 771 bytes
import os, glob
from . import Command
from . import CommandError
from ..package import find_package

class ListCommand(Command):
    __doc__ = 'This class extends :class:`Command` and implement the ``list``\n    command used by drove client to list installed plugins.\n    '

    def execute(self):
        plugin_dir = self.config.get('plugin_dir', None)
        if not plugin_dir:
            raise CommandError('Missing plugin_dir in configuration')
        for pkg in find_package(path=plugin_dir):
            self.log.info(str(pkg))