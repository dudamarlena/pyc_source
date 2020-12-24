# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/pypgsql/pgrunsql.py
# Compiled at: 2003-08-02 18:46:25
from pytable import dbspecifier
SQL = "SELECT \n\tcon.conkey, -- local key-columns\n\tcon.confrelid, -- remote table id\n\tc2.relname, -- remote table name\n\tcon.confkey -- remote key-columns\n\t\nFROM\n\tpg_constraint con,\n\tpg_class c,\n\tpg_class c2\nWHERE\n\tc.relname='temp2' AND\n\tc.oid = con.conrelid AND\n\tcon.contype = 'f' AND\n\tc2.oid = con.confrelid\n;\n"
spec = dbspecifier.DBSpecifier(drivername='PyPgSQL', user='mike', password='pass', host='localhost', database='test')
(driver, connection) = spec.connect()
cursor = connection.cursor()
cursor.execute(SQL)
print cursor.fetchall()