# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hashdb/hashdb_db.py
# Compiled at: 2011-01-06 01:19:27
from hashdb_output import log
import sqlite3 as sql
from hashdb_config_base import CombineDB
from collections import namedtuple
import os

def count_components(path):
    """Returns the number of components in the given path"""
    return path.count('/')


class HashDatabase(object):

    def __init__(self, filename):
        object.__init__(self)
        self._filename = filename
        self._combines = []
        self._mark = None
        self._conn = None
        return

    def add_combine(self, combine):
        self._combines.append(combine)

    def add_combines(self, combines):
        self._combines.extend(combines)

    @property
    def connection(self):
        return self._conn

    def open(self):
        try:
            conn = sql.connect(self._filename)
            conn.row_factory = sql.Row
            conn.text_factory = str
            conn.create_function('count_components', 1, count_components)
            self._create_schema(conn)
        except OSError, ex:
            log.error('error: Unable to open primary database (%s): %s' % (self._filename, ex))
            return False
        except sql.Error, ex:
            log.error('error: Unable to open primary database (%s): %s' % (self._filename, ex))
            return False
        else:
            for (i, combine) in enumerate(self._combines):
                try:
                    alias = self._dbalias(i)
                    with conn:
                        conn.execute('ATTACH ? as %s' % alias, (
                         combine.database,))
                except OSError, ex:
                    log.error('error: Unable to open secondary database (%s): %s' % (combine.database, ex))
                    return False
                except sql.Error, ex:
                    log.error('error: Unable to open secondary database (%s): %s' % (combine.database, ex))
                    return False

            try:
                self._create_combined(conn)
            except sql.Error, ex:
                log.error('error: Unable to create combined database view: %s' % ex)
                return False

            try:
                self._create_working(conn)
            except sql.Error, ex:
                log.error('error: Unable to create working tables: %s' % ex)
                return False

        self._conn = conn
        return True

    def _create_basic_schema(self, conn, name, temporary=False):
        primary = 'NOT NULL' if temporary else 'PRIMARY KEY ASC'
        temporary = 'TEMPORARY' if temporary else ''
        with conn:
            conn.executescript('\n                CREATE %(temporary)s TABLE IF NOT EXISTS %(name)s (\n                    path TEXT %(primary)s,\n                    hash TEXT NOT NULL,\n                    size LONG NOT NULL,\n                    time LONG NOT NULL,\n                    mark LONG NOT NULL\n                );\n\n                CREATE INDEX IF NOT EXISTS %(name)s_by_path ON %(name)s (\n                    path\n                );\n                CREATE INDEX IF NOT EXISTS %(name)s_by_hash ON %(name)s (\n                    hash\n                );\n                CREATE INDEX IF NOT EXISTS %(name)s_by_size ON %(name)s (\n                    size\n                );\n                CREATE INDEX IF NOT EXISTS %(name)s_by_hash_size ON %(name)s (\n                    hash,\n                    size\n                );\n                CREATE INDEX IF NOT EXISTS %(name)s_by_size_time ON %(name)s (\n                    size,\n                    time\n                );\n                CREATE INDEX IF NOT EXISTS %(name)s_by_hash_size_time ON %(name)s (\n                    hash,\n                    size,\n                    time\n                );\n                CREATE INDEX IF NOT EXISTS %(name)s_by_mark ON %(name)s (\n                    mark\n                );\n            ' % {'temporary': temporary, 'primary': primary, 'name': name})

    def _dbalias(self, i):
        return 'remotedb%02d' % i

    def _create_combined(self, conn):
        self._create_basic_schema(conn, 'combinedtab', True)
        selects = []
        argmap = {}
        selects.append('\n            SELECT\n                path,\n                hash,\n                size,\n                time,\n                mark\n            FROM\n                hashtab\n        ')
        for (i, combine) in enumerate(self._combines):
            local = combine.local
            if local != None:
                local = os.path.abspath(local)
            else:
                local = '/'
            remote = combine.remote
            if remote == None:
                remote = '/'
            if local == '/' and remote == '/':
                selects.append('\n                    SELECT\n                        path,\n                        hash,\n                        size,\n                        time,\n                        0 as mark\n                    FROM\n                        %s.hashtab\n                ' % self._dbalias(i))
            else:
                selects.append("\n                    SELECT\n                        :%(name)s_local || substr(path, :%(name)s_remote_len) as path,\n                        hash,\n                        size,\n                        time,\n                        0 as mark\n                    FROM\n                        %(name)s.hashtab\n                    WHERE\n                        (path = :%(name)s_remote) OR\n                        (substr(path, 1, :%(name)s_remote_len + 1) = :%(name)s_remote || '/')\n                " % {'name': self._dbalias(i)})
                argmap.update({'%s_local' % self._dbalias(i): local, 
                   '%s_remote' % self._dbalias(i): remote, 
                   '%s_remote_len' % self._dbalias(i): len(remote)})

        statement = '\n            INSERT OR IGNORE INTO combinedtab\n        ' + ('\n            UNION\n        ').join(selects) + '\n            ORDER BY\n                path,\n                mark DESC\n        '
        with conn:
            conn.execute(statement, argmap)
        return

    def _create_working(self, conn):
        with conn:
            conn.executescript('\n                CREATE TEMPORARY TABLE IF NOT EXISTS dirtab (\n                    path TEXT PRIMARY KEY\n                );\n            ')

    def _create_schema(self, conn):
        self._create_basic_schema(conn, 'hashtab', False)
        with conn:
            conn.executescript('\n                CREATE TABLE IF NOT EXISTS marktab (\n                    mark INTEGER PRIMARY KEY AUTOINCREMENT,\n                    time LONG\n                );\n            ')

    @property
    def mark(self):
        if self._mark == None:
            with self._conn:
                self._mark = self._conn.execute("INSERT INTO marktab (time) VALUES (strftime('%s','now'))").lastrowid
        return self._mark

    def _ismatch(self, row, stat):
        return row['time'] == stat.st_mtime and row['size'] == stat.st_size

    def path_mark(self, path):
        with self._conn as (conn):
            conn.execute('UPDATE hashtab SET mark=? WHERE path=?', (self.mark, path))

    def path_update(self, path, stat, hash):
        self.path_update_direct(path, stat.st_size, stat.st_mtime, hash)

    def path_update_direct(self, path, size, time, hash):
        with self._conn as (conn):
            conn.execute('UPDATE hashtab SET hash=?, size=?, time=?, mark=? WHERE path=?', (hash, size, time, self.mark, path))

    def path_dirdone(self, path):
        row = self._conn.execute('SELECT * FROM dirtab WHERE path=?', (path,)).fetchone()
        if not row:
            with self._conn as (conn):
                conn.execute('INSERT INTO dirtab (path) VALUES (?)', (path,))
            return False
        else:
            return True

    def path_hash(self, path, stat):
        row = self._conn.execute('SELECT * FROM hashtab WHERE path=?', (path,)).fetchone()
        if row:
            if row['mark'] == self.mark:
                return row['hash']
            if self._ismatch(row, stat):
                self.path_mark(path)
                return row['hash']
        for row in self._conn.execute('SELECT * FROM combinedtab WHERE path=?', (path,)):
            if self._ismatch(row, stat):
                self.path_update_direct(path=path, hash=row['hash'], size=row['size'], time=row['time'])
                return row['hash']

        return

    def path_discard_unmarked(self, path):
        pass

    def path_insert(self, path, stat, hash):
        with self._conn as (conn):
            conn.execute('INSERT OR REPLACE INTO hashtab (path, hash, size, time, mark) VALUES (?, ?, ?, ?, ?)', (path, hash, stat.st_size, stat.st_mtime, self.mark))

    def path_findall(self, path):
        for row in self._conn.execute('SELECT * FROM hashtab WHERE path=? UNION SELECT * FROM combinedtab WHERE path=? ORDER BY path, mark DESC', (path, path)):
            yield row

    def path_findroot(self, path):
        for row in self._conn.execute("\n                SELECT * FROM hashtab WHERE (path=:path) OR (substr(path,1,:path_len + 1) == :path || '/')\n                UNION\n                SELECT * FROM combinedtab WHERE (path=:path) OR (substr(path,1,:path_len + 1) == :path || '/')\n            ", {'path': path, 'path_len': len(path)}):
            yield row


if __name__ == '__main__':
    from hashdb_config_base import CombineDB
    dbB = HashDatabase('test/secondary.db')
    dbB.open()
    dbC = HashDatabase('test/ternary.db')
    dbC.open()
    dbA = HashDatabase('test/primary.db')
    dbA.add_combine(CombineDB('', 'test/secondary.db', ''))
    dbA.add_combine(CombineDB('', 'test/ternary.db', ''))
    dbA.open()
    for row in dbA._conn.execute('SELECT * FROM combinedtab'):
        print row