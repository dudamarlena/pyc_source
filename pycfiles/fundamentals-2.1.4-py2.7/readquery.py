# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/mysql/readquery.py
# Compiled at: 2020-04-17 06:44:40
"""
*Given a mysql query, read the data from the database and return the results as a list of dictionaries (database rows)*

:Author:
    David Young
"""
from builtins import str
import sys, os
os.environ['TERM'] = 'vt100'
from fundamentals import tools

def readquery(sqlQuery, dbConn, log, quiet=False):
    """Given a mysql query, read the data from the database and return the results as a list of dictionaries (database rows)

    **Key Arguments**

    - ``log`` -- the logger.
    - ``sqlQuery`` -- the MySQL command to execute
    - ``dbConn`` -- the db connection
    - ``quiet`` -- ignore mysql warnings and errors and move on. Be careful when setting this to true - damaging errors can easily be missed. Default *False*.
    

    **Return**

    - ``rows`` -- the rows returned by the sql query
    

    **Usage**

    ```python
    from fundamentals.mysql import readquery
    rows = readquery(
        log=log,
        sqlQuery=sqlQuery,
        dbConn=dbConn,
        quiet=False
    )
    ```
    
    """
    log.debug('starting the ``readquery`` function')
    import pymysql, warnings
    warnings.filterwarnings('error', category=pymysql.Warning)
    rows = []
    try:
        cursor = dbConn.cursor(pymysql.cursors.DictCursor)
    except Exception as e:
        log.error('could not create the database cursor: %s' % (e,))
        raise IOError('could not create the database cursor: %s' % (e,))

    try:
        cursor.execute(sqlQuery)
        rows = cursor.fetchall()
    except Exception as e:
        sqlQuery = sqlQuery[:1000]
        if quiet == False:
            log.warning('MySQL raised an error - read command not executed.\n' + str(e) + '\nHere is the sqlQuery\n\t%(sqlQuery)s' % locals())
            raise e
        else:
            log.warning('MySQL raised an error - read command not executed.\n' + str(e) + '\nHere is the sqlQuery\n\t%(sqlQuery)s' % locals())

    try:
        cursor.close()
    except Exception as e:
        log.warning('could not close the db cursor ' + str(e) + '\n')

    log.debug('completed the ``readquery`` function')
    return rows