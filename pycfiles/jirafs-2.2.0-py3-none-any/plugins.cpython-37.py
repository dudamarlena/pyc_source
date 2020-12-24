# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/plugins.py
# Compiled at: 2020-01-13 00:37:20
# Size of source mod 2**32: 3687 bytes
from blessings import Terminal
from jirafs import utils
from jirafs.plugin import CommandPlugin

class Command(CommandPlugin):
    __doc__ = ' Enable/Disable or display information about installed issue plugins '
    MIN_VERSION = '2.0.0'
    MAX_VERSION = '3.0.0'

    def handle(self, args, folder, parser, **kwargs):
        installed_plugins = utils.get_installed_plugins()
        if args.disabled_only:
            if args.enabled_only:
                parser.error('--disabled-only and --enabled-only are mutually exclusive.')
        if args.enable:
            if args.enable not in installed_plugins:
                parser.error("Plugin '%s' is not installed." % args.enable)
        return self.cmd(folder, args)

    def add_arguments(self, parser):
        parser.add_argument('--verbose', action='store_true', default=False)
        parser.add_argument('--enabled-only',
          dest='enabled_only', action='store_true', default=False)
        parser.add_argument('--disabled-only',
          dest='disabled_only', action='store_true', default=False)
        parser.add_argument('--enable',
          type=str)
        parser.add_argument('--disable',
          type=str)
        parser.add_argument('--global',
          dest='set_global', default=False, action='store_true')

    def build_plugin_dict(self, enabled, available):
        all_plugins = {}
        for plugin_name, cls in available.items():
            all_plugins[plugin_name] = {'enabled':False, 
             'class':cls}

        for plugin_instance in enabled:
            plugin_name = plugin_instance.plugin_name
            all_plugins[plugin_name]['enabled'] = True
            all_plugins[plugin_name]['instance'] = plugin_instance

        return all_plugins

    def main(self, folder, args):
        t = Terminal()
        enabled_plugins = folder.load_plugins()
        available_plugins = utils.get_installed_plugins()
        if args.enable:
            if args.set_global:
                utils.set_global_config_value('plugins', args.enable, 'enabled')
            else:
                folder.set_config_value('plugins', args.enable, 'enabled')
        else:
            if args.disable:
                if args.set_global:
                    utils.set_global_config_value('plugins', args.disable, 'disabled')
                else:
                    folder.set_config_value('plugins', args.disable, 'disabled')
            else:
                all_plugins = self.build_plugin_dict(enabled_plugins, available_plugins)
                for plugin_name, plugin_data in all_plugins.items():
                    if plugin_data['enabled']:
                        if args.disabled_only:
                            continue
                        else:
                            if not plugin_data['enabled']:
                                if args.enabled_only:
                                    continue
                            if plugin_data['enabled']:
                                color = t.bold
                            else:
                                color = t.normal
                        print(color + plugin_name + t.normal + (' (Enabled)' if plugin_data['enabled'] else ' (Disabled; enable by running `jirafs plugins --enable=%s`)' % plugin_name))
                        if args.verbose:
                            doc_string = plugin_data['class'].__doc__.strip().split('\n')
                            for line in doc_string:
                                print('     %s' % line)