# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_usr_lib64.py
# Compiled at: 2019-11-14 13:57:46
import doctest
from insights.parsers import ls_usr_lib64
from insights.parsers.ls_usr_lib64 import LsUsrLib64
from insights.tests import context_wrap
LS_USR_LIB64 = '\ntotal 447460\ndr-xr-xr-x. 150 0 0    77824 Jul 30 16:39 .\ndrwxr-xr-x.  13 0 0     4096 Apr 30  2017 ..\ndrwxr-xr-x.   3 0 0       20 Nov  3  2016 krb5\n-rwxr-xr-x.   1 0 0   155464 Oct 28  2016 ld-2.17.so\ndrwxr-xr-x.   3 0 0       20 Jun 10  2016 ldb\nlrwxrwxrwx.   1 0 0       10 Apr 30  2017 ld-linux-x86-64.so.2 -> ld-2.17.so\nlrwxrwxrwx.   1 0 0       21 Apr 30  2017 libabrt_dbus.so.0 -> libabrt_dbus.so.0.0.1\n'

def test_ls_usr_lib64():
    ls_usr_lib64 = LsUsrLib64(context_wrap(LS_USR_LIB64, path='insights_commands/ls_-lan_.usr.lib64'))
    assert len(ls_usr_lib64.dirs_of('/usr/lib64')) == 4
    ret = ls_usr_lib64.dir_entry('/usr/lib64', 'libabrt_dbus.so.0')
    assert ret == {'type': 'l', 
       'perms': 'rwxrwxrwx.', 
       'links': 1, 
       'owner': '0', 
       'group': '0', 
       'size': 21, 
       'date': 'Apr 30  2017', 
       'name': 'libabrt_dbus.so.0', 
       'link': 'libabrt_dbus.so.0.0.1', 
       'raw_entry': 'lrwxrwxrwx.   1 0 0       21 Apr 30  2017 libabrt_dbus.so.0 -> libabrt_dbus.so.0.0.1', 
       'dir': '/usr/lib64'}


def test_ls_usr_lib64_doc_examples():
    env = {'ls_usr_lib64': LsUsrLib64(context_wrap(LS_USR_LIB64, path='insights_commands/ls_-lan_.usr.lib64'))}
    failed, total = doctest.testmod(ls_usr_lib64, globs=env)
    assert failed == 0