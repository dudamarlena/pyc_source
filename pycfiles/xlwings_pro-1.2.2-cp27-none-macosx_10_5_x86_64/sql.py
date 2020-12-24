# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: <xlwings_pro-1.2.2>/xlwings/ext/sql.py
# Compiled at: 2020-03-09 05:37:56
from .. import func, arg, ret
import sqlite3

def conv_value(value, col_is_str):
    if value is None:
        return 'NULL'
    else:
        if col_is_str:
            return repr(str(value))
        else:
            if isinstance(value, bool):
                if value:
                    return 1
                return 0
            return repr(value)

        return


@func
@arg('tables', expand='table', ndim=2)
@ret(expand='table')
def sql(query, *tables):
    return _sql(query, *tables)


@func
@arg('tables', expand='table', ndim=2)
def sql_dynamic(query, *tables):
    """Called if native dynamic arrays are available"""
    return _sql(query, *tables)


def _sql(query, *tables):
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    for i, table in enumerate(tables):
        cols = table[0]
        rows = table[1:]
        types = [ any(type(row[j]) is str for row in rows) for j in range(len(cols))
                ]
        name = chr(65 + i)
        stmt = 'CREATE TABLE %s (%s)' % (
         name,
         (', ').join("'%s' %s" % (col, 'STRING' if typ else 'REAL') for col, typ in zip(cols, types)))
        c.execute(stmt)
        if rows:
            stmt = 'INSERT INTO %s VALUES %s' % (
             name,
             (', ').join('(%s)' % (', ').join(conv_value(value, type) for value, typ in zip(row, types)) for row in rows))
            stmt = stmt.replace("\\'", "''")
            c.execute(stmt)

    res = []
    c.execute(query)
    res.append([ x[0] for x in c.description ])
    for row in c:
        res.append(list(row))

    return res