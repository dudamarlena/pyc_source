# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_var_opt_mssql.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import ls_var_opt_mssql
from insights.tests import context_wrap
LS_VAR_OPT_MSSQL_WRONG_PERM = ('\ndrwxrwx---. 5 root root 58 Apr 16 07:20 /var/opt/mssql\n').strip()
LS_VAR_OPT_MSSQL_WRONG_PERM_2 = ('\ndrwxrwx---. 5 mssql root 58 Apr 16 07:20 /var/opt/mssql\n').strip()
LS_VAR_OPT_MSSQL = ('\ndrwxrwx---. 5 mssql mssql 58 Apr 16 07:20 /var/opt/mssql\n').strip()

def test_ls_var_opt_mssql():
    content = ls_var_opt_mssql.LsDVarOptMSSql(context_wrap(LS_VAR_OPT_MSSQL_WRONG_PERM, path='ls_-ld_.var.opt.mssql'))
    content_attr = content.listing_of('/var/opt/mssql').get('/var/opt/mssql')
    assert content_attr.get('owner') != 'mssql'
    assert content_attr.get('group') != 'mssql'
    content = ls_var_opt_mssql.LsDVarOptMSSql(context_wrap(LS_VAR_OPT_MSSQL_WRONG_PERM_2, path='ls_-ld_.var.opt.mssql'))
    content_attr = content.listing_of('/var/opt/mssql').get('/var/opt/mssql')
    assert content_attr.get('owner') == 'mssql'
    assert content_attr.get('group') != 'mssql'
    content = ls_var_opt_mssql.LsDVarOptMSSql(context_wrap(LS_VAR_OPT_MSSQL, path='ls_-ld_.var.opt.mssql'))
    content_attr = content.listing_of('/var/opt/mssql').get('/var/opt/mssql')
    assert content_attr.get('owner') == 'mssql'
    assert content_attr.get('group') == 'mssql'


def _failed_without_insights_command_as_path():
    foo = ls_var_opt_mssql.LsDVarOptMSSql(context_wrap(LS_VAR_OPT_MSSQL_WRONG_PERM_2))
    content_attr = foo.listing_of('/var/opt/mssql').get('/var/opt/mssql')
    assert content_attr.get('owner') != 'mssql'
    assert content_attr.get('group') != 'mssql'


def _failed_with_standard_path():
    bar = ls_var_opt_mssql.LsDVarOptMSSql(context_wrap(LS_VAR_OPT_MSSQL_WRONG_PERM_2, path='/var/opt/mssql'))
    content_attr = bar.listing_of('/var/opt/mssql').get('/var/opt/mssql')
    assert content_attr.get('owner') != 'mssql'
    assert content_attr.get('group') != 'mssql'


def test_ls_var_opt_mssql_docs():
    failed_count, tests = doctest.testmod(ls_var_opt_mssql, globs={'content': ls_var_opt_mssql.LsDVarOptMSSql(context_wrap(LS_VAR_OPT_MSSQL_WRONG_PERM, path='ls_-ld_.var.opt.mssql'))})
    assert failed_count == 0