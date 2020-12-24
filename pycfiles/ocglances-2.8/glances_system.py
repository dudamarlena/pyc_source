# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_system.py
# Compiled at: 2017-02-11 10:25:25
"""System plugin."""
import os, platform, re
from io import open
from ocglances.compat import iteritems
from ocglances.plugins.glances_plugin import GlancesPlugin
snmp_oid = {'default': {'hostname': '1.3.6.1.2.1.1.5.0', 'system_name': '1.3.6.1.2.1.1.1.0'}, 
   'netapp': {'hostname': '1.3.6.1.2.1.1.5.0', 'system_name': '1.3.6.1.2.1.1.1.0', 
              'platform': '1.3.6.1.4.1.789.1.1.5.0'}}
snmp_to_human = {'windows': {'Windows Version 10.0': 'Windows 10 or Server 2016', 'Windows Version 6.3': 'Windows 8.1 or Server 2012R2', 
               'Windows Version 6.2': 'Windows 8 or Server 2012', 
               'Windows Version 6.1': 'Windows 7 or Server 2008R2', 
               'Windows Version 6.0': 'Windows Vista or Server 2008', 
               'Windows Version 5.2': 'Windows XP 64bits or 2003 server', 
               'Windows Version 5.1': 'Windows XP', 
               'Windows Version 5.0': 'Windows 2000'}}

def _linux_os_release():
    """Try to determine the name of a Linux distribution.

    This function checks for the /etc/os-release file.
    It takes the name from the 'NAME' field and the version from 'VERSION_ID'.
    An empty string is returned if the above values cannot be determined.
    """
    pretty_name = ''
    ashtray = {}
    keys = ['NAME', 'VERSION_ID']
    try:
        with open(os.path.join('/etc', 'os-release')) as (f):
            for line in f:
                for key in keys:
                    if line.startswith(key):
                        ashtray[key] = re.sub('^"|"$', '', line.strip().split('=')[1])

    except (OSError, IOError):
        return pretty_name

    if ashtray:
        if 'NAME' in ashtray:
            pretty_name = ashtray['NAME']
        if 'VERSION_ID' in ashtray:
            pretty_name += (' {}').format(ashtray['VERSION_ID'])
    return pretty_name


class Plugin(GlancesPlugin):
    """Glances' host/system plugin.

    stats is a dict
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
        """Update the host/system info using the input method.

        Return the stats (dict)
        """
        self.reset()
        if self.input_method == 'local':
            self.stats['os_name'] = platform.system()
            self.stats['hostname'] = platform.node()
            self.stats['platform'] = platform.architecture()[0]
            if self.stats['os_name'] == 'Linux':
                try:
                    linux_distro = platform.linux_distribution()
                except AttributeError:
                    self.stats['linux_distro'] = _linux_os_release()

                if linux_distro[0] == '':
                    self.stats['linux_distro'] = _linux_os_release()
                else:
                    self.stats['linux_distro'] = (' ').join(linux_distro[:2])
                self.stats['os_version'] = platform.release()
            elif self.stats['os_name'].endswith('BSD') or self.stats['os_name'] == 'SunOS':
                self.stats['os_version'] = platform.release()
            elif self.stats['os_name'] == 'Darwin':
                self.stats['os_version'] = platform.mac_ver()[0]
            elif self.stats['os_name'] == 'Windows':
                os_version = platform.win32_ver()
                self.stats['os_version'] = (' ').join(os_version[::2])
                if self.stats['platform'] == '32bit' and 'PROCESSOR_ARCHITEW6432' in os.environ:
                    self.stats['platform'] = '64bit'
            else:
                self.stats['os_version'] = ''
            if self.stats['os_name'] == 'Linux':
                self.stats['hr_name'] = self.stats['linux_distro']
            else:
                self.stats['hr_name'] = ('{} {}').format(self.stats['os_name'], self.stats['os_version'])
            self.stats['hr_name'] += (' {}').format(self.stats['platform'])
        elif self.input_method == 'snmp':
            try:
                self.stats = self.get_stats_snmp(snmp_oid=snmp_oid[self.short_system_name])
            except KeyError:
                self.stats = self.get_stats_snmp(snmp_oid=snmp_oid['default'])

            self.stats['os_name'] = self.stats['system_name']
            if self.short_system_name == 'windows':
                for r, v in iteritems(snmp_to_human['windows']):
                    if re.search(r, self.stats['system_name']):
                        self.stats['os_name'] = v
                        break

            self.stats['hr_name'] = self.stats['os_name']
        return self.stats

    def msg_curse(self, args=None):
        """Return the string to display in the curse interface."""
        ret = []
        if args.client:
            if args.cs_status.lower() == 'connected':
                msg = 'Connected to '
                ret.append(self.curse_add_line(msg, 'OK'))
            elif args.cs_status.lower() == 'snmp':
                msg = 'SNMP from '
                ret.append(self.curse_add_line(msg, 'OK'))
            elif args.cs_status.lower() == 'disconnected':
                msg = 'Disconnected from '
                ret.append(self.curse_add_line(msg, 'CRITICAL'))
        msg = self.stats['hostname']
        ret.append(self.curse_add_line(msg, 'TITLE'))
        if self.stats['os_name'] == 'Linux' and self.stats['linux_distro']:
            msg = (' ({} {} / {} {})').format(self.stats['linux_distro'], self.stats['platform'], self.stats['os_name'], self.stats['os_version'])
        else:
            try:
                msg = (' ({} {} {})').format(self.stats['os_name'], self.stats['os_version'], self.stats['platform'])
            except Exception:
                msg = (' ({})').format(self.stats['os_name'])

        ret.append(self.curse_add_line(msg, optional=True))
        return ret