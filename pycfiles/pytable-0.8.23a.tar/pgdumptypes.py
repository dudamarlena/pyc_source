# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/pypgsql/pgdumptypes.py
# Compiled at: 2003-08-02 18:46:25
"""Conversion maps to/from PgSQL and wxoo type declarations"""
from pyPgSQL import PgSQL
from wxoo import typeregistry

def _getInformation(propertyObject):
    """Place holder, will become a customisation point on dbtable eventually"""
    for (typ, name) in typeToRegistryName:
        if typ == propertyObject:
            return typeregistry.TypeRegistry.search(name)

    return


def editorClass(propertyObject):
    """Get editor class for the given propertyObject"""
    information = _getInformation(propertyObject)
    if information:
        return information.gridEditor
    return


def viewerClass(propertyObject):
    """Get viewer class for the given propertyObject"""
    information = _getInformation(propertyObject)
    if information:
        return information.gridViewer
    return


typeToRegistryName = [
 (
  PgSQL.PG_DATE, 'mxDateTime'), (PgSQL.PG_INTERVAL, 'mxDateTimeDelta'), (PgSQL.PG_FLOAT, 'float'), (PgSQL.PG_FLOAT4, 'float'), (PgSQL.PG_FLOAT8, 'float'), (PgSQL.PG_INT2, 'int'), (PgSQL.PG_INT4, 'int'), (PgSQL.PG_INT8, 'long'), (PgSQL.PG_BIGINT, 'long'), (PgSQL.PG_INTEGER, 'int'), (PgSQL.PG_SMALLINT, 'int'), (PgSQL.PG_BYTEA, 'str.long'), (PgSQL.PG_CHAR, 'str'), (PgSQL.PG_TEXT, 'str.long'), (PgSQL.PG_VARCHAR, 'str'), (PgSQL.PG_BOOL, 'bool')]
if __name__ == '__main__':

    def setupPGConnection(dsn='', user='mike', password='pass', host='localhost', database='test'):
        from pyPgSQL import PgSQL
        connection = PgSQL.connect(dsn=dsn, user=user, password=password, host=host, database=database)
        return connection


    connection = setupPGConnection()
    cursor = connection.cursor()
    cursor.execute('select * from temp;')
    for row in cursor.description:
        print row[0], editorClass(row[1])