# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bzETL\util\sql.py
# Compiled at: 2013-12-18 14:05:11
from dzAlerts.util import struct

def find_holes(db, table_name, column_name, filter, _range):
    """
    FIND HOLES IN A DENSE COLUMN OF INTEGERS
    RETURNS A LIST OF {"min"min, "max":max} OBJECTS
    """
    _range = struct.wrap(_range)
    params = {'min': _range.min, 
       'max': _range.max - 1, 
       'column_name': db.quote_column(column_name), 
       'table_name': db.quote_column(table_name), 
       'filter': db.esfilter2sqlwhere(filter)}
    min_max = db.query('\n        SELECT\n            min({{column_name}}) `min`,\n            max({{column_name}})+1 `max`\n        FROM\n            {{table_name}} a\n        WHERE\n            a.{{column_name}} BETWEEN {{min}} AND {{max}} AND\n            {{filter}}\n    ', params)[0]
    db.execute('SET @last={{min}}-1', {'min': _range.min})
    ranges = db.query('\n        SELECT\n            prev_rev+1 `min`,\n            curr_rev `max`\n        FROM (\n            SELECT\n                a.{{column_name}}-@last diff,\n                @last prev_rev,\n                @last:=a.{{column_name}} curr_rev\n            FROM\n                {{table_name}} a\n            WHERE\n                a.{{column_name}} BETWEEN {{min}} AND {{max}} AND\n                {{filter}}\n            ORDER BY\n                a.{{column_name}}\n        ) a\n        WHERE\n            diff>1\n    ', params)
    if ranges:
        ranges.append({'min': min_max.max, 'max': _range.max})
    elif min_max.min:
        ranges.append({'min': _range.min, 'max': min_max.min})
        ranges.append({'min': min_max.max, 'max': _range.max})
    else:
        ranges.append(_range)
    return ranges