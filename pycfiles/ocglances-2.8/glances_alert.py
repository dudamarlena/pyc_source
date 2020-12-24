# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_alert.py
# Compiled at: 2017-02-11 10:25:25
"""Alert plugin."""
from datetime import datetime
from ocglances.logs import glances_logs
from ocglances.plugins.glances_plugin import GlancesPlugin

class Plugin(GlancesPlugin):
    """Glances alert plugin.

    Only for display.
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.display_curse = True
        self.align = 'bottom'
        self.reset()

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

    def update(self):
        """Nothing to do here. Just return the global glances_log."""
        self.stats = glances_logs.get()

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats and self.is_disable():
            return ret
        if not self.stats:
            msg = 'No warning or critical alert detected'
            ret.append(self.curse_add_line(msg, 'TITLE'))
        else:
            msg = 'Warning or critical alerts'
            ret.append(self.curse_add_line(msg, 'TITLE'))
            logs_len = glances_logs.len()
            if logs_len > 1:
                msg = (' (last {} entries)').format(logs_len)
            else:
                msg = ' (one entry)'
            ret.append(self.curse_add_line(msg, 'TITLE'))
            for alert in self.stats:
                ret.append(self.curse_new_line())
                msg = str(datetime.fromtimestamp(alert[0]))
                ret.append(self.curse_add_line(msg))
                if alert[1] > 0:
                    msg = (' ({})').format(datetime.fromtimestamp(alert[1]) - datetime.fromtimestamp(alert[0]))
                else:
                    msg = ' (ongoing)'
                ret.append(self.curse_add_line(msg))
                ret.append(self.curse_add_line(' - '))
                if alert[1] > 0:
                    msg = ('{} on {}').format(alert[2], alert[3])
                    ret.append(self.curse_add_line(msg))
                else:
                    msg = str(alert[3])
                    ret.append(self.curse_add_line(msg, decoration=alert[2]))
                if self.approx_equal(alert[6], alert[4], tolerance=0.1):
                    msg = (' ({:.1f})').format(alert[5])
                else:
                    msg = (' (Min:{:.1f} Mean:{:.1f} Max:{:.1f})').format(alert[6], alert[5], alert[4])
                ret.append(self.curse_add_line(msg))
                top_process = (', ').join([ p['name'] for p in alert[9] ])
                if top_process != '':
                    msg = (': {}').format(top_process)
                    ret.append(self.curse_add_line(msg))

        return ret

    def approx_equal(self, a, b, tolerance=0.0):
        """Compare a with b using the tolerance (if numerical)."""
        if str(int(a)).isdigit() and str(int(b)).isdigit():
            return abs(a - b) <= max(abs(a), abs(b)) * tolerance
        else:
            return a == b