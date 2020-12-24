# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/mysql/sqlite2mysql.py
# Compiled at: 2020-04-17 06:44:40
"""
Take a sqlite database file and copy the tables within it to a MySQL database

Usage:
    sqlite2mysql -s <pathToSettingsFile> <pathToSqliteDB> [<tablePrefix>]

Options:

    pathToSqliteDB        path to the sqlite database file
    tablePrefix           a string to prefix the table names when copying to mysql database
    pathToSettingsFile    path to a settings file with logging and database information (yaml file)

    -h, --help            show this help message
    -v, --version         show version
    -s, --settings        the settings file
"""
from builtins import object
import sys, os, sqlite3 as lite
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from fundamentals.mysql import writequery
from datetime import datetime, date, time

def main(arguments=None):
    """
    The main function used when ``yaml_to_database.py`` when installed as a cl tool
    """
    su = tools(arguments=arguments, docString=__doc__, logLevel='WARNING', options_first=False, projectName=False)
    arguments, settings, log, dbConn = su.setup()
    for arg, val in list(arguments.items()):
        if arg[0] == '-':
            varname = arg.replace('-', '') + 'Flag'
        else:
            varname = arg.replace('<', '').replace('>', '')
        if isinstance(val, str):
            exec varname + " = '%s'" % (val,)
        else:
            exec varname + ' = %s' % (val,)
        if arg == '--dbConn':
            dbConn = val
        log.debug('%s = %s' % (varname, val))

    from fundamentals.mysql import sqlite2mysql
    converter = sqlite2mysql(log=log, settings=settings, pathToSqlite=pathToSqliteDB, tablePrefix=tablePrefix, dbConn=dbConn)
    converter.convert_sqlite_to_mysql()


class sqlite2mysql(object):
    """
    *Take a sqlite database file and copy the tables within it to a MySQL database*

    **Key Arguments**

    - ``log`` -- logger
    - ``settings`` -- the settings dictionary
    - ``pathToSqlite`` -- path to the sqlite database to transfer into the MySQL database
    - ``tablePrefix`` -- a prefix to add to all the tablename when converting to mysql. Default *""*
    - ``dbConn`` -- mysql database connection 
    

    **Usage**

    To setup your logger, settings and database connections, please use the ``fundamentals`` package (`see tutorial here <http://fundamentals.readthedocs.io/en/latest/#tutorial>`_). 

    To convert and import the content of a sqlite database into MySQL run the following:

    .. todo::

        - add a tutorial about ``sqlite2mysql`` to documentation

    ```python
    from fundamentals.mysql import sqlite2mysql
    converter = sqlite2mysql(
        log=log,
        settings=settings,
        pathToSqlite="/path/to/sqlite.db",
        tablePrefix="external"
    )
    converter.convert_sqlite_to_mysql()
    ```
    
    """

    def __init__(self, log, pathToSqlite, tablePrefix='', settings=False, dbConn=False):
        self.log = log
        log.debug("instansiating a new 'sqlite2mysql' object")
        self.settings = settings
        self.pathToSqlite = pathToSqlite
        self.tablePrefix = tablePrefix
        self.dbConn = dbConn
        if not self.tablePrefix:
            self.tablePrefix = ''
        if len(self.tablePrefix):
            self.tablePrefix = self.tablePrefix + '_'
        return

    def convert_sqlite_to_mysql(self):
        """*copy the contents of the sqlite database into the mysql database*

        See class docstring for usage
        """
        from fundamentals.renderer import list_of_dictionaries
        from fundamentals.mysql import directory_script_runner
        self.log.debug('starting the ``convert_sqlite_to_mysql`` method')
        con = lite.connect(self.pathToSqlite)
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        createStatements = []
        inserts = []
        for table in tables:
            table = table['name']
            if table == 'sqlite_sequence':
                continue
            cur.execute("SELECT sql FROM sqlite_master WHERE name = '%(table)s';" % locals())
            createStatement = cur.fetchone()
            createStatement = createStatement[0].replace('"', '`') + ';'
            if 'DEFAULT' not in createStatement:
                if 'primary key(' in createStatement:
                    tmp = createStatement.split('primary key(')
                    tmp[0] = tmp[0].replace(',', ' varchar(150) DEFAULT NULL,')
                    createStatement = ('primary key(').join(tmp)
                if 'primary key,' in createStatement:
                    tmp = createStatement.split('primary key,')
                    tmp[1] = tmp[1].replace(',', ' varchar(150) DEFAULT NULL,')
                    tmp[1] = tmp[1].replace(');', ' varchar(150) DEFAULT NULL);')
                    createStatement = ('primary key,').join(tmp)
            createStatement = createStatement.replace('INTEGER PRIMARY KEY', 'INTEGER AUTO_INCREMENT PRIMARY KEY')
            createStatement = createStatement.replace('AUTOINCREMENT', 'AUTO_INCREMENT')
            createStatement = createStatement.replace("DEFAULT 't'", "DEFAULT '1'")
            createStatement = createStatement.replace("DEFAULT 'f'", "DEFAULT '0'")
            createStatement = createStatement.replace(",'t'", ",'1'")
            createStatement = createStatement.replace(",'f'", ",'0'")
            if 'CREATE TABLE `' in createStatement:
                createStatement = createStatement.replace('CREATE TABLE `', 'CREATE TABLE IF NOT EXISTS `' + self.tablePrefix)
            else:
                createStatement = createStatement.replace('CREATE TABLE ', 'CREATE TABLE IF NOT EXISTS ' + self.tablePrefix)
            if ', primary key(' in createStatement:
                createStatement = createStatement.replace(', primary key(', ",\n`dateCreated` datetime DEFAULT CURRENT_TIMESTAMP,\n`dateLastModified` datetime DEFAULT CURRENT_TIMESTAMP,\n`updated` tinyint(4) DEFAULT '0',\nprimary key(")
            else:
                createStatement = createStatement.replace(');', ",\n    `dateCreated` datetime DEFAULT CURRENT_TIMESTAMP,\n    `dateLastModified` datetime DEFAULT CURRENT_TIMESTAMP,\n    `updated` tinyint(4) DEFAULT '0');\n                ")
            createStatement = createStatement.replace(' text primary key', ' varchar(100) primary key')
            createStatement = createStatement.replace('`EntryText` TEXT NOT NULL,', '`EntryText` TEXT,')
            createStatement = createStatement.replace('`SelectionText` TEXT NOT NULL', '`SelectionText` TEXT')
            createStatement = createStatement.replace('`Filename` INTEGER NOT NULL,', '`Filename` TEXT NOT NULL,')
            createStatement = createStatement.replace('`SessionPartUUID` TEXT NOT NULL UNIQUE,', '`SessionPartUUID` VARCHAR(100) NOT NULL UNIQUE,')
            createStatement = createStatement.replace('`Name` TEXT PRIMARY KEY NOT NULL', '`Name` VARCHAR(100) PRIMARY KEY NOT NULL')
            createStatement = createStatement.replace(' VARCHAR ', ' VARCHAR(100) ')
            createStatement = createStatement.replace(' VARCHAR,', ' VARCHAR(100),')
            if len(createStatement.lower().split('datecreated')) > 2:
                createStatement = createStatement.replace('`dateCreated` datetime DEFAULT CURRENT_TIMESTAMP,\n', '')
            cur.execute("SELECT * from '%(table)s';" % locals())
            rows = cur.fetchall()
            allRows = []
            dateCreated = True
            for row in rows:
                thisDict = dict(row)
                if dateCreated and 'datecreated' in str(thisDict.keys()).lower():
                    dateCreated = False
                allRows.append(thisDict)

            if not os.path.exists('/tmp/headjack/'):
                os.makedirs('/tmp/headjack/')
            writequery(log=self.log, sqlQuery=createStatement, dbConn=self.dbConn)
            from fundamentals.mysql import insert_list_of_dictionaries_into_database_tables
            insert_list_of_dictionaries_into_database_tables(dbConn=self.dbConn, log=self.log, dictList=allRows, dbTableName=self.tablePrefix + table, uniqueKeyList=[], dateModified=True, dateCreated=dateCreated, batchSize=10000, replace=True, dbSettings=self.settings['database settings'])

        con.close()
        self.log.debug('completed the ``convert_sqlite_to_mysql`` method')
        return


if __name__ == '__main__':
    main()