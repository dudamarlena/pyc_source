# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_var_opt_mssql_log.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import ls_var_opt_mssql_log
from insights.parsers.ls_var_opt_mssql_log import LsVarOptMssqlLog
from insights.tests import context_wrap
MSSQL_LOG = '\ntotal 6322200\ndrwxr-xr-x.  3 mssql mssql        256 Jun  7 10:07 .\ndrwxr-xr-x. 71 root  root        4096 Jun 22 10:35 ..\ndrwxr-xr-x.  2 mssql mssql         65 Jul 10 09:33 journal\n-rw-------.  1 mssql mssql   67108864 Jul 10 09:32 local.0\n'

def test_ls_var_opt_mssql_log():
    log = LsVarOptMssqlLog(context_wrap(MSSQL_LOG, path='insights_commands/ls_-la_.var.opt.mssql.log'))
    assert log.dirs_of('/var/opt/mssql/log') == ['.', '..', 'journal']
    journal = log.dir_entry('/var/opt/mssql/log', 'journal')
    print journal
    assert journal == {'type': 'd', 
       'perms': 'rwxr-xr-x.', 'links': 2, 'owner': 'mssql', 'group': 'mssql', 
       'size': 65, 'date': 'Jul 10 09:33', 'raw_entry': 'drwxr-xr-x.  2 mssql mssql         65 Jul 10 09:33 journal', 
       'name': 'journal', 
       'dir': '/var/opt/mssql/log'}


def test_ls_var_opt_mssql_log_examples():
    env = {'ls_mssql_log': LsVarOptMssqlLog(context_wrap(MSSQL_LOG, path='insights_commands/ls_-la_.var.opt.mssql.log'))}
    failed, total = doctest.testmod(ls_var_opt_mssql_log, globs=env)
    assert failed == 0