# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/mysql/table_exists.py
# Compiled at: 2020-04-17 06:44:40
"""
*Probe a database to determine if a given table exists*

:Author:
    David Young
"""
import sys, os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from fundamentals.mysql import readquery

def table_exists(dbConn, log, dbTableName):
    """*Probe a database to determine if a given table exists*

    **Key Arguments**

    - ``dbConn`` -- mysql database connection
    - ``log`` -- logger
    - ``dbTableName`` -- the database tablename
    

    **Return**

    - ``tableExists`` -- True or False
    

    **Usage**

    To test if a table exists in a database:

    ```python
    from fundamentals.mysql import table_exists
    exists = table_exists(
        dbConn=dbConn,
        log=log,
        dbTableName="stupid_named_table"
    )

    print exists

    # OUTPUT: False
    ```
    
    """
    log.debug('starting the ``table_exists`` function')
    sqlQuery = "\n        SELECT count(*)\n        FROM information_schema.tables\n        WHERE table_name = '%(dbTableName)s'\n    " % locals()
    tableExists = readquery(log=log, sqlQuery=sqlQuery, dbConn=dbConn, quiet=False)
    if tableExists[0]['count(*)'] == 0:
        tableExists = False
    else:
        tableExists = True
    log.debug('completed the ``table_exists`` function')
    return tableExists