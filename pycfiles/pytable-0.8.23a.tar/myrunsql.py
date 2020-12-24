# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/mysql/myrunsql.py
# Compiled at: 2003-08-02 18:46:25
from pytable import dbspecifier
import traceback
SQL = ['SHOW DATABASES;', 'SHOW TABLES;', 'SHOW INDEX FROM temp;', 'SHOW INDEX FROM temp2;', 'SHOW COLUMNS FROM temp;', 'SHOW COLUMNS FROM temp2;']
spec = dbspecifier.DBSpecifier(drivername='MySQL', user='mike', password='password', host='localhost', database='test')
(driver, connection) = spec.connect()
cursor = connection.cursor()
for item in SQL:
    try:
        cursor.execute(item)
        result = cursor.fetchall()
        if cursor.description and result:
            print item
            print ('|').join([ d[0] for d in cursor.description ])
            for line in result:
                print line

            print
    except:
        traceback.print_exc()