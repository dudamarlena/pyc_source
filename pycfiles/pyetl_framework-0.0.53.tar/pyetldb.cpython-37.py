# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pyetldb\pyetldb.py
# Compiled at: 2020-01-23 12:43:55
# Size of source mod 2**32: 32229 bytes
__project__ = 'pyetldb'
__version__ = '0.1'
__author__ = 'natanaelfneto'
__authoremail__ = 'natanaelfneto@outlook.com'
__source__ = 'https://github.com/natanaelfneto/pyetldb'
short_description = 'Python module that allows an easy interconnection between Microsoft Access and a support server for SQL with data sync'
__description__ = f"This Python module: {short_description}"
import argparse, getpass, logging, os, pathlib, sys, time, unidecode, pypyodbc, pyodbc, psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime
import cx_Oracle

class DatabaseCrawler(object):

    def __init__(self):
        """
            Initiate a Main instance
        """
        pass

    def __enter__(self):
        """
            Function for entering class with python 3 standards of
            'with' parameter and a following __exit__ function for
            a cleanner use of the class instancies
        """
        try:
            return self
        except StopIteration:
            raise RuntimeError('Instance could not be returned')

    def sync(self, debug=False, source=None, target=None):
        databases = connect(debug=debug, databases=[source, target])
        source = databases[str(source)]
        target = databases[str(target)]
        LOGGER.adapter.info(f"Start syncing data from {source.provider} to {target.provider}...")
        if target.provider == Interface().db.ORACLE():
            target_cursor = target.database.connection.cursor()
            query = f"\n                SELECT\n                    table_name\n                FROM\n                    all_tables\n                WHERE \n                    owner = '{target.database.dsn.user}' OR\n                    owner = '{target.database.dsn.user.upper()}'\n            "
            target_cursor.execute(query)
            target_tables = [table[0] for table in target_cursor.fetchall()]
            target_cursor.close()
            if len(target_tables) == len([]):
                LOGGER.adapter.debug(f"Database for user: {target.database.dsn.user} does not exist. Please create ir first.")
            if source.provider == Interface().db.ODBC():
                source_cursor = source.database.connection.cursor()
                tables = list(filter(None, [table[2] if 'msy' not in str(table).lower() else None for table in source_cursor.tables()]))
                LOGGER.adapter.info(f"Found {len(tables)} tables to be copied")
                source_cursor.close()
                LOGGER.adapter.info('Copying...')
                for count, table in enumerate(tables, 1):
                    LOGGER.adapter.debug(f"Copying {count} out of {len(tables)} found tables")
                    table_name = table.replace(' ', '_').replace('-', '_').lower()
                    LOGGER.adapter.debug(f"Copying {table} as {table_name}")
                    source_cursor = source.database.connection.cursor()
                    try:
                        columns = source_cursor.columns(table=table)
                        columns = [{'name':unidecode.unidecode(column[3]),  'datatype':column[5],  'lenght':column[6],  'table':table} for column in columns]
                    except:
                        columns = []

                    query = f'SELECT * FROM "{table.lower()}"'
                    LOGGER.adapter.debug(f"Querying: {query}")
                    try:
                        source_cursor.execute(query)
                        rows = source_cursor.fetchall()
                        source_cursor.close()
                    except:
                        rows = []

                    LOGGER.adapter.debug(f"Table has {len(rows)} rows with {len(columns)} columns")
                    cleared_columns = []
                    uncleared_columns = []
                    columns_with_datatypes = []
                    for column in columns:
                        column_name = column['name'].lower()
                        cleared_column_name = column['name'].replace('-', '_').replace(' ', '_').replace('#', '').lower()
                        datatype = column['datatype']
                        lenght = f"({column['lenght']})"
                        if datatype == 'DATETIME':
                            datatype = 'TIMESTAMP'
                            lenght = '(0)'
                        else:
                            datatype = 'varchar2'
                            lenght = '(1000)'
                        column_with_datatype = f"{cleared_column_name} {datatype}{lenght}"
                        if column_with_datatype in columns_with_datatypes:
                            column_with_datatype = f"{cleared_column_name}_ {datatype}{lenght} NULL"
                        columns_with_datatypes.append(column_with_datatype)
                        cleared_columns.append(cleared_column_name)
                        if cleared_column_name == column_name:
                            uncleared_columns.append(column_name)
                        else:
                            uncleared_columns.append(f'"{column_name}" as {cleared_column_name}')

                    table_name = unidecode.unidecode(f"pyetl_{table_name}")
                    if not columns_with_datatypes:
                        LOGGER.adapter.debug(f"No value to be retrieved from {table_name}")
                    else:
                        query = f"CREATE TABLE {table_name} ({', '.join(columns_with_datatypes)})"
                        LOGGER.adapter.debug(f"Querying: {query}")
                        if not table_name in target_tables:
                            if not table_name.upper() in target_tables:
                                target_cursor = target.database.connection.cursor()
                                target_cursor.execute(query)
                                target_cursor.close()
                                target_cursor = target.database.connection.cursor()
                                query = f"TRUNCATE {table_name}; COMMIT;"
                                target_cursor.execute(query)
                                target_cursor.close()
                        for count, row in enumerate(rows):
                            cleared_row = []
                            for value in row:
                                if type(value) in [type(''), type(1)]:
                                    cleared_row.append(value)
                                    continue
                                if type(value) == type(datetime(2000, 1, 1, 1, 1)):
                                    cleared_row.append(f"#timestamp#{value}")
                                elif type(value) == type(None):
                                    cleared_row.append(None)
                                elif 'bytearray' in str(value):
                                    s = str(value)
                                    found = s[s.find('(') + 3:s.find(')') - 1]
                                    arr = bytearray(found, 'utf-8')
                                    cleared_row.append(1)
                                elif str(value) == str(True):
                                    cleared_row.append(True)
                                elif str(value) == str(False):
                                    cleared_row.append(False)
                                else:
                                    cleared_row.append(str(value))

                            row = [f"'{value}'" if value else 'NULL' for value in cleared_row]
                            row = [True if str(value) == str(True) else value for value in row]
                            row = [False if str(value) == str(False) else value for value in row]
                            row = [f"TO_DATE({value.replace('#timestamp#', '')}, 'yyyy/mm/dd hh24:mi:ss')" if '#timestamp#' in value else value for value in row]
                            target_cursor = target.database.connection.cursor()
                            query = f"INSERT INTO {table_name} ({', '.join(cleared_columns)}) VALUES ({', '.join(row)})"
                            LOGGER.adapter.debug(f"Querying: {query}")
                            target_cursor.execute(query)
                            target.database.connection.commit()
                            target_cursor.close()
                            print(f"Inserted {count} of {len(rows)} rows in {target.provider}'s {table_name} from {source.provider}'s {table_name}", end='\r')

        if target.provider == Interface().db.POSTGRES():
            target.database.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            target_cursor = target.database.connection.cursor()
            query = f"\n                SELECT\n                    datname\n                FROM\n                    pg_catalog.pg_database\n                WHERE \n                    datname = '{target.database.dsn.name}'\n            "
            target_cursor.execute(query)
            target_database = [db for db in target_cursor.fetchall()]
            target_cursor.close()
            if len(target_database) == len([]):
                LOGGER.adapter.debug(f"Database {target.database.dsn.name} does not exist. Creating...")
                target_cursor = target.database.connection.cursor()
                query = f"CREATE DATABASE {target.database.dsn.name}"
                LOGGER.adapter.debug(f"Querying {query}")
                target_cursor.execute(query)
                target_cursor.close()
            if source.provider == Interface().db.ODBC():
                source_cursor = source.database.connection.cursor()
                tables = [table[2] for table in source_cursor.tables()]
                LOGGER.adapter.info(f"Found {len(tables)} tables to be copied")
                source_cursor.close()
                LOGGER.adapter.info('Copying...')
                for count, table in enumerate(tables, 1):
                    LOGGER.adapter.debug(f"Copying {count} out of {len(tables)} found tables")
                    table_name = table.replace(' ', '_').replace('-', '_').lower()
                    LOGGER.adapter.debug(f"Copying {table} as {table_name}")
                    source_cursor = source.database.connection.cursor()
                    try:
                        columns = source_cursor.columns(table=table)
                        columns = [{'name':column[3],  'datatype':column[5],  'lenght':column[6],  'table':table} for column in columns]
                    except:
                        columns = []

                    query = f'SELECT * FROM "{table.lower()}"'
                    LOGGER.adapter.debug(f"Querying: {query}")
                    try:
                        source_cursor.execute(query)
                        rows = source_cursor.fetchall()
                        source_cursor.close()
                    except:
                        rows = []

                    LOGGER.adapter.debug(f"Table has {len(rows)} rows with {len(columns)} columns")
                    cleared_columns = []
                    uncleared_columns = []
                    columns_with_datatypes = []
                    for column in columns:
                        column_name = column['name'].lower()
                        cleared_column_name = column['name'].replace('-', '_').replace(' ', '_').replace('#', '').lower()
                        datatype = column['datatype']
                        lenght = f"({column['lenght']})"
                        if datatype == 'DATETIME':
                            datatype = 'TIMESTAMP'
                        else:
                            datatype = 'character varying'
                            lenght = ''
                        column_with_datatype = f"{cleared_column_name} {datatype}{lenght}"
                        if column_with_datatype in columns_with_datatypes:
                            column_with_datatype = f"{cleared_column_name}_ {datatype}{lenght} NULL"
                        columns_with_datatypes.append(column_with_datatype)
                        cleared_columns.append(cleared_column_name)
                        if cleared_column_name == column_name:
                            uncleared_columns.append(column_name)
                        else:
                            uncleared_columns.append(f'"{column_name}" as {cleared_column_name}')

                    query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_with_datatypes)});"
                    LOGGER.adapter.debug(f"Querying: {query}")
                    if 'msy' not in str(table).lower():
                        target_cursor = target.database.connection.cursor()
                        target_cursor.execute(query)
                        target_cursor.close()
                        target_cursor = target.database.connection.cursor()
                        query = f"TRUNCATE {table_name}"
                        target_cursor.execute(query)
                        target_cursor.close()
                        for count, row in enumerate(rows):
                            cleared_row = []
                            for value in row:
                                if type(value) in [type(''), type(1)]:
                                    cleared_row.append(value)
                                    continue
                                if type(value) == type(datetime(2000, 1, 1, 1, 1)):
                                    cleared_row.append(str(value))
                                elif type(value) == type(None):
                                    cleared_row.append(None)
                                elif 'bytearray' in str(value):
                                    s = str(value)
                                    found = s[s.find('(') + 3:s.find(')') - 1]
                                    arr = bytearray(found, 'utf-8')
                                    cleared_row.append(1)
                                elif str(value) == str(True):
                                    cleared_row.append(True)
                                elif str(value) == str(False):
                                    cleared_row.append(False)
                                else:
                                    cleared_row.append(str(value))

                            row = [f"'{value}'" if value else 'NULL' for value in cleared_row]
                            row = [True if str(value) == str(True) else value for value in row]
                            row = [False if str(value) == str(False) else value for value in row]
                            target_cursor = target.database.connection.cursor()
                            query = f"INSERT INTO {table_name} ({', '.join(cleared_columns)}) VALUES ({', '.join(row)})"
                            print(query)
                            LOGGER.adapter.debug(f"Querying: {query}")
                            target_cursor.execute(query)
                            target_cursor.close()
                            print(f"Inserted {count} of {len(rows)} rows in {target.provider}'s {table_name} from {source.provider}'s {table_name}", end='\r')

        LOGGER.adapter.debug('Waiting to finish runtime...')

    def __exit__(self, exc_type, exc_value, traceback):
        self = None


class DataSourceName(object):

    def __init__(self, database_type=None):
        """
            Initiate a Main instance
        """
        self.database = lambda : None
        self.dsn = lambda : None
        self.error = lambda : None
        self.error.status = True
        self.error.message = None
        self.type = database_type
        self.connection = None

    def __enter__(self):
        """
            Function for entering class with python 3 standards of
            'with' parameter and a following __exit__ function for
            a cleanner use of the class instancies
        """
        try:
            return self
        except StopIteration:
            raise RuntimeError('Instance could not be returned')

    def parse_dsn(self, source=None):
        dsn = lambda : None
        try:
            dsn.engine = source.get('ENGINE', None)
            dsn.name = source.get('NAME', None)
            dsn.user = source.get('USER', None)
            dsn.host = source.get('HOST', None)
            dsn.port = source.get('PORT', None)
            dsn.password = source.get('PASSWORD', None)
        except Exception as e:
            try:
                dsn.engine = None
                dsn.name = source
            finally:
                e = None
                del e

        self.dsn = dsn

    def __exit__(self, exc_type, exc_value, traceback):
        self = None


class Interface(object):

    def __init__(self):
        """
            Initiate a Main instance
        """
        self.db = lambda : None
        self.db.ODBC = lambda : 'ODBC'
        self.db.ODBC.drivers = lambda : pypyodbc.drivers()
        self.db.ODBC.drivers_count = len(self.db.ODBC.drivers())
        self.db.POSTGRES = lambda : 'POSTGRESQL'
        self.db.MYSQL = lambda : 'MYSQL'
        self.db.SQLITE = lambda : 'SQLITE'
        self.db.ORACLE = lambda : 'ORACLE'
        self.db.ALL = lambda : [att for att in dir(self.db) if att not in dir(lambda : None) if att != 'ALL']

    def __enter__(self):
        """
            Function for entering class with python 3 standards of
            'with' parameter and a following __exit__ function for
            a cleanner use of the class instancies
        """
        try:
            return self
        except StopIteration:
            raise RuntimeError('Instance could not be returned')

    def database_classifier(self, databases):
        classified_databases = {}
        for count, database in enumerate(databases):
            LOGGER.adapter.debug(f"Running classifier function on source {count}...")
            classified_databases[str(database)] = None
            data = lambda : None
            data.database = None
            data.provider = None
            if isinstance(database, pathlib.Path):
                LOGGER.adapter.debug(f"Trying to parse database as {self.db.ODBC()}...")
                connection = self.connect(self.db.ODBC(), database)
                provider = self.db.ODBC()
            else:
                for SQL_DB in self.db.ALL():
                    if SQL_DB != self.db.ODBC():
                        LOGGER.adapter.debug(f"Trying to parse database as {getattr(self.db, SQL_DB)()}...")
                        connection = self.connect(getattr(self.db, SQL_DB)(), database)
                        if connection.error.status == False:
                            provider = getattr(self.db, SQL_DB)()
                            break

            data.database = connection
            connection = None
            data.provider = provider
            provider = None
            classified_databases[str(database)] = data

        return classified_databases

    def parse_as_odbc(self, source=None):
        for count, driver in enumerate(self.db.ODBC.drivers(), 1):
            error_status = False
            self.dsn = f"Driver={{{driver}}};DBQ={source}"
            LOGGER.adapter.debug(f"Atempt {count} of {self.db.ODBC.drivers_count} to make connection using ODBC driver: {driver}...")
            if count < 8:
                try:
                    connection = pypyodbc.connect(self.dsn)
                    LOGGER.adapter.debug(f"SUCCESS on connection using ODBC driver: {driver}")
                except Exception as e:
                    try:
                        LOGGER.adapter.debug(f"FAIL on connection using ODBC driver: {driver} due to {e}")
                        connection, error_status = (None, True)
                    finally:
                        e = None
                        del e

                if error_status == False:
                    break

        return (
         connection, error_status)

    def parse_as_postgresql(self, dsn={}):
        error_status = False
        try:
            connection = psycopg2.connect(dbname=(dsn.name),
              user=(dsn.user),
              host=(dsn.host),
              password=(dsn.password),
              port=(dsn.port))
            dsn_parameters = connection.get_dsn_parameters()
            LOGGER.adapter.debug(f"SUCCESS on connection using DSN: {dsn_parameters}")
        except Exception as e:
            try:
                LOGGER.adapter.debug(f"FAIL on connection using DSN: {dsn} due to {e}")
                connection, error_status = (None, True)
            finally:
                e = None
                del e

        return (
         connection, error_status)

    def parse_as_mysql(self, dsn={}):
        return (None, True)

    def parse_as_sqlite(self, dsn={}):
        return (None, True)

    def parse_as_oracle(self, dsn={}):
        error_status = False
        try:
            connection = cx_Oracle.connect(dsn.user, dsn.password, dsn.name)
            pseudo_dsn = f"{dsn.engine}://{dsn.name}"
            LOGGER.adapter.debug(f"SUCCESS on connection using DSN: {pseudo_dsn}")
        except Exception as e:
            try:
                LOGGER.adapter.debug(f"FAIL on connection using DSN: {pseudo_dsn} due to {e}")
                connection, error_status = (None, True)
            finally:
                e = None
                del e

        return (
         connection, error_status)

    def connect(self, database_type, source):
        connection = DataSourceName(database_type)
        connection.parse_dsn(source)
        if connection.type == self.db.ODBC():
            connection.connection, connection.error.status = self.parse_as_odbc(source)
        elif connection.type == self.db.POSTGRES() and connection.dsn.engine.upper() == self.db.POSTGRES():
            pseudo_dsn = f"{connection.dsn.engine}://{connection.dsn.user}@{connection.dsn.host}:{connection.dsn.port}/{connection.dsn.name}"
            LOGGER.adapter.debug(f"Atempt to make {self.db.POSTGRES()} connection using DSN: {pseudo_dsn}...")
            connection.connection, connection.error.status = self.parse_as_postgresql(connection.dsn)
        elif connection.type == self.db.MYSQL() and connection.dsn.engine.upper() == self.db.MYSQL():
            LOGGER.adapter.debug(f"Connections with {self.db.MYSQL()} to be available in future release")
            connection.connection, connection.error.status = self.parse_as_mysql(connection.dsn)
        elif connection.type == self.db.SQLITE() and connection.dsn.engine.upper() == self.db.SQLITE():
            LOGGER.adapter.debug(f"Connections with {self.db.SQLITE()} to be available in future release")
            connection.connection, connection.error.status = self.parse_as_sqlite(connection.dsn)
        elif connection.type == self.db.ORACLE():
            if connection.dsn.engine.upper() == self.db.ORACLE():
                pseudo_dsn = f"{connection.dsn.engine}://{connection.dsn.name}"
                LOGGER.adapter.debug(f"Atempt to make {self.db.ORACLE()} connection using DSN: {pseudo_dsn}...")
                connection.connection, connection.error.status = self.parse_as_oracle(connection.dsn)
        return connection

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class Validity(object):

    def __init__(self):
        """ 
            Initiate a Path Validity instance.
        """
        self.logger = logger.adapter

    def path_check(self, files):
        """
            Function to check if each parsed path is a valid system file
            and if it can be accessed by the code.

            Arguments:
                paths: array of files to be checked
        """
        valid_files = []
        self.logger.debug('Checking validity of inputed sources')
        for analysed_file in files:
            if os.access(analysed_file, os.F_OK):
                if os.access(analysed_file, os.R_OK):
                    if os.path.isfile(analysed_file):
                        if DEBUG:
                            output = f"Source path {analysed_file} was successfully parsed"
                            self.logger.debug(output)
                        valid_files.append(analysed_file)
            if DEBUG:
                output = f"Source path {analysed_file} could not be accessed as a file"
                self.logger.debug(output)

        return valid_files


class Logger(object):

    def __init__(self):
        """ 
            Initiate a Logger instance.
            Argument:
                logger: a logging instance for output and log
        """
        self.folder = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../log/'))
        if not os.path.exists(self.folder):
            try:
                os.makedirs(self.folder)
            except Exception as e:
                try:
                    raise ValueError(f"Log folder: {self.folder} could not be created, error: {e}")
                    sys.exit()
                finally:
                    e = None
                    del e

        formatter = logging.Formatter('%(asctime)-8s %(levelname)-5s [%(project)s-%(version)s] user: %(user)s LOG: %(message)s')
        adapter = logging.getLogger(f"{__project__}-{__version__}")
        if not len(adapter.handlers):
            adapter.setLevel('INFO')
            if DEBUG == True:
                adapter.setLevel('DEBUG')
            file_handler = logging.FileHandler(f"{self.folder}/{__project__}.log")
            file_handler.setFormatter(formatter)
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            adapter.addHandler(file_handler)
            adapter.addHandler(stream_handler)
        self.adapter = logging.LoggerAdapter(adapter,
          extra={'project':__project__, 
         'version':__version__, 
         'user':getpass.getuser()})

    def __enter__(self):
        """
            Function for entering class with python 3 standards of
            'with' parameter and a following __exit__ function for
            a cleanner use of the class instancies
        """
        try:
            return self
        except StopIteration:
            raise RuntimeError('Instance could not be returned')

    def __exit__(self, exc_type, exc_value, traceback):
        LOGGER = None
        self = None


def args(args):
    """
        Main function for terminal call of library
        Arguments:
            args: receive all passed arguments and filter them using
                the argparser library
    """
    parser = argparse.ArgumentParser(description=short_description)
    parser.add_argument('sources',
      nargs='+',
      help='Microsoft Access .mdb and .accdb files paths',
      default=[])
    parser.add_argument('target',
      nargs='+',
      help='connection parameters of target SQL database',
      default={})
    parser.add_argument('-d',
      '--debug', action='store_true',
      help='enable debug log',
      default=False,
      required=False)
    parser.add_argument('-v',
      '--version', action='version',
      help='output software version',
      default=False,
      version=(__project__ + '-' + __version__))
    args = parser.parse_args(args)
    interface(debug=(args.debug),
      sources=(args.sources),
      target=(args.target))


def connect(debug=False, databases=[]):
    global DEBUG
    global LOGGER
    DEBUG = debug
    with Logger() as (logger):
        LOGGER = logger
        LOGGER.adapter.info(f"DEBUG flags was setted as: {DEBUG}")
        LOGGER.adapter.info('An application transaction was created due to command or module call...')
        LOGGER.adapter.info(f"Log file is being stored at directory: {logger.folder}")
        LOGGER.adapter.info('Begining database classifier instance...')
        LOGGER.adapter.info(f"Instance found {len(databases)} sources to be parsed as database")
        interface = Interface()
        output = ''
        for count, database in enumerate(databases, 1):
            output += f"\t{count}: {database}\n"

        LOGGER.adapter.info(f"SOURCES = [\n\r{output}]")
        dbs = interface.database_classifier(databases)
        return dbs


if __name__ == '__main__':
    args(sys.argv[1:])