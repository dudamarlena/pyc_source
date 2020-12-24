# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_var_spool_clientmq.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import ls_var_spool_clientmq
from insights.parsers.ls_var_spool_clientmq import LsVarSpoolClientmq
from insights.tests import context_wrap
LS_VAR_SPOOL_CLIENTMQ = '\ntotal 40\n-rw-rw---- 1 51 51   4 Jul 11 02:32 dfw6B6Wilr002718\n-rw-rw---- 1 51 51   4 Jul 11 02:32 dfw6B6WixJ002715\n-rw-rw---- 1 51 51   4 Jul 11 02:32 dfw6B6WjP6002721\n-rw-rw---- 1 51 51 817 Jul 11 03:35 dfw6B7Z8BB002906\n-rw-rw---- 1 51 51 817 Jul 11 04:02 dfw6B822T0011150\n'

def test_ls_var_spool_clientmq():
    ls_var_spool_clientmq = LsVarSpoolClientmq(context_wrap(LS_VAR_SPOOL_CLIENTMQ, path='insights_commands/ls_-ln_.var.spool.clientmqueue'))
    assert ls_var_spool_clientmq.files_of('/var/spool/clientmqueue') == ['dfw6B6Wilr002718', 'dfw6B6WixJ002715', 'dfw6B6WjP6002721', 'dfw6B7Z8BB002906', 'dfw6B822T0011150']
    onemail = ls_var_spool_clientmq.dir_entry('/var/spool/clientmqueue', 'dfw6B6Wilr002718')
    assert onemail is not None
    assert onemail == {'group': '51', 'name': 'dfw6B6Wilr002718', 'links': 1, 'perms': 'rw-rw----', 'raw_entry': '-rw-rw---- 1 51 51   4 Jul 11 02:32 dfw6B6Wilr002718', 'owner': '51', 'date': 'Jul 11 02:32', 'type': '-', 'dir': '/var/spool/clientmqueue', 'size': 4}
    return


def test_ls_var_spool_clientmq_doc_examples():
    env = {'LsVarSpoolClientmq': LsVarSpoolClientmq, 
       'ls_var_spool_clientmq': LsVarSpoolClientmq(context_wrap(LS_VAR_SPOOL_CLIENTMQ, path='insights_commands/ls_-ln_.var.spool.clientmqueue'))}
    failed, total = doctest.testmod(ls_var_spool_clientmq, globs=env)
    assert failed == 0