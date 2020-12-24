# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_etc.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import ls_etc
from insights.tests import context_wrap
LS_ETC = '\n/etc/sysconfig:\ntotal 96\ndrwxr-xr-x.  7 0 0 4096 Jul  6 23:41 .\ndrwxr-xr-x. 77 0 0 8192 Jul 13 03:55 ..\ndrwxr-xr-x.  2 0 0   41 Jul  6 23:32 cbq\ndrwxr-xr-x.  2 0 0    6 Sep 16  2015 console\n-rw-------.  1 0 0 1390 Mar  4  2014 ebtables-config\n-rw-r--r--.  1 0 0   72 Sep 15  2015 firewalld\nlrwxrwxrwx.  1 0 0   17 Jul  6 23:32 grub -> /etc/default/grub\n\n/etc/rc.d/rc3.d:\ntotal 4\ndrwxr-xr-x.  2 0 0   58 Jul  6 23:32 .\ndrwxr-xr-x. 10 0 0 4096 Sep 16  2015 ..\nlrwxrwxrwx.  1 0 0   20 Jul  6 23:32 K50netconsole -> ../init.d/netconsole\nlrwxrwxrwx.  1 0 0   17 Jul  6 23:32 S10network -> ../init.d/network\nlrwxrwxrwx.  1 0 0   15 Jul  6 23:32 S97rhnsd -> ../init.d/rhnsd\n'

def test_ls_etc():
    list_etc = ls_etc.LsEtc(context_wrap(LS_ETC))
    assert '/etc/sysconfig' in list_etc
    assert len(list_etc.files_of('/etc/sysconfig')) == 3
    assert list_etc.files_of('/etc/sysconfig') == ['ebtables-config', 'firewalld', 'grub']
    assert list_etc.dirs_of('/etc/sysconfig') == ['.', '..', 'cbq', 'console']
    assert list_etc.specials_of('/etc/sysconfig') == []
    assert list_etc.total_of('/etc/sysconfig') == 96
    grub = list_etc.dir_entry('/etc/sysconfig', 'grub')
    assert grub is not None
    assert grub == {'group': '0', 
       'name': 'grub', 
       'links': 1, 
       'perms': 'rwxrwxrwx.', 
       'raw_entry': 'lrwxrwxrwx.  1 0 0   17 Jul  6 23:32 grub -> /etc/default/grub', 
       'owner': '0', 
       'link': '/etc/default/grub', 
       'date': 'Jul  6 23:32', 
       'type': 'l', 
       'size': 17, 
       'dir': '/etc/sysconfig'}
    assert list_etc.files_of('/etc/rc.d/rc3.d') == ['K50netconsole',
     'S10network', 'S97rhnsd']
    return


def test_ls_etc_documentation():
    failed_count, tests = doctest.testmod(ls_etc, globs={'ls_etc': ls_etc.LsEtc(context_wrap(LS_ETC))})
    assert failed_count == 0