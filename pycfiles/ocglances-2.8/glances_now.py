# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_now.py
# Compiled at: 2017-02-11 10:25:25
from datetime import datetime
from ocglances.plugins.glances_plugin import GlancesPlugin

class Plugin(GlancesPlugin):
    """Plugin to get the current date/time.

    stats is (string)
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.display_curse = True
        self.align = 'bottom'

    def reset(self):
        """Reset/init the stats."""
        self.stats = ''

    def update(self):
        """Update current date/time."""
        self.stats = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.stats

    def msg_curse(self, args=None):
        """Return the string to display in the curse interface."""
        ret = []
        msg = ('{:23}').format(self.stats)
        ret.append(self.curse_add_line(msg))
        return ret