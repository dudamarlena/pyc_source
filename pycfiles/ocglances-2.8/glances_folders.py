# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_folders.py
# Compiled at: 2017-02-11 10:25:25
"""Folder plugin."""
import numbers
from ocglances.folder_list import FolderList as glancesFolderList
from ocglances.plugins.glances_plugin import GlancesPlugin

class Plugin(GlancesPlugin):
    """Glances folder plugin."""

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.display_curse = True
        self.glances_folders = None
        self.reset()
        return

    def get_key(self):
        """Return the key of the list."""
        return 'path'

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

    def load_limits(self, config):
        """Load the foldered list from the config file, if it exists."""
        self.glances_folders = glancesFolderList(config)

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update the foldered list."""
        self.reset()
        if self.input_method == 'local':
            if self.glances_folders is None:
                return self.stats
            self.glances_folders.update()
            self.stats = self.glances_folders.get()
        return self.stats

    def get_alert(self, stat):
        """Manage limits of the folder list"""
        if not isinstance(stat['size'], numbers.Number):
            return 'DEFAULT'
        else:
            ret = 'OK'
            if stat['critical'] is not None and stat['size'] > int(stat['critical']) * 1000000:
                ret = 'CRITICAL'
            elif stat['warning'] is not None and stat['size'] > int(stat['warning']) * 1000000:
                ret = 'WARNING'
            elif stat['careful'] is not None and stat['size'] > int(stat['careful']) * 1000000:
                ret = 'CAREFUL'
            return ret

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats or self.is_disable():
            return ret
        msg = ('{}').format('FOLDERS')
        ret.append(self.curse_add_line(msg, 'TITLE'))
        for i in self.stats:
            ret.append(self.curse_new_line())
            if len(i['path']) > 15:
                path = '_' + i['path'][-14:]
            else:
                path = i['path']
            msg = ('{:<16} ').format(path)
            ret.append(self.curse_add_line(msg))
            try:
                msg = ('{:>6}').format(self.auto_unit(i['size']))
            except (TypeError, ValueError):
                msg = ('{:>6}').format(i['size'])

            ret.append(self.curse_add_line(msg, self.get_alert(i)))

        return ret