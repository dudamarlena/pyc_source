# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\index\mainframe\view_db.py
# Compiled at: 2013-09-15 14:20:24
from __future__ import division, absolute_import, print_function, unicode_literals
import sys, os, logging
from sqlalchemy import MetaData, distinct
from ..lib.items import DirItem, FileItem, DisabledItem

def view_db(tree_widget):
    if DBSession.bind:
        metadata = MetaData(DBSession.bind)
        metadata.reflect()
        for table in metadata.tables:
            tdata = metadata.tables.get(table)
            table_item = DirItem(tree_widget, table, summary=tdata)
            for column in tdata.c:
                if column.primary_key:
                    column_item = DisabledItem(table_item, column.name)
                    column_item.setBrief(b'Главный ключ, просмотр отключен!')
                elif column.foreign_keys:
                    column_item = DisabledItem(table_item, column.name)
                    column_item.setBrief(b'Ссылка на другую таблицу, просмотр отключен!')
                else:
                    column_item = FileItem(table_item, column.name)
                    column_item.setBrief(get_distinct(column))

            table_item.setExpanded(True)


def get_distinct(column):
    query = DBSession.query(distinct(column))
    rows = query.all()
    rows_count = query.count()
    td_list = [ unicode(row[0]) for row in rows ]
    return (b'\n').join(td_list)