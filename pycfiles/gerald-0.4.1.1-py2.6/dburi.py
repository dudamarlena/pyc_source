# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gerald/utilities/dburi.py
# Compiled at: 2010-10-31 02:23:22
"""
This module provides a series of utility classes and functions to return a 
database connection from a URI.

These URIs are of the form;

 username[:password]@hostname[:instance name][/db name][?key=val[&key=val]]

e.g.

 - 'mysql://username[:password]@host[:port]/database name'
 - 'oracle://username[:password]@tns entry'
 - 'postgres://username[:password]@host[:port]/database name'
 - 'mssql://username[:password]@servername[:instance name]/databasename
 - 'sqlite://path/to/db/file'
 - 'sqlite://C|/path/to/db/file' - On MS Windows
 - 'sqlite://:memory:' - For an in memory database

This module is inspired by (and somewhat borrows from) SQLObject's dbconnection.py, I've just purposely not included a lot of the baggage from that particular module.

This module is licensed under the BSD License (see LICENSE.txt)

To do;
 - Add ODBC support via pyodbc - http://pyodbc.sourceforge.net/
"""
__version__ = (0, 3, 0)
__date__ = (2009, 1, 15)
__author__ = 'Andy Todd <andy47@halfcooked.com>'
import os
from Log import get_log
LOG = get_log(level='INFO')

class Connection(object):
    """Base class for all database specific connection classes"""

    def parse_uri(self, connection_string):
        """Turn the connection_string into a series of parameters to the connect method
        
        Note that connection_string values will be of the form
            username[:password]@hostname[:instance name][/database name][?key=value[&key=value]]
        """
        connection_details = {}
        if connection_string.find('@') != -1:
            (username, rest) = connection_string.split('@')
            if username.find(':') != -1:
                (username, password) = username.split(':')
            else:
                password = None
            if rest.find('?') != -1:
                (rest, key_values) = rest.split('?')
                for key_val_pair in key_values.split('&'):
                    (key, value) = key_val_pair.split('=')
                    connection_details[key] = value

            if rest.find('/') != -1:
                (host, db_name) = rest.split('/')
                if host == '':
                    raise ValueError, 'Connection must include host'
            else:
                host = rest
                db_name = None
            if host.find(':') != -1:
                (host, port) = host.split(':')
                try:
                    port = int(port)
                except ValueError:
                    raise ValueError, "port must be integer, got '%s' instead" % port
                else:
                    if not 1 <= port <= 65535:
                        raise ValueError, "port must be integer in the range 1-65535, got '%d' instead" % port
            else:
                port = None
        else:
            raise ValueError, 'Connection passed invalid connection_string'
        connection_details['user'] = username
        if password:
            connection_details['password'] = password
        connection_details['host'] = host
        if port:
            connection_details['port'] = port
        if db_name:
            connection_details['db_name'] = db_name
        return connection_details


class MySqlConnection(Connection):
    """Class to establish connections to MySQL databases

    The acceptable form of the connection string is;::

        mysql://username[:password]@host[:port]/database name

    The db modules we try (in order of preference) are MySQLdb
    """

    def __init__(self, connection_string):
        """Establish a connection to the MySQL database identified by connection_string"""
        try:
            import MySQLdb as db
        except ImportError:
            raise ImportError, "Can't connect to MySQL as db-api module not present"

        conn_details = self.parse_uri(connection_string)
        if 'db_name' not in conn_details:
            raise ValueError, 'Must supply a database name for MySQL'
        if 'password' not in conn_details:
            conn_details['password'] = None
        if 'port' not in conn_details:
            conn_details['port'] = None
        self.connection = db.connect(user=conn_details['user'] or '', passwd=conn_details['password'] or '', host=conn_details['host'] or 'localhost', port=conn_details['port'] or 0, db=conn_details['db_name'] or '')
        return


class SqliteConnection(Connection):
    """Class to establish connections to Sqlite databases

    The acceptable form of the connection string is;::

        sqlite://path/to/db/file

    The db modules we try (in order of preference) are sqlite3 and pysqlite2
    """

    def __init__(self, connection_string):
        """Establish a connection to the sqlite database identified by connection_string"""
        if not connection_string:
            raise ValueError, 'Cannot connect to sqlite. You must provide a connection string'
        try:
            from sqlite3 import dbapi2 as db
            from sqlite3 import Row
        except ImportError:
            try:
                from pysqlite2 import dbapi2 as db
            except ImportError:
                raise ImportError, "Can't connect to sqlite as db-api module not present"

        if connection_string.find('|') != -1:
            connection_string.replace('|', ':')
        LOG.debug(connection_string)
        self.connection = db.connect(connection_string)
        self.connection.row_factory = Row


class OracleConnection(Connection):
    """Class for connections to Oracle databases

    The acceptable form of the connection string is;::

        oracle://username:password@tns_entry

    The db modules we try (in order of preference) are cx_Oracle and dcoracle2
    """

    def __init__(self, connection_string):
        """Connect to Oracle database identified by connection_string"""
        try:
            import cx_Oracle as db
        except ImportError:
            import dcoracle2 as db

        if connection_string.startswith('/'):
            connection_string = connection_string[1:]
        if connection_string.find(':') != -1:
            connection_string = connection_string.replace(':', '/')
        LOG.debug('Trying to establish connection to Oracle using %s' % connection_string)
        self.connection = db.connect(connection_string)


class PostgresConnection(Connection):
    """Establish a connection to the PostgreSQL database identified by connection_string

    The acceptable form of the connection string is;::

        postgres://username[:password]@host[:port]/database name

    The db modules we try (in order of preference) are psycopg2, pygresql and pyPgSQL
    """

    def __init__(self, connection_string):
        """Connect to the PostgreSQL database identified by connection_string"""
        try:
            import psycopg2 as db
            module = 'psycopg2'
        except ImportError:
            try:
                import pgdb as db
                module = 'pygresql'
            except ImportError:
                from pyPgSQL import PgSQL as db
                module = 'pypgsql'

        connection = self.parse_uri(connection_string)
        if module == 'psycopg2':
            dsn = "user='%s'" % connection['user']
            if connection.has_key('password') and connection['password'] != None:
                dsn += " password='%s'" % connection['password']
            dsn += " host='%s'" % connection['host']
            if connection.has_key('db_name') and connection['db_name'] != '':
                dsn += " dbname='%s'" % connection['db_name']
            if connection.has_key('port') and connection['port'] != None:
                dsn += ' port=%d' % connection['port']
            LOG.debug('Trying to establish connection to Postgres using %s' % dsn)
            self.connection = db.connect(dsn)
        elif module == 'pygresql' or module == 'pypgsql':
            if connection.has_key('port') and connection['port'] != None:
                host = connection['host'] + ':' + connection['port']
            else:
                host = connection['host']
            if connection.has_key('password') and connection['password'] != None:
                self.connection = db.connect(host=host, user=connection['user'], database=connection['db_name'], password=connection['password'])
            else:
                self.connection = db.connect(host=host, user=connection['user'], database=connection['db_name'])
        else:
            raise NotImplementedError
        return


class SqlServerConnection(Connection):
    """Class for connections to SQL Server databases

    The acceptable form of the connection string is;::

        mssql://username[:password]@servername[/databasename]
        [?key=value[&key=value]]

    The db modules we try (in order of preference) are pymssql
    """

    def __init__(self, connection_string):
        """Establish a connect to the SQL Server db identified by connection_string"""
        if not connection_string:
            raise ValueError, 'Cannot connect to SQL Server. You must provide a connection string'
        try:
            import pymssql
        except ImportError:
            raise ImportError, 'Cannot import SQL Server db-api module'

        LOG.debug(connection_string)
        connection = self.parse_uri(connection_string)
        if 'trusted' in connection:
            if connection['trusted'] == 'True':
                connection['trusted'] = True
            elif connection['trusted'] == 'False':
                connection['trusted'] = False
        if 'db_name' in connection:
            connection['host'] = '%s\\%s' % (connection['host'], connection['db_name'])
            del connection['db_name']
        LOG.debug(connection)
        self.connection = pymssql.connect(**connection)


def get_connection(uri):
    """Get and return a database connection based on the uri
    
    The uri scheme is blatantly ripped off from SQLObject_. The general form 
    of these uris is;
     - 'plugin://user:password@host/database name'

    e.g.
     - 'mysql://username[:password]@host[:port]/database name'
     - 'sqlite:/path/to/db/file'
     - 'oracle://username:password@tns entry'
     - 'postgres://username[:password]@host[:port]/database name'
     - 'mssql://username[:password]@servername[:instance name]/databasename

    .. _SQLObject: http://www.sqlobject.org/sqlapi/module-sqlapi.uri.html
    """
    helpers = {'mysql': MySqlConnection, 'sqlite': SqliteConnection, 
       'oracle': OracleConnection, 
       'postgres': PostgresConnection, 
       'mssql': SqlServerConnection}
    (scheme, connection_string) = uri.split('://')
    connection = helpers[scheme](connection_string)
    return connection.connection