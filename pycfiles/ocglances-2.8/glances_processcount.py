# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_processcount.py
# Compiled at: 2017-02-11 10:25:25
"""Process count plugin."""
from ocglances.processes import glances_processes
from ocglances.plugins.glances_plugin import GlancesPlugin

class Plugin(GlancesPlugin):
    """Glances process count plugin.

    stats is a list
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.display_curse = True

    def reset(self):
        """Reset/init the stats."""
        self.stats = {}

    def update(self):
        """Update processes stats using the input method."""
        self.reset()
        if self.input_method == 'local':
            glances_processes.update()
            self.stats = glances_processes.getcount()
        elif self.input_method == 'snmp':
            pass
        return self.stats

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if args.disable_process:
            msg = "PROCESSES DISABLED (press 'z' to display)"
            ret.append(self.curse_add_line(msg))
            return ret
        else:
            if not self.stats:
                return ret
            if glances_processes.process_filter is not None:
                msg = 'Processes filter:'
                ret.append(self.curse_add_line(msg, 'TITLE'))
                msg = (' {} ').format(glances_processes.process_filter)
                if glances_processes.process_filter_key is not None:
                    msg += ('on column {} ').format(glances_processes.process_filter_key)
                ret.append(self.curse_add_line(msg, 'FILTER'))
                msg = "('ENTER' to edit, 'E' to reset)"
                ret.append(self.curse_add_line(msg))
                ret.append(self.curse_new_line())
            msg = 'TASKS'
            ret.append(self.curse_add_line(msg, 'TITLE'))
            other = self.stats['total']
            msg = ('{:>4}').format(self.stats['total'])
            ret.append(self.curse_add_line(msg))
            if 'thread' in self.stats:
                msg = (' ({} thr),').format(self.stats['thread'])
                ret.append(self.curse_add_line(msg))
            if 'running' in self.stats:
                other -= self.stats['running']
                msg = (' {} run,').format(self.stats['running'])
                ret.append(self.curse_add_line(msg))
            if 'sleeping' in self.stats:
                other -= self.stats['sleeping']
                msg = (' {} slp,').format(self.stats['sleeping'])
                ret.append(self.curse_add_line(msg))
            msg = (' {} oth ').format(other)
            ret.append(self.curse_add_line(msg))
            if glances_processes.auto_sort:
                msg = 'sorted automatically'
                ret.append(self.curse_add_line(msg))
                msg = (' by {}').format(glances_processes.sort_key)
                ret.append(self.curse_add_line(msg))
            else:
                msg = ('sorted by {}').format(glances_processes.sort_key)
                ret.append(self.curse_add_line(msg))
            ret[(-1)]['msg'] += ', %s view' % ('tree' if glances_processes.is_tree_enabled() else 'flat')
            return ret