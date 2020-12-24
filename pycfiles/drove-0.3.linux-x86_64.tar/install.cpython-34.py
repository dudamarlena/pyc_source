# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/command/install.py
# Compiled at: 2015-02-25 04:28:20
# Size of source mod 2**32: 1942 bytes
import os
from . import Command
from . import CommandError
from ..package import Package

class InstallCommand(Command):
    __doc__ = 'This class extends :class:`Command` and implement the ``install``\n    command used by drove client to install plugins.\n    '

    def execute(self):
        plugin_dir = self.config.get('plugin_dir', None)
        plugin = self.args.plugin
        upgrade = self.args.upgrade
        index_url = self.args.index_url or self.config.get('catalog.url', 'https://plugins.drove.io').strip('/')
        install_global = self.args.install_global
        if not plugin_dir:
            raise CommandError("'plugin_dir' is not configured")
        if install_global:
            plugin_dir = os.path.expanduser(plugin_dir[(-1)])
        else:
            plugin_dir = os.path.expanduser(plugin_dir[0])
        if plugin.split('://')[0] in ('http', 'https', 'ftp'):
            package = Package.from_url(plugin, plugin_dir, upgrade)
        else:
            if os.path.exists(plugin) and os.path.isfile(plugin):
                if plugin.endswith('.tar.gz'):
                    package = Package.from_tarball(plugin, plugin_dir, upgrade)
                else:
                    raise CommandError('Provided package file is not a tarball')
            else:
                package = Package.from_repo(plugin, plugin_dir, index_url, upgrade)
        self.log.info('Installed package successfully [%s]:%s' % (
         package.name, package.version[0:6]))