# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/CommonFileAPI/SQLiteAPI.py
# Compiled at: 2014-04-11 11:37:47
import sqlite3

def connect_to_database(database_name):
    con = sqlite3.connect(database_name + '.db')
    return con.cursor()


def execute_sql(database, sql):
    assert isinstance(database, sqlite3.Cursor)
    database.execute(sql)
    data = database.fetchall()
    return data