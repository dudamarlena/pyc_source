# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_var_run.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import ls_var_run
from insights.parsers.ls_var_run import LsVarRun
from insights.tests import context_wrap
LS_VAR_RUN = '\ntotal 20\ndrwx--x---.  2   0 984   40 May 15 09:29 openvpn\ndrwxr-xr-x.  2   0   0   40 May 15 09:30 plymouth\ndrwxr-xr-x.  2   0   0   40 May 15 09:29 ppp\ndrwxr-xr-x.  2  75  75   40 May 15 09:29 radvd\n-rw-r--r--.  1   0   0    5 May 15 09:30 rhnsd.pid\ndrwxr-xr-x.  2   0   0   60 May 30 09:31 rhsm\ndrwx------.  2  32  32   40 May 15 09:29 rpcbind\n-r--r--r--.  1   0   0    0 May 17 16:26 rpcbind.lock\n'

def test_ls_var_run():
    ls_var_run = LsVarRun(context_wrap(LS_VAR_RUN, path='insights_commands/ls_-lnL_.var.run'))
    assert ls_var_run.dirs_of('/var/run') == ['openvpn', 'plymouth', 'ppp', 'radvd', 'rhsm', 'rpcbind']
    foreman = ls_var_run.dir_entry('/var/run', 'openvpn')
    assert foreman is not None
    assert foreman == {'group': '984', 
       'name': 'openvpn', 
       'links': 2, 
       'perms': 'rwx--x---.', 
       'raw_entry': 'drwx--x---.  2   0 984   40 May 15 09:29 openvpn', 
       'owner': '0', 
       'date': 'May 15 09:29', 
       'type': 'd', 
       'size': 40, 
       'dir': '/var/run'}
    return


def test_ls_var_run_doc_examples():
    env = {'LsVarRun': LsVarRun, 
       'ls_var_run': LsVarRun(context_wrap(LS_VAR_RUN, path='insights_commands/ls_-lnL_.var.run'))}
    failed, total = doctest.testmod(ls_var_run, globs=env)
    assert failed == 0