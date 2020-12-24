# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_var_log.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.ls_var_log import LsVarLog
from insights.tests import context_wrap
from insights.util.file_permissions import FilePermissions
LS_1 = ('\n/var/log:\ntotal 1016\ndrwxr-xr-x.  7 root root   4096 Oct 19 15:38 .\ndrwxr-xr-x. 19 root root   4096 Oct 19 15:38 ..\ndrwxr-xr-x.  2 root root   4096 Jun 28 10:26 anaconda\ndrwxr-x---.  2 root root     22 Jun 28 10:26 audit\n-rw-r--r--.  1 root root   8433 Oct 19 15:38 boot.log\n-rw-------.  1 root utmp      0 Oct 19 05:39 btmp\n-rw-------.  1 root root  11370 Oct 19 22:01 cron\n-rw-r--r--.  1 root root  32226 Oct 19 15:38 dmesg\n-rw-r--r--.  1 root root  34423 Oct 19 15:27 dmesg.old\n-rw-------.  1 root root   5466 Oct 19 05:40 grubby\n-rw-r--r--.  1 root root 292292 Oct 19 22:42 lastlog\n-rw-------.  1 root root   1386 Oct 19 15:39 maillog\n-rw-------.  1 root root 609617 Oct 19 22:42 messages\ndrwx------.  2 root root      6 Jan 26  2014 ppp\ndrwxr-xr-x.  2 root root     41 Jun 28 10:28 rhsm\n-rw-------.  1 root root  18185 Oct 19 22:42 secure\n-rw-------.  1 root root      0 Jun 28 10:20 spooler\n-rw-------.  1 root root      0 Jun 28 10:19 tallylog\ndrwxr-xr-x.  2 root root     22 Sep  1 07:32 tuned\n-rw-r--r--.  1 root root   1854 Oct 19 22:38 up2date\n-rw-r--r--.  1 root root 211784 Jun 28 10:41 vboxadd-install.log\n-rw-r--r--.  1 root root     73 Oct 19 05:17 vboxadd-install-x11.log\n-rw-r--r--.  1 root root      1 Jun 28 10:40 VBoxGuestAdditions.log\n-rw-r--r--.  1 root root    280 Oct 19 15:38 wpa_supplicant.log\n-rw-rw-r--.  1 root utmp  21504 Oct 19 22:42 wtmp\n-rw-------.  1 root root   8423 Oct 19 15:29 yum.log\n\n/var/log/anaconda:\ntotal 1048\ndrwxr-xr-x. 2 root root   4096 Jun 28 10:26 .\ndrwxr-xr-x. 7 root root   4096 Oct 19 15:38 ..\n-rw-------. 1 root root  17862 Jun 28 10:26 anaconda.log\n-rw-------. 1 root root   1726 Jun 28 10:26 ifcfg.log\n-rw-------. 1 root root 680224 Jun 28 10:26 journal.log\n-rw-------. 1 root root      0 Jun 28 10:26 ks-script-2aaku7.log\n-rw-------. 1 root root 114262 Jun 28 10:26 packaging.log\n-rw-------. 1 root root  30137 Jun 28 10:26 program.log\n-rw-------. 1 root root  88243 Jun 28 10:26 storage.log\n-rw-------. 1 root root  63190 Jun 28 10:26 syslog\n-rw-------. 1 root root  52756 Jun 28 10:26 X.log\n\n/var/log/audit:\ntotal 1288\ndrwxr-x---. 2 root root      22 Jun 28 10:26 .\ndrwxr-xr-x. 7 root root    4096 Oct 19 15:38 ..\n-rw-------. 1 root root 1259137 Oct 19 22:42 audit.log\n\n/var/log/ppp:\ntotal 4\ndrwx------. 2 root root    6 Jan 26  2014 .\ndrwxr-xr-x. 7 root root 4096 Oct 19 15:38 ..\n\n/var/log/rhsm:\ntotal 32\ndrwxr-xr-x. 2 root root    41 Jun 28 10:28 .\ndrwxr-xr-x. 7 root root  4096 Oct 19 15:38 ..\n-rw-r--r--. 1 root root  4279 Oct 19 19:39 rhsmcertd.log\n-rw-r--r--. 1 root root 18331 Oct 19 19:39 rhsm.log\n\n/var/log/tuned:\ntotal 16\ndrwxr-xr-x. 2 root root   22 Sep  1 07:32 .\ndrwxr-xr-x. 7 root root 4096 Oct 19 15:38 ..\n-rw-r--r--. 1 root root 8834 Oct 19 15:39 tuned.log\n\n').strip()

def test_smoketest():
    context = context_wrap(LS_1)
    result = LsVarLog(context)
    assert '/var/log' in result
    assert '/var/log/audit' in result
    assert '/var/log/ppp' in result
    assert '/var/log/rhsm' in result
    assert '/var/log/tuned' in result
    assert 'audit.log' in result.listings['/var/log/audit']['entries']
    assert 'audit.log' == result.get_filepermissions('/var/log/audit', 'audit.log').path


def test_dir_parsed():
    context = context_wrap(LS_1)
    result = LsVarLog(context)
    ls = {}
    current_dir = ''
    test_lines = LS_1.splitlines()
    for line in test_lines:
        if line.endswith(':'):
            current_dir = line.split(':')[0]
            ls[current_dir] = []
        elif line.startswith('total'):
            pass
        elif line:
            fileperm = FilePermissions(line)
            ls[current_dir].append(fileperm.path)

    for dir in ls:
        assert dir in result
        dir_from_parser = result.listings[dir]['entries']
        for fil in ls[dir]:
            assert fil in dir_from_parser

        for fil in dir_from_parser:
            assert fil in ls[dir]


def test_get_filepermissions():
    context = context_wrap(LS_1)
    result = LsVarLog(context)
    ls = {}
    current_dir = ''
    test_lines = LS_1.splitlines()
    for line in test_lines:
        if line.endswith(':'):
            current_dir = line.split(':')[0]
            ls[current_dir] = []
        elif line.startswith('total'):
            pass
        elif line:
            fileperm = FilePermissions(line)
            ls[current_dir].append(fileperm)

    for dir in ls:
        assert dir in result
        for fil in ls[dir]:
            found = result.get_filepermissions(dir, fil.path)
            assert found is not None
            assert fil.line == found.line
            not_found = result.get_filepermissions(dir, 'nonexisting' + fil.path)
            assert not_found is None

    return