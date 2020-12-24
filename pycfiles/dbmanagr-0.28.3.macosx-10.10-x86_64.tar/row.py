# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/model/row.py
# Compiled at: 2015-10-11 07:17:06
import logging
from dbmanagr.model.baseitem import BaseItem
from dbmanagr.formatter import Formatter
from dbmanagr.utils import primary_key_or_first_column
logger = logging.getLogger(__name__)

def val(row, column):
    return row[column]


class Row(BaseItem):
    """A table row from the database"""

    def __init__(self, table, row):
        self.table = table
        self.row = row

    def __getitem__(self, i):
        if i is None:
            return
        else:
            if type(i) == unicode:
                i = i.encode('ascii')
            if type(i) is str:
                try:
                    return self.row.__dict__[i]
                except BaseException:
                    return

            return self.row[i]

    def __repr__(self):
        return str(self.row)

    def title(self):
        if 'title' in self.row.__dict__:
            return val(self, 'title')
        return val(self, primary_key_or_first_column(self.table))

    def subtitle(self):
        return val(self, 'subtitle')

    def autocomplete(self):
        column = primary_key_or_first_column(self.table)
        return self.table.autocomplete_(column, self[column])

    def icon(self):
        return 'images/row.png'

    def format(self):
        return Formatter.format_row(self)