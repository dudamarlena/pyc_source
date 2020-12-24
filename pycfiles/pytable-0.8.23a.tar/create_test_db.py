# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/pypgsql/create_test_db.py
# Compiled at: 2003-08-02 18:46:25
from pytable import dbspecifier
import traceback
queries = [
 'DROP INDEX temp_first_second;', 'DROP TABLE temp2;', 'DROP TABLE temp;', 'CREATE TABLE temp (\n\t\tid int4 NOT NULL PRIMARY KEY,\n\t\tabc varchar(64),\n\t\tbcd decimal NOT NULL,\n\t\tcde float8 NOT NULL DEFAULT 0.999,\n\t\tefg int8\n\t);\n\t', 'CREATE TABLE temp2 (\n\t\tid int4 NOT NULL PRIMARY KEY,\n\t\ttemp_id int4 NOT NULL REFERENCES temp (id),\n\t\tname varchar(32) NOT NULL\n\t);\n\t', 'CREATE UNIQUE INDEX temp_first_second ON temp (abc, bcd);', "INSERT into temp values (1,'blah',23,.34, 55);", "INSERT into temp values (2,'hi there',25,4.34, 54);", "INSERT into temp2 values (1,1, 'blah');", "INSERT into temp2 values (2,2, 'blunder');"]
spec = dbspecifier.DBSpecifier(drivername='PyPgSQL', user='mike', password='pass', host='localhost', database='test')
(driver, connection) = spec.connect()
cursor = connection.cursor()
for SQL in queries:
    try:
        cursor.execute(SQL)
    except Exception:
        if SQL[:4] != 'DROP':
            traceback.print_exc()
            print SQL

connection.commit()