# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_modprobe.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.modprobe import ModProbe
from insights.tests import context_wrap
MODPROBE_CONF = ('\noptions ipv6 disable=1\noptions mlx4_core debug_level=1 log_num_mgm_entry_size=-1\n\ninstall ipv6 /bin/true\n').strip()
MODPROBE_CONF_PATH = 'etc/modprobe.conf'
MOD_OPTION_INFO = ('\noptions ipv6 disable=1\noptions mlx4_core debug_level=1 log_num_mgm_entry_size=-1\n\ninstall ipv6 /bin/true\n').strip()
MOD_OPTION_INFO_PATH = 'etc/modprobe.d/ipv6.conf'
MOD_COMPLETE = ("\n#\n# Syntax: see modprobe.conf(5).\n#\n\n# aliases\nalias en* bnx2\nalias eth* bnx2\nalias scsi_hostadapter megaraid_sas\nalias scsi_hostadapter1 ata_piix\n\n# watchdog drivers\nblacklist i8xx_tco\n\n# Don't install the Firewire ethernet driver\ninstall eth1394 /bin/true\n\n# Special handling for USB mouse\ninstall usbmouse /sbin/modprobe --first-time --ignore-install usbmouse && { /sbin/modprobe hid; /bin/true; }\nremove usbmouse { /sbin/modprobe -r hid; } ; /sbin/modprobe -r --first-time --ignore-remove usbmouse\n\n# bonding options\noptions bonding max_bonds=2\noptions bnx2 disable_msi=1\n\n# Test bad data - save in bad_lines\nalias\nalias scsi_hostadapter2 ata_piix failed comment\nbalclkist ieee80211\n").strip()
MOD_COMPLETE_PATH = 'etc/modprobe.conf'

def test_modprobe_v1():
    modprobe_info = ModProbe(context_wrap(MOD_OPTION_INFO, path=MOD_OPTION_INFO_PATH))
    assert modprobe_info['options'].get('ipv6') == ['disable=1']
    assert modprobe_info['options'].get('mlx4_core')[0] == 'debug_level=1'
    assert modprobe_info['install'].get('ipv6') == ['/bin/true']


def test_modprobe_v2():
    modprobe_info = ModProbe(context_wrap(MODPROBE_CONF, path=MODPROBE_CONF_PATH))
    assert modprobe_info['options'].get('ipv6') == ['disable=1']
    assert modprobe_info['options'].get('mlx4_core')[0] == 'debug_level=1'
    assert modprobe_info['install'].get('ipv6') == ['/bin/true']


def test_modprobe_complete():
    minfo = ModProbe(context_wrap(MOD_COMPLETE, path=MOD_COMPLETE_PATH))
    assert sorted(minfo.data.keys()) == sorted([
     'alias', 'blacklist', 'install', 'options', 'remove'])
    assert sorted(minfo['alias']['bnx2']) == sorted(['eth*', 'en*'])
    assert 'i8xx_tco' in minfo['blacklist']
    assert minfo['blacklist']['i8xx_tco'] is True
    assert minfo['install']['eth1394'] == ['/bin/true']
    assert 'usbmouse' in minfo['install']
    assert 'usbmouse' in minfo['remove']
    assert minfo['options']['bonding'] == ['max_bonds=2']
    assert minfo['options']['bnx2'] == ['disable_msi=1']
    assert len(minfo.bad_lines) == 3
    assert minfo.bad_lines[0] == 'alias'
    assert minfo.bad_lines[1] == 'alias scsi_hostadapter2 ata_piix failed comment'
    assert minfo.bad_lines[2] == 'balclkist ieee80211'