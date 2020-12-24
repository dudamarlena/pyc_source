# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/pg_python/_delete.py
# Compiled at: 2019-10-12 05:47:14
import logging

def make_postgres_delete_statement(table, kv_map, debug):
    _prefix = 'DELETE FROM '
    keys = (' and ').join([ k + '=%s' for k in list(kv_map.keys()) ])
    statement = (' ').join([_prefix, table, ' where ', keys])
    if debug:
        logging.warning('Deleting from Db: %s, %s' % (statement, list(kv_map.values())))
    return (
     statement, list(kv_map.values()))