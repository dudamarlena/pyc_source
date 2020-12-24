# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/turicas/software/pyenv/versions/rows/lib/python3.6/site-packages/rows/operations.py
# Compiled at: 2019-02-13 03:47:25
# Size of source mod 2**32: 2795 bytes
from __future__ import unicode_literals
from collections import OrderedDict
from rows.plugins.utils import create_table
from rows.table import Table

def join(keys, tables):
    """Merge a list of `Table` objects using `keys` to group rows"""
    fields = OrderedDict()
    for table in tables:
        fields.update(table.fields)

    fields_keys = set(fields.keys())
    for key in keys:
        if key not in fields_keys:
            raise ValueError('Invalid key: "{}"'.format(key))

    none_fields = lambda : OrderedDict({field:None for field in fields.keys()})
    data = OrderedDict()
    for table in tables:
        for row in table:
            row_key = tuple([getattr(row, key) for key in keys])
            if row_key not in data:
                data[row_key] = none_fields()
            data[row_key].update(row._asdict())

    merged = Table(fields=fields)
    merged.extend(data.values())
    return merged


def transform(fields, function, *tables):
    """Return a new table based on other tables and a transformation function"""
    new_table = Table(fields=fields)
    for table in tables:
        for row in filter(bool, map(lambda row: function(row, table), table)):
            new_table.append(row)

    return new_table


def transpose(table, fields_column, *args, **kwargs):
    field_names = []
    new_rows = [{} for _ in range(len(table.fields) - 1)]
    for row in table:
        row = row._asdict()
        field_name = row[fields_column]
        field_names.append(field_name)
        del row[fields_column]
        for index, value in enumerate(row.values()):
            new_rows[index][field_name] = value

    table_rows = [[row[field_name] for field_name in field_names] for row in new_rows]
    return create_table([field_names] + table_rows, *args, **kwargs)