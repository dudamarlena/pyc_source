# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysctl.py
# Compiled at: 2019-11-14 13:57:46
import doctest
from insights.parsers import sysctl
from insights.tests import context_wrap
from insights.util import keys_in
SYSCTL_TEST = ('\na=1\nb = 2\nc = include an = sign\n').strip()
SYSCTL_DOC_TEST = ('\nkernel.domainname = example.com\nkernel.modprobe = /sbin/modprobe\n').strip()
SYSCTL_CONF_TEST = ('\n# sysctl.conf sample\n#\n  kernel.domainname = example.com\n# kernel.domainname.invalid = notvalid.com\n\n; this one has a space which will be written to the sysctl!\n  kernel.modprobe = /sbin/mod probe\n').strip()
SYSCTL_CONF_INITRAMFS_TEST = ('\ninitramfs:/etc/sysctl.conf\n========================================================================\n# sysctl settings are defined through files in\n# /usr/lib/sysctl.d/, /run/sysctl.d/, and /etc/sysctl.d/.\n#\n# Vendors settings live in /usr/lib/sysctl.d/.\n# To override a whole file, create a new file with the same in\n# /etc/sysctl.d/ and put new settings there. To override\n# only specific settings, add a file with a lexically later\n# name in /etc/sysctl.d/ and put new settings there.\n#\n# For more information, see sysctl.conf(5) and sysctl.d(5).\nfs.inotify.max_user_watches=524288\nkey2=value2\nkey2_alt=value2_alt\n#  key3=value3\n; key4=value4\n========================================================================\n\ninitramfs:/etc/sysctl.d/*.conf\n========================================================================\n========================================================================\n').strip()

def test_sysctl():
    r = sysctl.Sysctl(context_wrap(SYSCTL_TEST))
    assert keys_in(['a', 'b', 'c'], r.data)
    assert r.data['a'] == '1'
    assert r.data['b'] == '2'
    assert r.data['c'] == 'include an = sign'


def test_sysctl_conf():
    r = sysctl.SysctlConf(context_wrap(SYSCTL_CONF_TEST))
    assert keys_in(['kernel.domainname', 'kernel.modprobe'], r.data)
    assert r.data['kernel.domainname'] == 'example.com'
    assert r.data['kernel.modprobe'] == '/sbin/mod probe'
    assert 'kernel.domainname.invalid' not in r.data


def test_sysctl_conf_initramfs():
    r = sysctl.SysctlConfInitramfs(context_wrap(SYSCTL_CONF_INITRAMFS_TEST))
    assert r is not None
    assert r.get('max_user_watches') == [{'raw_message': 'fs.inotify.max_user_watches=524288'}]
    assert r.get('key2') == [{'raw_message': 'key2=value2'}, {'raw_message': 'key2_alt=value2_alt'}]
    assert r.get('key3') == []
    assert r.get('key4') == []
    return


def test_docs():
    env = {'sysctl': sysctl.Sysctl(context_wrap(SYSCTL_DOC_TEST)), 
       'sysctl_conf': sysctl.SysctlConf(context_wrap(SYSCTL_CONF_TEST)), 
       'sysctl_initramfs': sysctl.SysctlConfInitramfs(context_wrap(SYSCTL_CONF_INITRAMFS_TEST))}
    failed, total = doctest.testmod(sysctl, globs=env)
    assert failed == 0