# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/gorgou/sql/sqlite3.py
# Compiled at: 2018-02-02 23:22:40
# Size of source mod 2**32: 1031 bytes
import sqlite3

def exe(db, sql, par=()):
    """CREATE TABLE COMPANY
           (ID INT PRIMARY KEY     NOT NULL,
           NAME           TEXT    NOT NULL,
           AGE            INT     NOT NULL,
           ADDRESS        CHAR(50),
           SALARY         REAL);"""
    conn = sqlite3.connect(db)
    conn.execute(sql, par)
    conn.close()


def read(db, sql, par=()):
    conn = sqlite3.connect(db)
    cur = conn.execute(sql, par)
    conn.close()
    return cur