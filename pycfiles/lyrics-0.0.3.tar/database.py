# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/david/source/lyrics/lyrics/database.py
# Compiled at: 2013-01-30 15:40:13
import sqlite3, threading, settings, debug

def load(artist, song, album):
    if settings.use_database:
        return _LyricsDb.load(artist, song, album)
    raise LookupError('settings.use_database = False')


def save(artist, song, album, lyrics):
    if settings.use_database:
        debug.debug('save')
        return _LyricsDb.save(artist, song, album, lyrics)


def _get_db_cursor():
    connection = sqlite3.connect(settings.database_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    return (
     connection, cursor)


_db_lock = threading.Lock()

def _sqlite_threadsafe(func):

    def wrapper(*args, **kwargs):
        _db_lock.acquire()
        try:
            result = func(*args, **kwargs)
        except:
            _db_lock.release()
            raise

        _db_lock.release()
        return result

    return wrapper


class _LyricsDb(object):
    _create_table = '\n    CREATE TABLE IF NOT EXISTS lyrics(\n        artist text not null,\n        song text not null,\n        album text not null,\n        lyrics text null,\n        unique(artist, song, album)\n    )\n    '
    _select = 'SELECT lyrics FROM lyrics WHERE artist=? and song=? and album=?'
    _insert = 'INSERT INTO lyrics VALUES (?, ?, ?, ?)'

    def get_cursor(self):
        """create new connections, sqlite cannot handle multi threading"""
        connection, cursor = _get_db_cursor()
        cursor.execute(self._create_table)
        return (connection, cursor)

    @_sqlite_threadsafe
    def save(self, *args):
        debug.debug('savex', args)
        connection, cursor = self.get_cursor()
        cursor.execute(self._insert, args)
        connection.commit()

    @_sqlite_threadsafe
    def load(self, *args):
        connection, cursor = self.get_cursor()
        cursor.execute(self._select, args)
        row = cursor.fetchone()
        if row is None:
            raise LookupError('Row not found')
        return row[0]


class ID3Cache(object):
    _create_table = '\n    CREATE TABLE IF NOT EXISTS id3_cache(\n        path text primary key,\n        artist text not null,\n        song text not null,\n        album text not null,\n        genre text not null,\n        year text not null,\n        track text not null\n    )\n    '
    _select = 'SELECT * FROM id3_cache WHERE path=?'
    _insert = 'INSERT INTO id3_cache VALUES (\n                    :path, :artist, :song, :album, :genre, :year, :track)'

    def get_cursor(self):
        """create new connections, sqlite cannot handle multi threading"""
        connection, cursor = _get_db_cursor()
        (connection, cursor.execute(self._create_table))
        return (connection, cursor)

    @_sqlite_threadsafe
    def save(self, dct):
        connection, cursor = self.get_cursor()
        debug.debug('save id3 db song', dct)
        cursor.execute(self._insert, dct)
        connection.commit()

    @_sqlite_threadsafe
    def load(self, path):
        connection, cursor = self.get_cursor()
        cursor.execute(self._select, (path,))
        row = cursor.fetchone()
        if row is None:
            return
        else:
            row = dict(zip(row.keys(), row))
            return row


_LyricsDb = _LyricsDb()
ID3Cache = ID3Cache()