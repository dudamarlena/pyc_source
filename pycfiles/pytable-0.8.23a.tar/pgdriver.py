# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/pypgsql/pgdriver.py
# Compiled at: 2006-07-18 16:18:23
"""PyPgSQL PostgreSQL database driver"""
from pytable._postgresql import postgresdriver
from pyPgSQL import PgSQL
from basicproperty import common
from pytable import pypgsql
import decimal

class PGDriver(postgresdriver.PostgresDriver):
    """PyPgSQL PostgreSQL database driver

        This is the most commonly used driver for the
        PyTable module, and as such has had the most testing
        and debugging.  It provides basically all features,
        which are supported by PyTable, and is available
        under a Python-CNRI-style license.
        """
    name = pypgsql.name
    baseModule = PgSQL
    paramstyle = common.StringProperty('paramstyle', 'DBAPI 2.0 parameter-style value', defaultValue=PgSQL.paramstyle)
    threadsafety = common.IntegerProperty('paramstyle', 'DBAPI 2.0 threadsafety value XXX should be an enumeration!', defaultValue=PgSQL.threadsafety)
    apilevel = common.StringProperty('apilevel', 'DBAPI 2.0 apilevel value', defaultValue=PgSQL.apilevel)
    userDescription = 'PostgreSQL database driver (via PyPgSQL)\n\nProvides access to the open-source, cross-platform\nserver-based PostgreSQL database. This driver is\none of the preferred drivers for the system.\n\nThe homepages of PostgreSQL and PyPgSQL are:\n\thttp://www.postgresql.org/\n\thttp://pypgsql.sourceforge.net/\n'

    def getLastOID(cls, cursor):
        """Given a cursor, return last-inserted OID value

                This implementation overrides the base implementation to
                support the (non-standard) use of oidValue instead of
                lastrowid to store the OID value.
                """
        try:
            oidValue = cursor.cursor.oidValue
        except AttributeError:
            oidValue = cursor.oidValue

        return oidValue

    getLastOID = classmethod(getLastOID)
    localTypeRegistry = [ (getattr(PgSQL, name), name[3:].lower()) for name in dir(PgSQL) if name.startswith('PG_') if name == name.upper()
                        ]


PGDriver.copyErrorsFromModule(PgSQL)
if not getattr(PgSQL._quote, 'IS_OVERRIDE', False):
    ORIGINAL_QUOTE = PgSQL._quote

    def _quote(value):
        """Perform quoting on decimal.Decimal instances"""
        if isinstance(value, decimal.Decimal):
            value = str(value)
        value = ORIGINAL_QUOTE(value)
        return value


    _quote.IS_OVERRIDE = True
    PgSQL._quote = _quote