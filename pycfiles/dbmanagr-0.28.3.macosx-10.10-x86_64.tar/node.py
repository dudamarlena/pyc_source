# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/dto/node.py
# Compiled at: 2015-10-11 07:17:06
from dbmanagr.dto import Dto
from dbmanagr.jsonable import from_json
from dbmanagr.formatter import Formatter
PRIMARY_KEY_OPTIONS = {True: '*', 
   False: ''}
NULLABLE_OPTIONS = {True: '?', 
   False: '', 
   None: ''}

class BaseNode(Dto):

    def __eq__(self, o):
        return hash(self) == hash(o)

    def __hash__(self):
        return hash(str(self))

    def format(self):
        return Formatter.format_node(self)

    def format_verbose(self, verbosity=0):
        if verbosity > -1:
            return self.format()
        else:
            return


class ColumnNode(BaseNode):

    def __init__(self, column, indent=0):
        BaseNode.__init__(self)
        self.column = column
        self.indent = indent

    def __hash__(self):
        return hash(str(self.column))

    def __str__(self):
        indent = '  ' * self.indent
        return ('{0}- {1}{2}{3}').format(indent, self.column.name, PRIMARY_KEY_OPTIONS.get(self.column.primary_key), NULLABLE_OPTIONS.get(self.column.nullable))

    def format(self):
        return Formatter.format_column_node(self)

    def format_verbose(self, verbosity=0):
        indent = '  ' * self.indent
        return ('{0}- {1}').format(indent, self.column.ddl())

    @staticmethod
    def from_json(d):
        return ColumnNode(from_json(d['column']), from_json(d['indent']))


class ForeignKeyNode(BaseNode):

    def __init__(self, fk, parent=None, indent=0):
        BaseNode.__init__(self)
        self.fk = fk
        self.parent = parent
        self.indent = indent

    def __str__(self):
        indent = '  ' * self.indent
        if self.fk.a.tablename == self.parent.name:
            return ('{0}→ {1}{3} → {2}').format(indent, self.fk.a.name, self.fk.b, NULLABLE_OPTIONS.get(self.fk.a.nullable))
        return ('{0}↑ {1} ({2} → {3}.{4})').format(indent, self.fk.a.tablename, self.fk.a.name, self.fk.b.tablename, self.fk.b.name)

    def __hash__(self):
        return hash(str(self.fk))

    def format(self):
        return Formatter.format_foreign_key_node(self)

    @staticmethod
    def from_json(d):
        return ForeignKeyNode(from_json(d['fk']), from_json(d['parent']), from_json(d['indent']))


class TableNode(BaseNode):

    def __init__(self, table, indent=0):
        BaseNode.__init__(self)
        self.table = table
        self.indent = indent

    def __str__(self):
        return self.table.name

    def __hash__(self):
        return hash(str(self.table))

    def format(self):
        return Formatter.format_table_node(self)

    @staticmethod
    def from_json(d):
        return TableNode(from_json(d['table']), from_json(d['indent']))


class NameNode(BaseNode):

    def __init__(self, name, indent=0):
        BaseNode.__init__(self)
        self.name = name
        self.indent = indent

    def __str__(self):
        return ('{0}{1}').format('  ' * self.indent, self.name)

    def __hash__(self):
        return hash(self.name)

    def format(self):
        return Formatter.format_name_node(self)

    @staticmethod
    def from_json(d):
        return NameNode(from_json(d['name']), from_json(d['indent']))