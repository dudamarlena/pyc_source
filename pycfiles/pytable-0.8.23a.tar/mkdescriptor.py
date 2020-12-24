# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/mk/mkdescriptor.py
# Compiled at: 2003-08-02 18:46:25
from pytable import dbdescriptor
from wxoo import typeregistry
from basicproperty import common

def defaultDataType(property, client):
    """Get a data-type value for client (a property descriptor)"""
    typ = client.description[1]
    for (typCode, name) in client.typeToRegistryName:
        if typ == typCode:
            return name

    return ''


class PGDescriptor(dbdescriptor.DBDescriptor):
    """Property descriptor for PyPgSQL drivers
        """
    __module__ = __name__
    dataType = common.StringProperty('dataType', 'String value declaring a unique type for editor lookups', defaultFunction=defaultDataType)
    typeToRegistryName = [
     (
      PgSQL.PG_DATE, 'mxDateTime'), (PgSQL.PG_INTERVAL, 'mxDateTimeDelta'), (PgSQL.PG_FLOAT, 'float'), (PgSQL.PG_FLOAT4, 'float'), (PgSQL.PG_FLOAT8, 'float'), (PgSQL.PG_INT2, 'int'), (PgSQL.PG_INT4, 'int'), (PgSQL.PG_INT8, 'long'), (PgSQL.PG_BIGINT, 'long'), (PgSQL.PG_INTEGER, 'int'), (PgSQL.PG_SMALLINT, 'int'), (PgSQL.PG_BYTEA, 'str.long'), (PgSQL.PG_CHAR, 'str'), (PgSQL.PG_TEXT, 'str.long'), (PgSQL.PG_VARCHAR, 'str'), (PgSQL.PG_BOOL, 'bool')]