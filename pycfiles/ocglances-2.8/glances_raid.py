# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_raid.py
# Compiled at: 2017-02-11 10:25:25
"""RAID plugin."""
from ocglances.compat import iterkeys
from ocglances.logger import logger
from ocglances.plugins.glances_plugin import GlancesPlugin
try:
    from pymdstat import MdStat
except ImportError:
    logger.debug('pymdstat library not found. Glances cannot grab RAID info.')

class Plugin(GlancesPlugin):
    """Glances RAID plugin.

    stats is a dict (see pymdstat documentation)
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.display_curse = True
        self.reset()

    def reset(self):
        """Reset/init the stats."""
        self.stats = {}

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update RAID stats using the input method."""
        self.reset()
        if self.input_method == 'local':
            try:
                mds = MdStat()
                self.stats = mds.get_stats()['arrays']
            except Exception as e:
                logger.debug('Can not grab RAID stats (%s)' % e)
                return self.stats

        elif self.input_method == 'snmp':
            pass
        return self.stats

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats:
            return ret
        else:
            msg = ('{:11}').format('RAID disks')
            ret.append(self.curse_add_line(msg, 'TITLE'))
            msg = ('{:>6}').format('Used')
            ret.append(self.curse_add_line(msg))
            msg = ('{:>6}').format('Avail')
            ret.append(self.curse_add_line(msg))
            arrays = sorted(iterkeys(self.stats))
            for array in arrays:
                ret.append(self.curse_new_line())
                status = self.raid_alert(self.stats[array]['status'], self.stats[array]['used'], self.stats[array]['available'])
                array_type = self.stats[array]['type'].upper() if self.stats[array]['type'] is not None else 'UNKNOWN'
                msg = ('{:<5}{:>6}').format(array_type, array)
                ret.append(self.curse_add_line(msg))
                if self.stats[array]['status'] == 'active':
                    msg = ('{:>6}').format(self.stats[array]['used'])
                    ret.append(self.curse_add_line(msg, status))
                    msg = ('{:>6}').format(self.stats[array]['available'])
                    ret.append(self.curse_add_line(msg, status))
                elif self.stats[array]['status'] == 'inactive':
                    ret.append(self.curse_new_line())
                    msg = ('└─ Status {}').format(self.stats[array]['status'])
                    ret.append(self.curse_add_line(msg, status))
                    components = sorted(iterkeys(self.stats[array]['components']))
                    for i, component in enumerate(components):
                        if i == len(components) - 1:
                            tree_char = '└─'
                        else:
                            tree_char = '├─'
                        ret.append(self.curse_new_line())
                        msg = ('   {} disk {}: ').format(tree_char, self.stats[array]['components'][component])
                        ret.append(self.curse_add_line(msg))
                        msg = ('{}').format(component)
                        ret.append(self.curse_add_line(msg))

                if self.stats[array]['used'] < self.stats[array]['available']:
                    ret.append(self.curse_new_line())
                    msg = '└─ Degraded mode'
                    ret.append(self.curse_add_line(msg, status))
                    if len(self.stats[array]['config']) < 17:
                        ret.append(self.curse_new_line())
                        msg = ('   └─ {}').format(self.stats[array]['config'].replace('_', 'A'))
                        ret.append(self.curse_add_line(msg))

            return ret

    def raid_alert(self, status, used, available):
        """RAID alert messages.

        [available/used] means that ideally the array may have _available_
        devices however, _used_ devices are in use.
        Obviously when used >= available then things are good.
        """
        if status == 'inactive':
            return 'CRITICAL'
        else:
            if used is None or available is None:
                return 'DEFAULT'
            if used < available:
                return 'WARNING'
            return 'OK'