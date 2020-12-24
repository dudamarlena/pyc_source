# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/mysql/get_database_table_column_names.py
# Compiled at: 2020-04-17 06:44:40
"""
*Given a database connection and a database table name, return the column names for the table*

:Author:
    David Young
"""
from builtins import str
import sys, os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from fundamentals.mysql import readquery

def get_database_table_column_names(dbConn, log, dbTable):
    """get database table column names

    **Key Arguments**

    - ``dbConn`` -- mysql database connection
    - ``log`` -- logger
    - ``dbTable`` -- database tablename
    

    **Return**

    - ``columnNames`` -- table column names
    

    **Usage**

    To get the column names of a table in a given database:

    ```python
    from fundamentals.mysql import get_database_table_column_names
    columnNames = get_database_table_column_names(
        dbConn=dbConn,
        log=log,
        dbTable="test_table"
    )
    ```
    
    """
    log.debug('starting the ``get_database_table_column_names`` function')
    sqlQuery = 'SELECT * FROM %s LIMIT 1' % (
     dbTable,)
    try:
        rows = readquery(log=log, sqlQuery=sqlQuery, dbConn=dbConn)
    except Exception as e:
        log.error('could not find column names for dbTable %s - failed with this error: %s ' % (
         dbTable, str(e)))
        return -1

    columnNames = list(rows[0].keys())
    log.debug('completed the ``get_database_table_column_names`` function')
    return columnNames