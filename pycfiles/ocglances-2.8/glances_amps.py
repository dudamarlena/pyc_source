# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_amps.py
# Compiled at: 2017-02-11 10:25:25
"""Monitor plugin."""
from ocglances.compat import iteritems
from ocglances.amps_list import AmpsList as glancesAmpsList
from ocglances.plugins.glances_plugin import GlancesPlugin

class Plugin(GlancesPlugin):
    """Glances AMPs plugin."""

    def __init__(self, args=None, config=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.args = args
        self.config = config
        self.display_curse = True
        self.glances_amps = glancesAmpsList(self.args, self.config)
        self.reset()

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update the AMP list."""
        self.reset()
        if self.input_method == 'local':
            for k, v in iteritems(self.glances_amps.update()):
                self.stats.append({'key': k, 'name': v.NAME, 
                   'result': v.result(), 
                   'refresh': v.refresh(), 
                   'timer': v.time_until_refresh(), 
                   'count': v.count(), 
                   'countmin': v.count_min(), 
                   'countmax': v.count_max()})

        return self.stats

    def get_alert(self, nbprocess=0, countmin=None, countmax=None, header='', log=False):
        """Return the alert status relative to the process number."""
        if nbprocess is None:
            return 'OK'
        else:
            if countmin is None:
                countmin = nbprocess
            if countmax is None:
                countmax = nbprocess
            if nbprocess > 0:
                if int(countmin) <= int(nbprocess) <= int(countmax):
                    return 'OK'
                else:
                    return 'WARNING'

            else:
                if int(countmin) == 0:
                    return 'OK'
                else:
                    return 'CRITICAL'

            return

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats or args.disable_process or self.is_disable():
            return ret
        for m in self.stats:
            if m['result'] is None:
                continue
            first_column = ('{}').format(m['name'])
            first_column_style = self.get_alert(m['count'], m['countmin'], m['countmax'])
            second_column = ('{}').format(m['count'])
            for l in m['result'].split('\n'):
                msg = ('{:<16} ').format(first_column)
                ret.append(self.curse_add_line(msg, first_column_style))
                msg = ('{:<4} ').format(second_column)
                ret.append(self.curse_add_line(msg))
                first_column = second_column = ''
                ret.append(self.curse_add_line(l, splittable=True))
                ret.append(self.curse_new_line())

        try:
            ret.pop()
        except IndexError:
            pass

        return ret