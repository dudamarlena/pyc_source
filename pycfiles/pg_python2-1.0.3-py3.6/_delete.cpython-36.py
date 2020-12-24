# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pg_python2/_delete.py
# Compiled at: 2018-08-03 06:01:13
# Size of source mod 2**32: 362 bytes
import logging

def make_postgres_delete_statement(table, kv_map, debug):
    _prefix = 'DELETE FROM '
    keys = ' and '.join([k + '=%s' for k in kv_map.keys()])
    statement = ' '.join([_prefix, table, ' where ', keys])
    if debug:
        logging.info('Deleting from Db: %s, %s' % (statement, kv_map.values()))
    return (
     statement, list(kv_map.values()))