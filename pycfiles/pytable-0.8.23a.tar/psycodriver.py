# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/psycopg/psycodriver.py
# Compiled at: 2004-02-19 05:50:21
"""psycopg PostgreSQL database driver"""
from pytable._postgresql import postgresdriver
from pytable import psycopg as pytable_psycopg
from pytable import dbdriver
import psycopg
from basicproperty import common

class PsycoDriver(postgresdriver.PostgresDriver):
    """psycopg PostgreSQL database driver

        PsycoDriver is a minor customisation of the PyPgSQL
        driver to allow interoperation with psycopg.  Note that
        psycopg is a *GPL* licensed driver.  If you include it
        in your project you must abide by the restrictions of
        the GPL.

        The wrapper here includes no GPL code, so should not be
        under any GPL restrictions as long as it is not bundled
        with GPL code.
        """
    __module__ = __name__
    name = pytable_psycopg.name
    baseModule = psycopg
    capabilities = dbdriver.DriverCapabilities(serial=1, inherits=1, queryUnicode=0)
    paramstyle = common.StringProperty('paramstyle', 'DBAPI 2.0 parameter-style value', defaultValue=psycopg.paramstyle)
    threadsafety = common.IntegerProperty('paramstyle', 'DBAPI 2.0 threadsafety value XXX should be an enumeration!', defaultValue=psycopg.threadsafety)
    apilevel = common.StringProperty('apilevel', 'DBAPI 2.0 apilevel value', defaultValue=psycopg.apilevel)
    userDescription = 'PostgreSQL database driver (via psycopg)\n\nProvides access to the open-source, cross-platform\nserver-based PostgreSQL database.\n\nWARNING:\n\tBecause of GPL restrictions psycopg is not a\n\tprefered driver for the system, but it does\n\tconnect to PostgreSQL, which is the prefered\n\tdatabase, and should be functionally equivalent\n\tto PyPgSQL\n\nThe homepages of PostgreSQL and psycopg are:\n\thttp://www.postgresql.org/\n\thttp://initd.org/software/initd/psycopg\n'
    localTypeRegistry = []
    for _name in ['BOOLEAN', 'BINARY', 'DATE', 'DATETIME', 'FLOAT', 'INTEGER', 'INTERVAL', 'LONGINTEGER', 'NUMBER', 'ROWID', 'STRING', 'TIME']:
        for _num in getattr(psycopg, _name).values:
            localTypeRegistry.append((_num, _name.lower()))

    del _name
    del _num


PsycoDriver.copyErrorsFromModule(psycopg)