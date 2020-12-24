# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asfpy/sqlite.py
# Compiled at: 2020-04-17 15:43:08
# Size of source mod 2**32: 8417 bytes
"""SQLite document-store wrapper for ASF."""
import sqlite3

class asfpyDBError(Exception):
    pass


class db:

    def __init__(self, fp):
        self.connector = sqlite3.connect(fp)
        self.connector.row_factory = sqlite3.Row
        self.cursor = self.connector.cursor()
        self.upserts_supported = sqlite3.sqlite_version >= '3.25.0'

    def run(self, cmd, *args):
        self.cursor.execute(cmd, args)

    def runc(self, cmd, *args):
        self.cursor.execute(cmd, args)
        self.connector.commit()

    def delete(self, table, **target):
        """Delete a row where ..."""
        if not target:
            raise asfpyDBError('DELETE must have at least one defined target value for locating where to delete from')
        k, v = next(iter(target.items()))
        statement = f"DELETE FROM {table} WHERE {k} = ?;"
        self.runc(statement, v)

    def update(self, table, document, **target):
        """Update a row where ..."""
        if not target:
            raise asfpyDBError('UPDATE must have at one defined target to specify the row to update')
        k, v = next(iter(target.items()))
        items = document.items()
        columns = ', '.join(('%s = ?' % uk for uk, uv in items))
        statement = f"UPDATE {table} SET {columns} WHERE {k} = ?;"
        values = [uv for uk, uv in items]
        values.append(v)
        (self.runc)(statement, *values)

    def insert(self, table, document):
        """Standard insert, document -> sql."""
        items = document.items()
        columns = ', '.join((uk for uk, uv in items))
        questionmarks = ', '.join(['?'] * len(items))
        statement = f"INSERT INTO {table} ({columns}) VALUES ({questionmarks});"
        values = [uv for uk, uv in items]
        (self.runc)(statement, *values)

    def upsert(self, table, document, **target):
        """Performs an upsert in a table with unique constraints. Insert if not present, update otherwise."""
        if not target:
            raise asfpyDBError('UPSERTs must have at least one defined target value for locating where to upsert')
        else:
            k, v = next(iter(target.items()))
            document[k] = v
            if self.upserts_supported:
                items = document.items()
                variables = ', '.join((uk for uk, uv in items))
                questionmarks = ', '.join(['?'] * len(items))
                upserts = ', '.join(('%s = ?' % uk for uk, uv in items))
                statement = f"INSERT INTO {table} ({variables}) VALUES ({questionmarks}) ON CONFLICT({k}) DO UPDATE SET {upserts} WHERE {k} = ?;"
                values = [uv for uk, uv in items] * 2 + [v]
                (self.runc)(statement, *values)
            else:
                try:
                    self.insert(table, document)
                except sqlite3.IntegrityError:
                    (self.update)(table, document, **target)

    def fetch(self, table, limit=1, **params):
        """Searches a table for matching params, returns up to $limit items that match, as dicts."""
        if params:
            items = params.items()
            search = ' AND '.join(('%s = ?' % uk for uk, uv in items))
            values = [uv for uk, uv in items]
        else:
            search = '1'
            values = ()
        statement = f"SELECT * FROM {table} WHERE {search}"
        if limit:
            statement += f" LIMIT {limit}"
            rows_left = limit
        self.cursor.execute(statement, values)
        saw_row = False
        while True:
            rowset = self.cursor.fetchmany()
            if not rowset:
                if not saw_row:
                    yield
                return
            for row in rowset:
                yield dict(row)
            else:
                if limit:
                    rows_left -= len(rowset)
                    assert rows_left >= 0
                    if rows_left == 0:
                        return
                saw_row = True

    def fetchone(self, table_name, **params):
        return next((self.fetch)(table_name, **params))

    def table_exists(self, table):
        """Simple check to see if a table exists or not."""
        return self.fetchone('sqlite_master', type='table', name=table) and True or False


def test(dbname=':memory:'):
    testdb = db(dbname)
    cstatement = 'CREATE TABLE test (\n                      foo   varchar unique,\n                      bar   varchar,\n                      baz   real\n                      )'
    try:
        testdb.runc(cstatement)
    except sqlite3.OperationalError as e:
        try:
            assert str(e) == 'table test already exists'
        finally:
            e = None
            del e

    try:
        testdb.insert('test', {'foo':'foo1234',  'bar':'blorgh',  'baz':5})
    except sqlite3.IntegrityError as e:
        try:
            assert str(e) == 'UNIQUE constraint failed: test.foo'
        finally:
            e = None
            del e

    else:
        try:
            testdb.insert('test', {'foo':'foo1234',  'bar':'blorgh',  'baz':2})
        except sqlite3.IntegrityError as e:
            try:
                assert str(e) == 'UNIQUE constraint failed: test.foo'
            finally:
                e = None
                del e

        else:
            testdb.upsert('test', {'foo':'foo1234',  'bar':'blorgssh',  'baz':8}, foo='foo1234')
    try:
        testdb.upsert('test', {'foo':'foo1234',  'bar':'blorgssh',  'baz':8})
    except asfpyDBError as e:
        try:
            assert str(e) == 'UPSERTs must have at least one defined target value for locating where to upsert'
        finally:
            e = None
            del e

    else:
        testdb.update('test', {'foo': 'foo4321'}, foo='foo1234')
        obj = testdb.fetchone('test', foo='foo4321')
        if not (type(obj) is dict and obj.get('foo') == 'foo4321'):
            raise AssertionError
        obj = testdb.fetch('test', limit=5, foo='foo4321')
        assert str(type(obj)) == "<class 'generator'>"
        assert next(obj).get('foo') == 'foo4321'
        obj = testdb.fetchone('test', foo='foo9999')
        assert obj is None
        testdb.delete('test', foo='foo4321')
        assert testdb.table_exists('test')
        assert not testdb.table_exists('test2')
    for i in range(1000):
        testdb.insert('test', {'foo':str(i),  'bar':str(i),  'baz':i})
    else:
        count = 0
        for row in testdb.fetch('test', limit=None):
            assert int(row['foo']) == count
            count += 1
        else:
            assert count == 1000
            testdb.cursor.arraysize = 97
            count = 0
            for row in testdb.fetch('test', limit=None):
                assert int(row['foo']) == count
                count += 1
            else:
                assert count == 1000
                count = 0
                for row in testdb.fetch('test', limit=30):
                    assert int(row['foo']) == count
                    count += 1
                else:
                    assert count == 30


if __name__ == '__main__':
    test()