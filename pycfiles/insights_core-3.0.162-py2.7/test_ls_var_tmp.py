# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_var_tmp.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import ls_var_tmp
from insights.parsers.ls_var_tmp import LsVarTmp
from insights.tests import context_wrap
LS_VAR_TMP = '\n/var/tmp:\ntotal 20\ndrwxr-xr-x.  2 0 0 4096 Mar 26 02:25 a1\ndrwxr-xr-x.  2 0 0 4096 Mar 26 02:25 a2\ndrwxr-xr-x.  3 0 0 4096 Apr  3 02:50 foreman-ssh-cmd-fc3f65c9-2b35-480d-87e3-1d971433d6ad\n'

def test_ls_var_tmp():
    ls_var_tmp = LsVarTmp(context_wrap(LS_VAR_TMP))
    assert ls_var_tmp.dirs_of('/var/tmp') == ['a1', 'a2', 'foreman-ssh-cmd-fc3f65c9-2b35-480d-87e3-1d971433d6ad']
    foreman = ls_var_tmp.dir_entry('/var/tmp', 'foreman-ssh-cmd-fc3f65c9-2b35-480d-87e3-1d971433d6ad')
    assert foreman is not None
    assert foreman == {'group': '0', 
       'name': 'foreman-ssh-cmd-fc3f65c9-2b35-480d-87e3-1d971433d6ad', 
       'links': 3, 
       'perms': 'rwxr-xr-x.', 
       'raw_entry': 'drwxr-xr-x.  3 0 0 4096 Apr  3 02:50 foreman-ssh-cmd-fc3f65c9-2b35-480d-87e3-1d971433d6ad', 
       'owner': '0', 
       'date': 'Apr  3 02:50', 
       'type': 'd', 
       'size': 4096, 
       'dir': '/var/tmp'}
    return


def test_ls_var_tmp_doc_examples():
    env = {'LsVarTmp': LsVarTmp, 
       'ls_var_tmp': LsVarTmp(context_wrap(LS_VAR_TMP))}
    failed, total = doctest.testmod(ls_var_tmp, globs=env)
    assert failed == 0