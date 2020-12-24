# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/uszipcode-project/uszipcode/pkg/sqlalchemy_mate/crud/updating.py
# Compiled at: 2018-09-29 23:45:55
# Size of source mod 2**32: 2404 bytes
"""
This module provide utility functions for update operation.
"""
from collections import OrderedDict
from sqlalchemy import and_
from ..utils import ensure_list

def update_all(engine, table, data, upsert=False):
    """
    Update data by its primary_key column.
    """
    data = ensure_list(data)
    ins = table.insert()
    upd = table.update()
    pk_cols = OrderedDict()
    for column in table._columns:
        if column.primary_key:
            pk_cols[column.name] = column

    data_to_insert = list()
    if len(pk_cols) >= 2:
        for row in data:
            result = engine.execute((upd.where(and_(*[col == row[name] for name, col in pk_cols.items()])).values)(**row))
            if result.rowcount == 0:
                data_to_insert.append(row)

    else:
        if len(pk_cols) == 1:
            for row in data:
                result = engine.execute((upd.where([col == row[name] for name, col in pk_cols.items()][0]).values)(**row))
                if result.rowcount == 0:
                    data_to_insert.append(row)

        else:
            data_to_insert = data
    if upsert:
        if len(data_to_insert):
            engine.execute(ins, data_to_insert)


def upsert_all(engine, table, data):
    """
    Update data by primary key columns. If not able to update, do insert.

    Example::

        # suppose in database we already have {"id": 1, "name": "Alice"}
        >>> data = [
        ...     {"id": 1, "name": "Bob"}, # this will be updated
        ...     {"id": 2, "name": "Cathy"}, # this will be added
        ... ]
        >>> upsert_all(engine, table_user, data)
        >>> engine.execute(select([table_user])).fetchall()
        [{"id": 1, "name": "Bob"}, {"id": 2, "name": "Cathy"}]

    **中文文档**

    批量更新文档. 如果该表格定义了Primary Key, 则用Primary Key约束where语句. 对于
    where语句无法找到的行, 自动进行批量bulk insert.
    """
    update_all(engine, table, data, upsert=True)