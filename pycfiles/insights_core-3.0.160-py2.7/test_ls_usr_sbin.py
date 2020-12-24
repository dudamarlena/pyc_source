# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_usr_sbin.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.core.filters import add_filter
from insights.parsers import ls_usr_sbin
from insights.parsers.ls_usr_sbin import LsUsrSbin
from insights.specs import Specs
from insights.tests import context_wrap
LS_USR_SBIN = '\ntotal 41472\n-rwxr-xr-x. 1 0  0   11720 Mar 18  2014 accessdb\n-rwxr-xr-x. 1 0  0    3126 Oct  4  2013 addgnupghome\n-rwxr-xr-x. 1 0  0   20112 Jun  1  2017 addpart\n-rwxr-xr-x. 1 0  0  371912 Jan 27  2014 postconf\n-rwxr-sr-x. 1 0 90  218552 Jan 27  2014 postdrop\n'

def test_ls_usr_sbin():
    ls_usr_sbin = LsUsrSbin(context_wrap(LS_USR_SBIN, path='insights_commands/ls_-ln_.usr.sbin'))
    assert ls_usr_sbin.files_of('/usr/sbin') == ['accessdb', 'addgnupghome', 'addpart', 'postconf', 'postdrop']
    postdrop = ls_usr_sbin.dir_entry('/usr/sbin', 'postdrop')
    assert postdrop is not None
    assert postdrop == {'group': '90', 
       'name': 'postdrop', 
       'links': 1, 
       'perms': 'rwxr-sr-x.', 
       'raw_entry': '-rwxr-sr-x. 1 0 90  218552 Jan 27  2014 postdrop', 
       'owner': '0', 
       'date': 'Jan 27  2014', 
       'type': '-', 
       'size': 218552, 
       'dir': '/usr/sbin'}
    return


def test_ls_usr_sbin_doc_examples():
    env = {'Specs': Specs, 
       'add_filter': add_filter, 
       'LsUsrSbin': LsUsrSbin, 
       'ls_usr_sbin': LsUsrSbin(context_wrap(LS_USR_SBIN, path='insights_commands/ls_-ln_.usr.sbin'))}
    failed, total = doctest.testmod(ls_usr_sbin, globs=env)
    assert failed == 0