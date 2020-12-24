# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_dbapi.py
# Compiled at: 2013-11-20 07:32:15
from pymills.dbapi import Connection

def test_sqlite():
    db = Connection('sqlite', ':memory:')
    rows = db.do('CREATE TABLE foo (x, y)')
    assert list(rows) == []
    rows = db.do('INSERT INTO foo VALUES (?, ?)', 1, 2)
    assert list(rows) == []
    rows = db.do('INSERT INTO foo VALUES (?, ?)', 3, 4)
    assert list(rows) == []
    rows = db.do('SELECT x, y FROM foo')
    rows = list(rows)
    assert len(rows) == 2
    assert rows[0].keys() == ['x', 'y']
    assert rows[0].items() == [('x', 1), ('y', 2)]
    assert rows[0].values() == [1, 2]
    assert rows[1].x == 3
    assert rows[1].y == 4