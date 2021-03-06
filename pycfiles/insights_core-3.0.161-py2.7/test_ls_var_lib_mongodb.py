# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_var_lib_mongodb.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import ls_var_lib_mongodb
from insights.parsers.ls_var_lib_mongodb import LsVarLibMongodb
from insights.tests import context_wrap
LS_VAR_LIB_MONGODB = '\ntotal 6322200\ndrwxr-xr-x.  3 mongodb mongodb        256 Jun  7 10:07 .\ndrwxr-xr-x. 71 root    root          4096 Jun 22 10:35 ..\ndrwxr-xr-x.  2 mongodb mongodb         65 Jul 10 09:33 journal\n-rw-------.  1 mongodb mongodb   67108864 Jul 10 09:32 local.0\n-rw-------.  1 mongodb mongodb   16777216 Jul 10 09:32 local.ns\n'

def test_ls_var_lib_mongodb():
    ls_var_lib_mongodb = LsVarLibMongodb(context_wrap(LS_VAR_LIB_MONGODB, path='insights_commands/ls_-la_.var.lib.mongodb'))
    assert ls_var_lib_mongodb.dirs_of('/var/lib/mongodb') == ['.', '..', 'journal']
    journal = ls_var_lib_mongodb.dir_entry('/var/lib/mongodb', 'journal')
    assert journal is not None
    assert journal == {'group': 'mongodb', 'name': 'journal', 'links': 2, 'perms': 'rwxr-xr-x.', 'raw_entry': 'drwxr-xr-x.  2 mongodb mongodb         65 Jul 10 09:33 journal', 'owner': 'mongodb', 'date': 'Jul 10 09:33', 'type': 'd', 'dir': '/var/lib/mongodb', 'size': 65}
    return


def test_ls_var_lib_mongodb_doc_examples():
    env = {'LsVarLibMongodb': LsVarLibMongodb, 
       'ls_var_lib_mongodb': LsVarLibMongodb(context_wrap(LS_VAR_LIB_MONGODB, path='insights_commands/ls_-la_.var.lib.mongodb'))}
    failed, total = doctest.testmod(ls_var_lib_mongodb, globs=env)
    assert failed == 0