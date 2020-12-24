# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/files/list_of_dictionaries_to_mysql_inserts.py
# Compiled at: 2020-04-17 06:44:40
"""
*Convert a python list of dictionaries to pretty csv output*

:Author:
    David Young
"""
import sys, os, io, csv
from decimal import Decimal
from datetime import datetime
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from fundamentals.mysql import convert_dictionary_to_mysql_table

def list_of_dictionaries_to_mysql_inserts(log, datalist, tableName):
    """Convert a python list of dictionaries to pretty csv output

    **Key Arguments**

    - ``log`` -- logger
    - ``datalist`` -- a list of dictionaries
    - ``tableName`` -- the name of the table to create the insert statements for
    

    **Return**

    - ``output`` -- the mysql insert statements (as a string)
    

    **Usage**

    ```python
    from fundamentals.files import list_of_dictionaries_to_mysql_inserts
    mysqlInserts = list_of_dictionaries_to_mysql_inserts(
        log=log,
        datalist=dataList,
        tableName="my_new_table"
    )
    print mysqlInserts
    ```

    this output the following:

    ```plain
    INSERT INTO `testing_table` (a_newKey,and_another,dateCreated,uniqueKey2,uniquekey1) VALUES ("cool" ,"super cool" ,"2016-09-14T13:17:26" ,"burgers" ,"cheese")  ON DUPLICATE KEY UPDATE  a_newKey="cool", and_another="super cool", dateCreated="2016-09-14T13:17:26", uniqueKey2="burgers", uniquekey1="cheese" ;
    ...
    ...
    ```
    
    """
    log.debug('starting the ``list_of_dictionaries_to_mysql_inserts`` function')
    if not len(datalist):
        return 'NO MATCH'
    inserts = []
    for d in datalist:
        insertCommand = convert_dictionary_to_mysql_table(log=log, dictionary=d, dbTableName='testing_table', uniqueKeyList=[], dateModified=False, returnInsertOnly=True, replace=True, batchInserts=False)
        inserts.append(insertCommand)

    output = (';\n').join(inserts) + ';'
    log.debug('completed the ``list_of_dictionaries_to_mysql_inserts`` function')
    return output