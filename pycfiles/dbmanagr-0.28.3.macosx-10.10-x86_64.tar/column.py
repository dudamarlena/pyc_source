# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/model/column.py
# Compiled at: 2015-10-11 07:17:06
from dbmanagr.model.baseitem import BaseItem
from dbmanagr.formatter import Formatter
from dbmanagr.utils import dictminus

class Column(BaseItem):
    """A table column"""

    def __init__(self, table, name, **kwargs):
        self.table = table
        self.name = name
        self.type = None
        self.nullable = None
        self.default = None
        self.__dict__.update(kwargs)
        self.tablename = table.name
        self.uri = self.autocomplete()
        return

    def __repr__(self):
        return '%s.%s' % (self.table.name, self.name)

    def __str__(self):
        return self.__repr__()

    def ddl(self):
        return ('{0} {1}{2}{3}').format(self.name, self.type.compile(), {False: ' not null'}.get(self.nullable, ''), {None: ''}.get(self.default, (' default {0}').format(self.default)))

    def title(self):
        return self.name

    def subtitle(self):
        return self.table.title()

    def autocomplete(self):
        return '%s%s?%s' % (self.table.uri, self.table.name, self.name)

    def icon(self):
        return 'images/table.png'

    def format(self):
        return Formatter.format_column(self)

    def as_json(self):
        d = {'__cls__': str(self.__class__), 
           'name': self.name, 
           'table': self.table.name, 
           'type': self.type.compile(), 
           'uri': self.uri}
        if self.default is not None:
            d['default'] = self.default
        return d


def create_column(table, name, column=None):
    if column is None:
        return Column(table, name)
    else:
        return Column(table, name, **dictminus(column.__dict__, 'name', 'table'))