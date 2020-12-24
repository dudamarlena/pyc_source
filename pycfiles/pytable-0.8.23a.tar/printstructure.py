# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/tests/printstructure.py
# Compiled at: 2005-07-28 12:50:05
from pytable import dbspecifier, specifierfromoptions

def printTable(driver, connection, tableName):
    print repr(driver.tableStructure(connection, tableName=tableName))
    if hasattr(driver, 'listIndices'):
        for index in driver.listIndices(connection, tableName=tableName):
            print repr(index)


if __name__ == '__main__':
    spec = specifierfromoptions.specifierFromOptions()
    (driver, conn) = spec.connect()
    for table in driver.listTables(conn):
        printTable(driver, conn, table)

    for (namespace, table) in driver.listNamespaceTables(conn):
        printTable(driver, conn, '%s.%s' % (namespace, table))