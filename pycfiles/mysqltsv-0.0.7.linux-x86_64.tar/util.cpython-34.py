# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/halfak/env/3.4/lib/python3.4/site-packages/mysqltsv/util.py
# Compiled at: 2015-12-19 13:21:12
# Size of source mod 2**32: 1449 bytes
import logging
logger = logging.getLogger(__name__)

def encode(val, none_string='NULL'):
    if val == None:
        return none_string
    if isinstance(val, bytes):
        val = str(val, 'utf-8', 'replace')
    else:
        val = str(val)
    return val.replace('\t', '\\t').replace('\n', '\\n')


def decode(val, type=str, none_string='NULL'):
    if val == none_string:
        return
    if isinstance(val, bytes):
        val = str(val, 'utf-8', 'replace')
    return type(val.replace('\\t', '\t').replace('\\n', '\n'))


def read_row(line, *args, types=None, **kwargs):
    raw_values = line.strip('\r\n').split('\t')
    if types is None:
        return (decode(rv, *args, **kwargs) for rv in raw_values)
    else:
        return (decode(rv, type=t, *args, **kwargs) for rv, t in zip(raw_values, types))


def write_row(row, f, *args, headers=None, **kwargs):
    if isinstance(row, dict):
        if headers is None:
            raise ValueError('Cannot write `dict` without specifying headers.')
        values = [row[h] for h in headers]
    else:
        if hasattr(row, 'values'):
            values = list(row.values())
        else:
            if hasattr(row, '__iter__'):
                values = list(row)
            else:
                raise ValueError('row is non-iterable type {0}'.format(type(row)))
    f.write('\t'.join(encode(v, *args, **kwargs) for v in values))
    f.write('\n')