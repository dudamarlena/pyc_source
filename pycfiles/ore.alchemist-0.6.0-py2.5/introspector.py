# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/alchemist/introspector.py
# Compiled at: 2008-09-11 20:29:53
"""
Schema Introspection

$Id: introspector.py 299 2008-05-23 20:31:48Z kapilt $
"""
from zope import interface
from sqlalchemy.databases import information_schema
from sqlalchemy.schema import MetaData, Table
from sqlalchemy import sql
from interfaces import ISchemaIntrospector, ISQLAlchemyMetadata
interface.classImplements(MetaData, ISQLAlchemyMetadata)

class TableSchemaIntrospector(object):
    interface.implements(ISchemaIntrospector)

    def __init__(self, context=None):
        self._metadata = context
        self._information_schema = None
        return

    def keys(self):
        return self._listTables()

    def __iter__(self):
        return self.keys()

    def values(self):
        return list(self.itervalues())

    def itervalues(self):
        return self._getTables()

    def items(self):
        return list(self.iteritems())

    def iteritems(self):
        for table in self.values():
            yield (table.name, table)

    def __len__(self):
        return len(self.keys())

    def __getitem__(self, key):
        return self._getTable(key)

    def __contains__(self, name):
        return self._hasTable(name)

    def get(self, key, default=None):
        try:
            return self._getTable(key)
        except KeyError:
            return default

    def bindEngine(self, engine, schema_name=None):
        self._metadata = MetaData(engine, schema_name)
        self._clear()

    def bindMetadata(self, metadata):
        if not metadata.is_bound():
            raise SyntaxError('metadata bind arguement must be bound')
        self._metadata = metadata
        self._clear()

    def _getMetadata(self):
        if self._metadata is None:
            raise AttributeError('_metadata')
        return self._metadata

    metadata = property(_getMetadata, bindMetadata)
    context = metadata

    def _getInformationSchema(self):
        if self._information_schema is None:
            bound_ischema = MetaData(self.metadata.engine)
            for table in information_schema.ischema.table_iterator():
                table.tometadata(bound_ischema)

            self._information_schema = bound_ischema
        return self._information_schema

    information_schema = property(_getInformationSchema)

    def orderedKeys(self, reverse=False):
        self.values()
        for table in self.metadata.table_iterator(reverse):
            yield table.name

    def itemInfo(self, key):
        return self._getTableInfo(key)

    def _clear(self):
        self._information_schema = None
        return

    def _getTableInfo(self, table_name):
        t = self.information_schema.tables['information_schema.tables']
        s = sql.select()
        if self.metadata.name:
            s.append_whereclause(t.c.table_schema == self.metadata.name)
        s.append_whereclause(t.c.table_name == sql.bindparam('table_name'))
        results = s.execute(table_name=table_name)
        return dict(results[0].items())

    def _getTable(self, table_name):
        if table_name not in self:
            raise KeyError(table_name)
        d = self._tableConstructorArgs(table_name)
        return Table(**d)

    def _tableConstructorArgs(self, table_name):
        d = {'autoload': True, 'useexisting': True}
        if self.metadata.name:
            d['schema'] = self.metadata.name
        d['name'] = table_name
        d['metadata'] = self.metadata
        return d

    def _getTables(self):
        for table_name in self.keys():
            d = self._tableConstructorArgs(table_name)
            yield Table(**d)

    def _listTables(self):
        t = self.information_schema.tables['information_schema.tables']
        s = sql.select([t.c.table_name])
        if self.metadata.name:
            s.append_whereclause(t.c.table_schema == self.metadata.name)
        results = s.execute()
        return [ row[t.c.table_name] for row in results.fetchall() ]

    def _hasTable(self, table_name):
        t = self.information_schema.tables['information_schema.tables']
        s = sql.select([t.c.table_name])
        if self.metadata.name:
            s.append_whereclause(t.c.table_schema == self.metadata.name)
        s.append_whereclause(t.c.table_name == sql.bindparam('table_name'))
        results = s.execute(table_name=table_name)
        return results.rowcount == 1