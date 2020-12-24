# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_odbc.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.odbc import ODBCIni, ODBCinstIni
from insights.tests import context_wrap
ODBC_INI = ('\n[myodbc5w]\nDriver       = /usr/lib64/libmyodbc5w.so\nDescription  = DSN to MySQL server\nSERVER       = localhost\nNO_SSPS     = 1\n\n[mysqlDSN]\nDriver      = /usr/lib64/libmyodbc5.so\nSERVER      = localhost\n\n[myodbc]\nDriver=MySQL\nSERVER=localhost\n#NO_SSPS=1\n').strip()

def test_odbc_ini():
    res = ODBCIni(context_wrap(ODBC_INI))
    assert res.data.get('mysqlDSN', 'Driver') == '/usr/lib64/libmyodbc5.so'
    assert res.data.get('mysqlDSN', 'SERVER') == 'localhost'
    assert not res.has_option('mysqlDSN', 'NO_SSPS')
    assert len(res.items('myodbc5w')) == 4
    assert res.getint('myodbc5w', 'NO_SSPS') == 1
    assert res.getint('myodbc5w', 'No_Ssps') == 1
    assert res.getint('myodbc5w', ('NO_SSPS').lower()) == 1
    assert 'myodbc' in res
    assert res.data.get('myodbc', 'Driver') == 'MySQL'
    assert not res.has_option('myodbc', 'NO_SSPS')


ODBCINST_INI = ('\n# Example driver definitions\n\n# Driver from the postgresql-odbc package\n# Setup from the unixODBC package\n[PostgreSQL]\nDescription\t= ODBC for PostgreSQL\nDriver\t\t= /usr/lib/psqlodbcw.so\nSetup\t\t= /usr/lib/libodbcpsqlS.so\nDriver64\t= /usr/lib64/psqlodbcw.so\nSetup64\t\t= /usr/lib64/libodbcpsqlS.so\nFileUsage\t= 1\n\n\n# Driver from the mysql-connector-odbc package\n# Setup from the unixODBC package\n[MySQL]\nDescription\t= ODBC for MySQL\nDriver\t\t= /usr/lib/libmyodbc5.so\nSetup\t\t= /usr/lib/libodbcmyS.so\nDriver64\t= /usr/lib64/libmyodbc5.so\nSetup64\t\t= /usr/lib64/libodbcmyS.so\nFileUsage\t= 1\n').strip()

def test_odbcinst_ini():
    res = ODBCinstIni(context_wrap(ODBCINST_INI))
    assert 'PostgreSQL' in res
    assert 'MySQL' in res
    assert 'XXSQL' not in res
    assert res.data.get('MySQL', 'Driver64') == '/usr/lib64/libmyodbc5.so'