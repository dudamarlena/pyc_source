# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\table_class\unittest\unittest_table.py
# Compiled at: 2019-08-20 12:27:39
# Size of source mod 2**32: 458 bytes
from sqlalchemy import Column, String, Integer
from sql_factory.base_table import BaseTable

class UnittestTable(BaseTable):
    table_columns = [
     Column('id', Integer, primary_key=True, autoincrement=True),
     Column('name', String(50)),
     Column('obj', String)]

    def insert_by_id(self, id: int, content: dict):
        if 'id' not in content.keys():
            content['id'] = id
        self.insert(content)