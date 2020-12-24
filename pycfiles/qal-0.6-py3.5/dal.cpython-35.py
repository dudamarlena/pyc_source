# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/qal/dal/dal.py
# Compiled at: 2016-04-12 13:41:36
# Size of source mod 2**32: 15239 bytes
"""
    ************************************
    qal.dal - Database Abstraction Layer
    ************************************
    
    The goal with DAL is to hide the connection-related differences between the most common database backends.
    
    :copyright: Copyright 2010-2014 by Nicklas Boerjesson
    :license: BSD, see LICENSE for details.
"""
from qal.common.meta import readattr
from qal.dal.types import DB_MYSQL, DB_POSTGRESQL, DB_ORACLE, DB_DB2, DB_SQLSERVER, string_to_db_type, db_type_to_string, DB_SQLITE
from qal.dal.conversions import parse_description, python_type_to_sql_type
from qal.common.discover import import_error_to_help

class DatabaseAbstractionLayer(object):
    __doc__ = 'This class abstracts the different peculiarities of the different database backends with\n    regards to connection details'
    on_connect = None
    connected = False
    connection = None
    db_type = None
    server = ''
    databasename = ''
    username = ''
    password = ''
    instance = ''
    driver = None
    autocommit = True
    port = None
    field_names = None
    field_types = None
    _pg_xact = None

    def read_resource_settings(self, _resource):
        """
        Read settings from a resource object
        :param _resource: A resource object
        """
        if _resource.type.upper() != 'RDBMS':
            raise Exception('DAL.read_resource_settings error: Wrong resource type - ' + _resource.type)
        self.db_type = string_to_db_type(_resource.db_type)
        self.server = readattr(_resource, 'server')
        self.databasename = readattr(_resource, 'databasename')
        self.username = readattr(_resource, 'username')
        self.password = readattr(_resource, 'password')
        self.port = readattr(_resource, 'port')
        self.autocommit = readattr(_resource, 'autocommit', False)
        self.instance = readattr(_resource, 'instance')

    def write_resource_settings(self, _resource):
        """
        Write settings to a resource object
        :param _resource: A resource object.
        """
        _resource.type = 'RDBMS'
        _resource.db_type = db_type_to_string(self.db_type)
        _resource.server = self.server
        _resource.databasename = self.databasename
        _resource.username = self.username
        _resource.password = self.password
        if hasattr(_resource, 'autocommit'):
            _resource.autocommit = self.autocommit
        if hasattr(_resource, 'port'):
            _resource.port = self.port
        if hasattr(_resource, 'instance'):
            _resource.instance = self.instance

    def connect_to_db(self):
        """Connects to the database"""
        if self.db_type == DB_MYSQL:
            try:
                import pymysql
            except ImportError as _err:
                raise Exception(import_error_to_help(_module='pymysql', _err_obj=_err, _pip_package='pymysql3', _apt_package=None, _win_package=None))

            _connection = pymysql.connect(host=self.server, db=self.databasename, user=self.username, passwd=self.password)
        else:
            if self.db_type == DB_POSTGRESQL:
                try:
                    import postgresql.driver as pg_driver
                except ImportError as _err:
                    raise Exception(import_error_to_help(_module='postgresql', _err_obj=_err, _pip_package='py-postgresql', _apt_package='python3-postgresql', _win_package=None, _import_comment='2014-04-16: If using apt-get on Debian, ' + 'check so version is > 1.0.3-2' + ' as there is a severe bug in the 1.0.2 version. ' + 'See https://bugs.debian.org/cgi-bin/bugreport' + '.cgi?bug=724597'))

                if self.port is None or self.port == '' or self.port == 0:
                    _port = 5432
                else:
                    _port = self.port
                _connection = pg_driver.connect(host=self.server, database=self.databasename, user=self.username, password=self.password, port=_port)
            elif self.db_type in [DB_SQLSERVER, DB_DB2]:
                _connection_string = None
                try:
                    import pyodbc
                except ImportError as _err:
                    raise Exception(import_error_to_help(_module='pyodbc', _err_obj=_err, _pip_package='pyodbc', _apt_package=None, _win_package=None, _import_comment='(For Linux) 2014-04-16: ' + 'No apt package (python3-pyodbc)' + ' available at this time.'))

                import platform
        if self.db_type == DB_SQLSERVER:
            if platform.system().lower() in ('linux', 'darwin'):
                _connection_string = 'DRIVER={FreeTDS};SERVER=' + self.server + ';DATABASE=' + self.databasename + ';TDS_VERSION=8.0;UID=' + self.username + ';PWD=' + self.password + ';PORT=' + str(self.port) + ';Trusted_Connection=no;'
            else:
                if platform.system().lower() == 'windows':
                    _connection_string = 'Driver={SQL Server};Server=' + self.server + ';DATABASE=' + self.databasename + ';UID=' + self.username + ';PWD=' + self.password + ';PORT=' + str(self.port) + ';Trusted_Connection=no'
                else:
                    raise Exception('connect_to_db: SQL Server connections on ' + platform.system() + ' not supported yet.')
        else:
            if self.db_type == DB_DB2:
                if platform.system().lower() in ('linux', 'darwin'):
                    drivername = 'DB2'
                else:
                    if platform.system().lower() == 'windows':
                        drivername = '{IBM DATA SERVER DRIVER for ODBC - C:/PROGRA~1/IBM}'
                    else:
                        raise Exception('connect_to_db: DB2 connections on ' + platform.system() + ' not supported yet.')
                    _connection_string = 'Driver=' + drivername + ';Database=' + self.databasename + ';hostname=' + self.server + ';port=' + str(self.port) + ';protocol=TCPIP; uid=' + self.username + '; pwd=' + self.password
                print('Connect to database using connection string:  ' + _connection_string)
                _connection = pyodbc.connect(_connection_string, autocommit=self.autocommit)
            else:
                if self.db_type == DB_ORACLE:
                    try:
                        import cx_Oracle
                    except ImportError as _err:
                        raise Exception(import_error_to_help(_module='cx_Oracle', _err_obj=_err, _pip_package='cx_Oracle', _apt_package=None, _win_package='Download and install binary .msi package from ' + 'http://cx-oracle.sourceforge.net/ and install.', _import_comment='(Linux) 2014-04-16: No python3-pyodbc available' + ' at build time.'))

                    _connection_string = self.username + '/' + self.password + '@' + self.server + ':' + str(self.port) + '/' + self.instance
                    print('Connect to database using connection string:  ' + _connection_string)
                    _connection = cx_Oracle.connect(_connection_string)
                    _connection.autocommit = self.autocommit
                else:
                    if self.db_type == DB_SQLITE:
                        try:
                            import sqlite3
                        except ImportError as _err:
                            raise Exception('Error importing SQLite3, which is built-in into Python, check your Python installation. Error: ' + str(_err))

                        _connection = sqlite3.connect(self.databasename)
                    else:
                        raise Exception('connect_to_db: Invalid database type.')
        self.connection = _connection
        if self.on_connect:
            self.on_connect()
        self.connected = True
        return _connection

    def __init__(self, _resource=None, _connect=True):
        """

        :param _resource: A resource object to read settings from
        :param _connect: Also connect to the database (default:True)
        """
        self.on_connect = None
        if _resource is not None:
            self.resource = _resource
            self.read_resource_settings(_resource)
            if _connect:
                self.connect_to_db()

    def execute(self, _sql):
        """Execute the SQL statement, expect no dataset"""
        print('Info: dal.execute() at ' + str(self) + '/' + str(self.connection) + ' running the following SQL:\n' + str(_sql))
        if self.db_type == DB_POSTGRESQL:
            self.connection.execute(_sql)
        else:
            cur = self.connection.cursor()
            cur.execute(_sql)

    @staticmethod
    def _make_positioned_params(_input, _db_type):
        _arg_idx = 1
        _output = _input
        if _db_type == DB_POSTGRESQL:
            _prefix = '$'
        elif _db_type == DB_ORACLE:
            _prefix = ':'
        for _curr_idx in range(0, len(_input)):
            _chunk = _input[_curr_idx:_curr_idx + 2]
            if _chunk == '%s':
                _output = _output.replace(_chunk, _prefix + str(_arg_idx), 1)
                _arg_idx += 1
            elif _chunk == '%d':
                _output = _output.replace(_chunk, _prefix + str(_arg_idx), 1)
                _arg_idx += 1

        return _output

    def executemany(self, _sql, _values):
        """Execute the SQL statements , expect no dataset"""
        if self.db_type == DB_POSTGRESQL:
            _sql = self._make_positioned_params(_sql, DB_POSTGRESQL)
            _prepared = self.connection.prepare(_sql)
            print(_sql)
            for _row in _values:
                _prepared(*_row)

            return
        if self.db_type in [DB_SQLSERVER, DB_DB2, DB_SQLITE]:
            _sql = _sql.replace('%d', '?').replace('%s', '?')
        elif self.db_type in [DB_ORACLE]:
            _sql = self._make_positioned_params(_sql, DB_ORACLE)
        cur = self.connection.cursor()
        cur.executemany(_sql, _values)

    def query(self, _sql):
        """Execute the SQL statement, get a dataset"""
        if self.connection is None:
            raise Exception('Error: dal.query() is called without a database connection. Query:\n' + _sql)
        print('Info: dal.query() at ' + str(self) + '/' + str(self.connection) + ' running the following SQL:\n' + _sql)
        if self.db_type == DB_POSTGRESQL:
            _ps = self.connection.prepare(_sql)
            _res = _ps()
            if _ps.column_names is not None:
                self.field_names = _ps.column_names
                self.field_types = []
                for _curr_type in _ps.column_types:
                    self.field_types.append(python_type_to_sql_type(_curr_type))

        else:
            cur = self.connection.cursor()
            cur.execute(_sql)
            self.field_names, self.field_types = parse_description(cur.description, self.db_type)
            _res = cur.fetchall()
        _results = []
        for _row in _res:
            _results.append(list(_row))

        if self.db_type == DB_ORACLE:
            import cx_Oracle
            if cx_Oracle.BLOB in self.field_types:
                for _curr_row_idx, _curr_row in enumerate(_results):
                    for _curr_col_idx, _curr_col in enumerate(_curr_row):
                        if isinstance(_curr_col, cx_Oracle.LOB):
                            _results[_curr_row_idx][_curr_col_idx] = _curr_col.read()

        return _results

    def close(self):
        """Close the database connection"""
        self.connection.close()

    def start(self):
        """Start transaction"""
        if self.db_type == DB_POSTGRESQL and self._pg_xact is None:
            self._pg_xact = self.connection.xact()
            self._pg_xact.start()
        else:
            self.execute('START TRANSACTION')

    def commit(self):
        """Commit the transaction"""
        if self.db_type == DB_POSTGRESQL:
            if self._pg_xact is not None:
                self._pg_xact.commit()
                self._pg_xact = None
        else:
            self.connection.commit()

    def rollback(self):
        """Rollback the transaction"""
        if self.db_type == DB_POSTGRESQL:
            self._pg_xact.rollback()
            self._pg_xact = None
        self.connection.rollback()