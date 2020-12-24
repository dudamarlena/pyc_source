# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/mysql.py
# Compiled at: 2013-09-06 06:39:01
""" **mysql**

**A handful of useful mysql python methods**

| Created by David Young on October 8, 2012
| If you have any questions requiring this script please email me: d.r.young@qub.ac.uk

**dryx syntax**
 | ``xxx`` = come back here and do some more work
 | ``_someObject`` = a 'private' object that should only be changed for debugging

**notes**:
 - Dave started work on this file on October 8, 2012
 - This is a growing repository for Dave's custom MySQL classes and functions """
import sys, os

def set_db_connection(pathToYamlFile):
    """Get a database connection using settings in yaml file. Given the location of a YAML dictionary containing database credientials,
    this function will setup and return the connection

    ****Key Arguments:****
        - ``pathToYamlFile`` -- path to the YAML dictionary.

    Returns:
        - ``dbConn`` -- connection to the MySQL database """
    import logging, yaml, MySQLdb as ms, sys
    try:
        logging.info('importing the yaml database connection dictionary from ' + pathToYamlFile)
        stream = file(pathToYamlFile, 'r')
        connDict = yaml.load(stream)
    except:
        logging.critical('could not load the connect dictionary from ' + pathToYamlFile)
        sys.exit(1)

    try:
        logging.info('connecting to the ' + connDict['db'] + ' database on ' + connDict['host'])
        dbConn = ms.connect(host=connDict['host'], user=connDict['user'], passwd=connDict['password'], db=connDict['db'])
    except Exception as e:
        logging.critical('could not connect to the ' + connDict['db'] + ' database on ' + connDict['host'] + ' : ' + str(e) + '\n')

    return dbConn


def execute_mysql_write_query(sqlQuery, dbConn, log):
    """ Execute a MySQL write command given a sql query

            ****Key Arguments:****
                - ``sqlQuery`` -- the MySQL command to execute
                - ``dbConn`` -- the db connection

            **Return:**
                - ``None`` """
    import MySQLdb
    log.info('starting execute_mysql_write_query')
    try:
        cursor = dbConn.cursor(MySQLdb.cursors.DictCursor)
    except Exception as e:
        log.error('could not create the database cursor.')

    try:
        cursor.execute(sqlQuery)
    except MySQLdb.Error as e:
        if e[0] == 1050 and 'already exists' in e[1]:
            log.info(str(e) + '\n')
        elif e[0] == 1062:
            log.debug('Duplicate Key error: %s' % (str(e),))
        else:
            log.error('MySQL write command not executed for this query: << %s >>\nThe error was: %s ' % (sqlQuery,
             str(e)))
    except Exception as e:
        log.error('MySQL write command not executed for this query: << %s >>\nThe error was: %s ' % (sqlQuery, str(e)))

    try:
        cursor.close()
    except Exception as e:
        log.warning('could not close the db cursor ' + str(e) + '\n')

    log.info('finished execute_mysql_write_query')
    return


def execute_mysql_read_query(sqlQuery, dbConn, log):
    """ Execute a MySQL select command given a query

            ****Key Arguments:****
             - ``sqlQuery`` -- the MySQL command to execute
             - ``dbConn`` -- the db connection

            **Return:**
             - ``rows`` -- the rows returned by the sql query """
    import MySQLdb
    try:
        cursor = dbConn.cursor(MySQLdb.cursors.DictCursor)
    except Exception as e:
        log.error('could not create the database cursor: %s' % (e,))

    try:
        cursor.execute(sqlQuery)
        rows = cursor.fetchall()
    except Exception as e:
        log.error('MySQL raised an error - write command not executed.\n' + str(e) + '\n')
        raise e

    try:
        cursor.close()
    except Exception as e:
        log.warning('could not close the db cursor ' + str(e) + '\n')

    return rows


def convert_dictionary_to_mysql_table(dbConn, log, dictionary, dbTableName, uniqueKeyList=[], createHelperTables=False):
    """ Convert a python dictionary into a mysql table

    **Key Arguments:**
        - ``log`` -- logger
        - ``dictionary`` -- python dictionary
        - ``dbConn`` -- the db connection
        - ``dbTableName`` -- name of the table you wish to add the data to (or create if it does not exist)
        - ``uniqueKeyList`` - a lists column names that need combined to create the primary key
        - ``createHelperTables`` -- create some helper tables with the main table, detailing original keywords etc

    **Return:**
        - ``None`` """
    import MySQLdb as mdb, re, yaml, time
    from dryxPython import commonutils as dcu
    import collections as c
    log.info('starting convert_dictionary_to_mysql_table')
    if str(type(dbConn).__name__) != 'Connection':
        message = 'Please use a valid MySQL DB connection.'
        log.critical(message)
        raise TypeError(message)
    if not isinstance(dictionary, dict):
        message = 'Please make sure "dictionary" argument is a dict type.'
        log.critical(message)
        raise TypeError(message)
    if not isinstance(uniqueKeyList, list):
        message = 'Please make sure "uniqueKeyList" is a list'
        log.critical(message)
        raise TypeError(message)
    for i in uniqueKeyList:
        if i not in dictionary.keys():
            message = 'Please make sure values in "uniqueKeyList" are present in the "dictionary" you are tring to convert'
            log.critical(message)
            raise ValueError(message)

    for k, v in dictionary.iteritems():
        if isinstance(v, list) and len(v) != 2:
            message = 'Please make sure the list values in "dictionary" 2 items in length'
            log.critical('%s: in %s we have a %s (%s)' % (message, k, v, type(v)))
            raise ValueError(message)
        if not (isinstance(v[0], str) or isinstance(v[0], int) or isinstance(v[0], bool) or isinstance(v[0], float) or v[0] == None):
            message = 'Please make sure values in "dictionary" are of an appropriate value to add to the database, must be str, float, int or bool'
            log.critical('%s: in %s we have a %s (%s)' % (message, k, v, type(v)))
            raise ValueError(message)

    if not isinstance(createHelperTables, bool):
        message = 'Please make sure "createHelperTables" is a True or False'
        log.critical(message)
        raise TypeError(message)
    qCreateColumnPreamble = "IF NOT EXISTS( (SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=DATABASE() AND COLUMN_NAME='my_additional_column' AND TABLE_NAME='my_table_name') ) THEN"
    qCreateColumnPostamble = 'PRIMARY KEY (`primaryId`)) ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;'
    qCreateTableCommandList = []
    qCreateTableCommandList.extend([
     'CREATE TABLE IF NOT EXISTS `' + dbTableName + "`\n                                            (`primaryId` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'An internal counter',\n                                            PRIMARY KEY (`primaryId`))\n                                            ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=latin1"])
    reFeedParserClass = re.compile('FeedParserDict')
    reDatetime = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}T')
    reTypeTime = re.compile('struct_time')
    qCreateColumn = ''
    formattedKey = ''
    formattedKeyList = []
    myValues = []
    try:
        for command in qCreateTableCommandList:
            execute_mysql_write_query(command, dbConn, log)

    except MySQLdb.Error as e:
        if e[0] == 1050 and 'already exists' in e[1]:
            pass
        else:
            log.critial('could not create the table ' + dbTableName + ' ' + str(e) + '\n')
            sys.exit(e)
    except Exception as e:
        log.critical('could not create the table ' + dbTableName + ' ' + str(e) + '\n')
        sys.exit(e)

    dictionary['dateCreated'] = [str(dcu.get_now_sql_datetime()), 'date row was created']
    dictionary['dateLastModified'] = [str(dcu.get_now_sql_datetime()), 'date row was modified']
    dictionary['dateLastRead'] = [str(dcu.get_now_sql_datetime()), 'date row was last read']
    count = len(dictionary)
    i = 1
    for key, value in dictionary.items():
        if value[0] is None:
            del dictionary[key]

    odictionary = c.OrderedDict(sorted(dictionary.items()))
    for key, value in odictionary.iteritems():
        formattedKey = key.replace(' ', '_').replace('-', '_')
        if formattedKey == 'dec':
            formattedKey = 'decl'
        if formattedKey == 'DEC':
            formattedKey = 'DECL'
        formattedKeyList.extend([formattedKey])
        if len(key) > 0:
            if type(value[0]) == list or reFeedParserClass.search(str(type(value[0]))):
                value[0] = yaml.dump(value[0])
                value[0] = str(value[0])
            if type(value[0]) == unicode:
                myValues.extend(['%s' % value[0].strip()])
            else:
                myValues.extend(['%s' % (value[0],)])
            colExists = "SELECT *                                FROM information_schema.COLUMNS                                WHERE TABLE_SCHEMA=DATABASE()                                    AND COLUMN_NAME='" + formattedKey + "'                                    AND TABLE_NAME='" + dbTableName + "'"
            try:
                rows = execute_mysql_read_query(colExists, dbConn, log)
            except Exception as e:
                log.error('something went wrong' + str(e) + '\n')

            if len(rows) == 0:
                qCreateColumn = 'ALTER TABLE %s ADD %s' % (dbTableName, formattedKey)
                if reDatetime.search(str(value[0])):
                    qCreateColumn += ' datetime DEFAULT NULL'
                elif formattedKey == 'updated_parsed' or formattedKey == 'published_parsed' or formattedKey == 'feedName' or formattedKey == 'title':
                    qCreateColumn += ' varchar(100) DEFAULT NULL'
                elif (type(value[0]) == str or type(value[0]) == unicode) and len(value[0]) < 30:
                    qCreateColumn += ' varchar(100) DEFAULT NULL'
                elif (type(value[0]) == str or type(value[0]) == unicode) and len(value[0]) >= 30 and len(value[0]) < 80:
                    qCreateColumn += ' varchar(100) DEFAULT NULL'
                elif type(value[0]) == str or type(value[0]) == unicode:
                    columnLength = 450 + len(value[0]) * 2
                    qCreateColumn += ' varchar(' + str(columnLength) + ') DEFAULT NULL'
                elif type(value[0]) == int and abs(value[0]) <= 9:
                    qCreateColumn += ' tinyint DEFAULT NULL'
                elif type(value[0]) == int:
                    qCreateColumn += ' int DEFAULT NULL'
                elif type(value[0]) == float or type(value[0]) == long:
                    qCreateColumn += ' double DEFAULT NULL'
                elif type(value[0]) == bool:
                    qCreateColumn += ' tinyint DEFAULT NULL'
                elif type(value[0]) == list:
                    qCreateColumn += ' varchar(1024) DEFAULT NULL'
                else:
                    log.debug('Do not know what format to add this key in MySQL - removing from dictionary: %s, %s' % (
                     key, type(value[0])))
                    formattedKeyList.pop()
                    myValues.pop()
                    qCreateColumn = None
                if qCreateColumn:
                    if key is not formattedKey:
                        qCreateColumn += " COMMENT 'original keyword: " + key + "'"
                    try:
                        log.info('creating the ' + formattedKey + ' column in the ' + dbTableName + ' table')
                        execute_mysql_write_query(qCreateColumn, dbConn, log)
                    except Exception as e:
                        log.debug('qCreateColumn: %s' % (qCreateColumn,))
                        log.error('could not create the ' + formattedKey + ' column in the ' + dbTableName + ' table -- ' + str(e) + '\n')

    if len(uniqueKeyList):
        for i in range(len(uniqueKeyList)):
            uniqueKeyList[i] = uniqueKeyList[i].replace(' ', '_').replace('-', '_')
            if uniqueKeyList[i] == 'dec':
                uniqueKeyList[i] = 'decl'
            if uniqueKeyList[i] == 'DEC':
                uniqueKeyList[i] = 'DECL'

        indexName = uniqueKeyList[0].replace(' ', '_').replace('-', '_')
        for i in range(len(uniqueKeyList) - 1):
            indexName += '_' + uniqueKeyList[(i + 1)]

        indexName = dcu.make_lowercase_nospace(indexName)
        rows = execute_mysql_read_query("SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS WHERE TABLE_SCHEMA = DATABASE() AND\n                                    TABLE_NAME = '" + dbTableName + "' AND INDEX_NAME = '" + indexName + "'", dbConn, log)
        exists = rows[0]['COUNT(*)']
        log.debug('uniqueKeyList: %s' % (uniqueKeyList,))
        if exists == 0:
            if type(uniqueKeyList) is list:
                uniqueKeyList = (',').join(uniqueKeyList)
            addUniqueKey = 'ALTER TABLE ' + dbTableName + ' ADD unique ' + indexName + ' (' + uniqueKeyList + ')'
            execute_mysql_write_query(addUniqueKey, dbConn, log)
    myKeys = (',').join(formattedKeyList)
    myValues = ('" ,"').join(myValues)
    myValues = myValues.replace('time.struct_time', '')
    myValues = myValues.replace('- !!python/object/new:feedparser.FeedParserDict', '')
    myValues = myValues.replace('!!python/object/new:feedparser.FeedParserDict', '')
    myValues = myValues.replace('dictitems:', '')
    myValues = myValues.replace('dictitems', '')
    myValues = myValues.replace('!!python/unicode:', '')
    myValues = myValues.replace('!!python/unicode', '')
    addValue = 'INSERT INTO ' + dbTableName + ' (' + myKeys + ') VALUES ("' + myValues + '")'
    try:
        execute_mysql_write_query(addValue, dbConn, log)
    except Exception as e:
        log.error("could not add new data added to the table '" + dbTableName + "' : " + str(e) + '\n')

    log.info('finished convert_dictionary_to_mysql_table')
    return


def set_flag(dbConn, log, tableName, flagColumn, flagValue, primaryKeyColumn, primaryKeyId):
    """ Set a flag in a db table to a given value

            ****Key Arguments:****
                - ``dbConn`` -- db connection
                - ``tableName`` -- db table name
                - ``flagColumn`` -- flag column name
                - ``flagValue`` -- value flag is to be set to
                - ``primaryKeyColumn`` -- primaryKey column name
                - ``primaryKeyId`` -- single id of the row you wish to set the flag for

            **Return:**
                - ``None`` """
    import dryxPython.mysql as m
    sqlQuery = 'update ' + tableName + ' set ' + flagColumn + ' = ' + str(flagValue) + ' where ' + primaryKeyColumn + ' = ' + str(primaryKeyId)
    try:
        log.debug('update the ingested flags for ' + tableName)
        m.execute_mysql_write_query(sqlQuery, dbConn, log)
    except Exception as e:
        log.error('cound not update the ingested flags for %s, error: %s' % (tableName, str(e)))
        return -1

    return


def add_column_to_db_table(tableName, colName, colType, dbConn):
    """ Add a column of agiven name to a database table

            ****Key Arguments:****
                - ``tableName`` -- name of table to add column to
                - ``dbConn`` -- database hosting the above table
                - ``colName`` -- name of the column to add
                - ``colType`` -- type of the column to be added
                - ``default`` -- the default value of the column to be added

            **Return:**
                - ``None`` """
    colsToAdd = {colName: colType}
    for key in colsToAdd.keys():
        colExists = "SELECT *                                FROM information_schema.COLUMNS                                WHERE TABLE_SCHEMA=DATABASE()                                    AND COLUMN_NAME='" + key + "'                                    AND TABLE_NAME='" + tableName + "'"
        colExists = execute_mysql_read_query(colExists, dbConn, log)
        if not colExists:
            sqlQuery = 'ALTER TABLE ' + tableName + ' ADD ' + key + ' ' + colsToAdd[key] + ' DEFAULT NULL'
            (sqlQuery, dbConn, log)

    return


def add_HTMIds_to_mysql_tables(raColName, declColName, tableName, dbConn, log, primaryIdColumnName='primaryId'):
    """ Calculate and append HTMId info to a mysql db table containing ra and dec columns

    ****Key Arguments:****
        - ``raColName`` -- ra in sexegesimal
        - ``declColName`` -- dec in sexegesimal
        - ``tableName`` -- name of table to add htmid info to
        - ``dbConn`` -- database hosting the above table
        - ``log`` -- logger

    **Return:**
        - ``None`` """
    import MySQLdb as ms, dryxPython.mysql as m
    from dryxPython.kws import utils as u
    sqlQuery = 'show tables'
    rows = execute_mysql_read_query(sqlQuery=sqlQuery, dbConn=dbConn, log=log)
    tableList = []
    for row in rows:
        tableList.extend(row.values())

    if tableName not in tableList:
        message = 'The %s table does not exist in the database' % (tableName,)
        log.critical(message)
        raise IOError(message)
    cursor = dbConn.cursor(ms.cursors.DictCursor)
    sqlQuery = 'SELECT * FROM %s LIMIT 1' % (tableName,)
    cursor.execute(sqlQuery)
    rows = cursor.fetchall()
    desc = cursor.description
    existingColumns = []
    for i in range(len(desc)):
        existingColumns.append(desc[i][0])

    if raColName not in existingColumns or declColName not in existingColumns:
        message = 'Please make sure you have got the naes of the RA and DEC columns correct'
        log.critical(message)
        raise IOError(message)
    htmCols = {'htm16ID': 'BIGINT(20)', 
       'htm20ID': 'BIGINT(20)', 
       'cx': 'DOUBLE', 
       'cy': 'DOUBLE', 
       'cz': 'DOUBLE'}
    for key in htmCols.keys():
        try:
            log.debug('attempting to check and generate the HTMId columns for the %s db table' % (tableName,))
            colExists = "SELECT *\n                    FROM information_schema.COLUMNS\n                    WHERE TABLE_SCHEMA=DATABASE()\n                    AND COLUMN_NAME='%s'\n                    AND TABLE_NAME='%s'" % (
             key, tableName)
            colExists = m.execute_mysql_read_query(colExists, dbConn, log)
            if not colExists:
                sqlQuery = 'ALTER TABLE ' + tableName + ' ADD ' + key + ' ' + htmCols[key] + ' DEFAULT NULL'
                m.execute_mysql_write_query(sqlQuery, dbConn, log)
        except Exception as e:
            log.critical('could not check and generate the HTMId columns for the %s db table - failed with this error: %s ' % (
             tableName, str(e)))
            return -1

    sqlQuery = 'SELECT %s, %s, %s from %s where htm16ID is NULL' % (primaryIdColumnName, raColName, declColName, tableName)
    rows = m.execute_mysql_read_query(sqlQuery, dbConn, log)
    for row in rows:
        if row[raColName] is None or row[declColName] is None:
            continue
        else:
            thisRa, thisDec = float(row[raColName]), float(row[declColName])
            htm16ID = u.htmID(thisRa, thisDec, 16)
            htm20ID = u.htmID(thisRa, thisDec, 20)
            cx, cy, cz = u.calculate_cartesians(thisRa, thisDec)
            sqlQuery = "UPDATE %s SET htm16ID=%s, htm20ID=%s,cx=%s,cy=%s,cz=%s\n                                                    where %s = '%s'" % (
             tableName,
             htm16ID,
             htm20ID,
             cx,
             cy,
             cz,
             primaryIdColumnName,
             row[primaryIdColumnName])
            try:
                log.debug('attempting to update the HTMIds for new objects in the %s db table' % (tableName,))
                m.execute_mysql_write_query(sqlQuery, dbConn, log)
            except Exception as e:
                log.critical('could not update the HTMIds for new objects in the %s db table - failed with this error: %s ' % (
                 tableName, str(e)))
                return -1

    return


def get_db_table_column_names(dbConn, log, dbTable):
    """get database table column names

    ****Key Arguments:****
        - ``dbConn`` -- mysql database connection
        - ``log`` -- logger
        - ``dbTable`` -- database tablename

    **Return:**
        - ``columnNames`` -- table column names """
    sqlQuery = 'SELECT *\n                                FROM %s\n                                LIMIT 1' % (
     dbTable,)
    try:
        log.debug('attempting to find column names for dbTable %s' % (dbTable,))
        rows = execute_mysql_read_query(sqlQuery, dbConn, log)
    except Exception as e:
        log.error('could not find column names for dbTable %s - failed with this error: %s ' % (dbTable, str(e)))
        return -1

    columnNames = rows[0].keys()
    return columnNames


if __name__ == '__main__':
    main()