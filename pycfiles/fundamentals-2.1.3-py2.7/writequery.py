# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/mysql/writequery.py
# Compiled at: 2020-04-17 06:44:40
"""
*Execute a MySQL write query on a database table*

:Author:
    David Young
"""
from builtins import str
import sys, os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
import time

def writequery(log, sqlQuery, dbConn, Force=False, manyValueList=False):
    """*Execute a MySQL write command given a sql query*

    **Key Arguments**

    - ``sqlQuery`` -- the MySQL command to execute
    - ``dbConn`` -- the db connection
    - ``Force`` -- do not exit code if error occurs, move onto the next command
    - ``manyValueList`` -- a list of value tuples if executing more than one insert
    

    **Return**

    - ``message`` -- error/warning message
    

    **Usage**

    Here's an example of how to create a table using the database connection passed to the function:

    ```python
    from fundamentals.mysql import writequery
    sqlQuery = "CREATE TABLE `testing_table` (`id` INT NOT NULL, PRIMARY KEY (`id`))"
    message = writequery(
        log=log,
        sqlQuery=sqlQuery,
        dbConn=dbConn,
        Force=False,
        manyValueList=False
    )
    ```

    Here's a many value insert example:

    ```python
    from fundamentals.mysql import writequery
    sqlQuery = "INSERT INTO testing_table (id) values (%s)"
    message = writequery(
        log=log,
        sqlQuery=sqlQuery,
        dbConn=dbConn,
        Force=False,
        manyValueList=[(1,), (2,), (3,), (4,), (5,), (6,), (7,),
                       (8,), (9,), (10,), (11,), (12,), ]
    )
    ```
    
    """
    log.debug('starting the ``writequery`` function')
    import pymysql, warnings
    warnings.filterwarnings('error', category=pymysql.Warning)
    message = ''
    try:
        cursor = dbConn.cursor(pymysql.cursors.DictCursor)
    except Exception as e:
        log.error('could not create the database cursor.')

    try:
        if manyValueList == False:
            cursor.execute(sqlQuery)
        else:
            batch = 100000
            offset = 0
            stop = 0
            while stop == 0:
                thisList = manyValueList[offset:offset + batch]
                offset += batch
                a = len(thisList)
                cursor.executemany(sqlQuery, thisList)
                dbConn.commit()
                if len(thisList) < batch:
                    stop = 1

    except pymysql.err.ProgrammingError as e:
        message = 'MySQL write command not executed for this query: << %s >>\nThe error was: %s \n' % (sqlQuery,
         str(e))
        if Force == False:
            log.error(message)
            raise
        else:
            log.warning(message)
    except pymysql.Error as e:
        try:
            e = e.args
        except:
            pass

        if e[0] == 1050 and 'already exists' in e[1]:
            log.info(str(e) + '\n')
        elif e[0] == 1062:
            log.debug('Duplicate Key error: %s\n' % (str(e),))
            message = 'duplicate key error'
        elif e[0] == 1061:
            log.debug('index already exists: %s\n' % (str(e),))
            message = 'index already exists'
        elif 'Duplicate entry' in str(e):
            log.debug('Duplicate Key error: %s\n' % (str(e),))
            message = 'duplicate key error'
        elif 'Deadlock' in str(e):
            i = 0
            while i < 10:
                time.sleep(1)
                i += 1
                try:
                    if manyValueList == False:
                        cursor.execute(sqlQuery)
                    else:
                        batch = 100000
                        offset = 0
                        stop = 0
                        while stop == 0:
                            thisList = manyValueList[offset:offset + batch]
                            offset += batch
                            a = len(thisList)
                            cursor.executemany(sqlQuery, thisList)
                            dbConn.commit()
                            if len(thisList) < batch:
                                stop = 1

                    i = 20
                except:
                    pass

            if i == 10:
                log.error('Deadlock: %s\n' % (str(e),))
                message = 'Deadlock error'
                raise
        else:
            message = 'MySQL write command not executed for this query: << %s >>\nThe error was: %s \n' % (sqlQuery,
             str(e))
            if Force == False:
                log.error(message)
                raise
            else:
                log.warning(message)
    except pymysql.Warning as e:
        log.info(str(e))
    except Exception as e:
        if 'truncated' in str(e):
            log.error('%s\n Here is the sqlquery:\n%s\n' % (str(e), sqlQuery))
            if manyValueList:
                log.error('... and the values:\n%s\n' % (thisList,))
        elif 'Duplicate entry' in str(e):
            log.warning('Duplicate Key error: %s\n' % (str(e),))
            message = 'duplicate key error'
        else:
            log.error('MySQL write command not executed for this query: << %s >>\nThe error was: %s \n' % (
             sqlQuery, str(e)))
            if Force == False:
                sys.exit(0)
            cursor.close()
            return -1

    dbConn.commit()
    cOpen = True
    count = 0
    while cOpen:
        try:
            cursor.close()
            cOpen = False
        except Exception as e:
            time.sleep(1)
            count += 1
            if count == 10:
                log.warning('could not close the db cursor ' + str(e) + '\n')
                raise e
                count = 0

    log.debug('completed the ``writequery`` function')
    return message