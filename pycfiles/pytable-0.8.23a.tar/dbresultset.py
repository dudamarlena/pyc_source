# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/dbresultset.py
# Compiled at: 2007-04-01 22:04:08
"""Thick wrapper around a pytable cursor with a result-set"""
from __future__ import generators
from basictypes import typeunion
from basicproperty import propertied, common, basic, weak
from pytable import dbschema, viewschema, sqlquery, lazyresultset

class DBResultSet(lazyresultset.LazyResultSet, propertied.Propertied):
    """A pseudo-sequence with read/write lazy-result-set semantics

        The DBResultSet wraps a pytable cursor which has a
        retrieved result-set to provide access to a controlling
        schema (a table or view schema) and to provide automated
        commit/abort of changes to the generated dbrow objects.

        Via the lazyresultset base-class provides lazy loading
        of the results from the set.
        """
    schema = basic.BasicProperty('schema', 'The controlling schema for this result-set', baseType=typeunion.TypeUnion((
     viewschema.ViewSchema,
     dbschema.TableSchema)))
    cursor = basic.BasicProperty('cursor', 'Pointer to our database cursor (a pytable dbcursor instance)')
    cursorDescription = basic.BasicProperty('cursorDescription', 'The db-api-style cursor description for data-rows\n\n\tThis is used to unify result-set fields with the\n\tcontrolling schema, as the order of fields may\n\tnot match that within the database.\n\t', defaultFunction=lambda property, client: getattr(client, 'description', None) or getattr(client.cursor, 'description', None), setDefaultOnGet=False)
    _rowCache = common.ListProperty('_rowCache', "Cache of row-objects loaded from the database\n\n\tThese rows in the cache are the wrapped objects, that\n\tis, dbrow objects.  Generally there's no need to access\n\tthis property directly.\n\n\tNote: this property shadows the lazyresultset's\n\tattribute to provide documentation.\n\t", defaultFunction=lambda prop, client: [])
    length = common.IntegerProperty('length', "Length of the table if calculated yet, otherwise -1\n\n\tYou should use len( self ), not self.length for any\n\tcode you write.  Length is just part of the\n\tlazyresultset base-class's API.\n\n\tNote: this property shadows the lazyresultset's\n\tattribute to provide documentation.\n\t", defaultValue=-1)

    def __getattr__(self, key):
        """Delegate attribute lookup to our schema if it exists"""
        for target in ('schema', ):
            if key != target:
                resultSet = self.__dict__.get(target, None) or getattr(self.__class__, target, None)
                try:
                    return getattr(resultSet, key)
                except AttributeError:
                    pass

        raise AttributeError('%s instance does not have %r attribute' % (
         self.__class__.__name__,
         key))
        return

    def getProperties(self):
        """Retrieve the properties for this particular result-set"""
        items = self.schema.properties
        result = []
        for field in self.schema.fields:
            result.append(items.get(field.name))

        return result

    def wrapRow(self, data, index):
        """Wrap a single row in our DBRow class"""
        names = [ item[0] for item in self.cursorDescription ]
        data = dict(map(None, names, data))
        return self.schema.itemClass(_DBRow__data=data)