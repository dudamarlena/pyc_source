# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_osroot.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import ls_osroot
from insights.parsers.ls_osroot import LsOsroot
from insights.tests import context_wrap
LS_LAN_OSROOT = ('\ntotal 5256\ndr-xr-xr-x.  17 0 0     271 Apr  5 18:08 .\ndr-xr-xr-x.  17 0 0     271 Apr  5 18:08 ..\n-rw-r--r--.   1 0 0       0 Feb 25  2017 1\nlrwxrwxrwx.   1 0 0       7 Feb 25  2017 bin -> usr/bin\ndr-xr-xr-x.   3 0 0    4096 Feb 25  2017 boot\n-rw-r--r--.   1 0 0 5168141 Oct 16  2017 channel-list\ndrwxr-xr-x.  21 0 0    3440 Apr 12 14:46 dev\ndrwxr-xr-x. 148 0 0    8192 Apr 18 09:17 etc\ndrwxr-xr-x.   5 0 0      37 Jul 31  2017 home\nlrwxrwxrwx.   1 0 0       7 Feb 25  2017 lib -> usr/lib\nlrwxrwxrwx.   1 0 0       9 Feb 25  2017 lib64 -> usr/lib64\ndrwxr-xr-x.   2 0 0       6 Mar 10  2016 media\ndrwxr-xr-x.   2 0 0       6 Mar 10  2016 mnt\ndrwxr-xr-x.   5 0 0      48 Mar 27 13:37 opt\ndr-xr-xr-x. 265 0 0       0 Apr  6 02:07 proc\n-rw-r--r--.   1 0 0  175603 Apr  5 18:08 .readahead\ndr-xr-x---.  26 0 0    4096 Apr 18 09:17 root\ndrwxr-xr-x.  43 0 0    1340 Apr 18 09:17 run\nlrwxrwxrwx.   1 0 0       8 Feb 25  2017 sbin -> usr/sbin\ndrwxr-xr-x.   2 0 0       6 Mar 10  2016 srv\ndr-xr-xr-x.  13 0 0       0 Apr  5 18:07 sys\ndrwxrwxrwt.  40 0 0    8192 Apr 18 11:17 tmp\ndrwxr-xr-x.  13 0 0     155 Feb 25  2017 usr\ndrwxr-xr-x.  21 0 0    4096 Apr  6 02:07 var\n').strip()

def test_ls_osroot():
    ls_osroot = LsOsroot(context_wrap(LS_LAN_OSROOT, path='ls_-lan'))
    assert '/' in ls_osroot
    assert len(ls_osroot.files_of('/')) == 7
    assert ls_osroot.files_of('/') == ['1', 'bin', 'channel-list', 'lib', 'lib64', '.readahead', 'sbin']
    assert ls_osroot.dirs_of('/') == ['.', '..', 'boot', 'dev', 'etc', 'home', 'media', 'mnt', 'opt', 'proc', 'root', 'run', 'srv', 'sys', 'tmp', 'usr', 'var']
    assert ls_osroot.listing_of('/')['tmp'] == {'group': '0', 'name': 'tmp', 'links': 40, 'perms': 'rwxrwxrwt.', 'raw_entry': 'drwxrwxrwt.  40 0 0    8192 Apr 18 11:17 tmp', 'owner': '0', 'date': 'Apr 18 11:17', 'type': 'd', 'dir': '/', 'size': 8192}


def test_ls_osroot_doc_examples():
    env = {'LsOsroot': LsOsroot, 
       'ls_osroot': LsOsroot(context_wrap(LS_LAN_OSROOT, path='ls_-lan'))}
    failed, total = doctest.testmod(ls_osroot, globs=env)
    assert failed == 0