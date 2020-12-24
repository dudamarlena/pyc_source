# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pg_python2/_read.py
# Compiled at: 2018-09-10 07:56:21
# Size of source mod 2**32: 1923 bytes
import logging

def make_postgres_read_statement(table, kv_map, keys_to_get, limit, order_by, order_type, debug, clause, group_by, join_clause):
    _prefix = 'SELECT'
    _join_by = ' ' + join_clause + ' '
    _table_string = ' '.join(['FROM', table])
    _key_string = _join_by.join([k + clause + '%s' for k in kv_map.keys()])
    values = list(kv_map.values())
    if clause.strip().lower() == 'in':
        values = []
        _key_string = _join_by.join([k + clause + '(' + ','.join("'" + x + "'" for x in kv_map[k]) + ')' for k in kv_map.keys()])
    statement = ' '.join([_prefix, ', '.join(sorted(keys_to_get)), _table_string])
    if len(kv_map.keys()) > 0:
        statement = ' '.join([_prefix, ', '.join(sorted(keys_to_get)), _table_string, 'WHERE', _key_string])
    if group_by is not None:
        statement += ' GROUP BY ' + group_by
    if order_by is not None:
        statement += ' ORDER BY ' + order_by + ' ' + order_type
    if limit is not None:
        statement += ' LIMIT ' + str(limit)
    if debug:
        logging.info('Reading From Db: %s, %s' % (statement, kv_map.values()))
    return (
     statement, values)


def prepare_values(all_values, keys_to_get):
    ret_val = []
    if all_values is None:
        return
    else:
        k = sorted(keys_to_get)
        for row in all_values:
            row_kv = {}
            if len(row) == len(keys_to_get):
                for idx in range(0, len(row)):
                    try:
                        row_kv[k[idx]] = str(row[idx])
                    except UnicodeEncodeError:
                        row_kv[k[idx]] = str(row[idx].encode('utf-8'))
                    except Exception as e:
                        logging.error('Error occurred with exception: %s\n on value: %s' % (e, row[idx]))

            else:
                logging.error('Number of keys to be fetched are not correct')
                continue
            ret_val.append(row_kv)

        return ret_val