# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/will/.virtualenvs/datasight-backend/lib/python2.7/site-packages/dejavu/database_sql.py
# Compiled at: 2015-04-19 17:14:05
from __future__ import absolute_import
from itertools import izip_longest
import Queue, MySQLdb as mysql
from MySQLdb.cursors import DictCursor
from dejavu.database import Database

class SQLDatabase(Database):
    """
    Queries:

    1) Find duplicates (shouldn't be any, though):

        select `hash`, `song_id`, `offset`, count(*) cnt
        from fingerprints
        group by `hash`, `song_id`, `offset`
        having cnt > 1
        order by cnt asc;

    2) Get number of hashes by song:

        select song_id, song_name, count(song_id) as num
        from fingerprints
        natural join songs
        group by song_id
        order by count(song_id) desc;

    3) get hashes with highest number of collisions

        select
            hash,
            count(distinct song_id) as n
        from fingerprints
        group by `hash`
        order by n DESC;

    => 26 different songs with same fingerprint (392 times):

        select songs.song_name, fingerprints.offset
        from fingerprints natural join songs
        where fingerprints.hash = "08d3c833b71c60a7b620322ac0c0aba7bf5a3e73";
    """
    type = 'mysql'
    FINGERPRINTS_TABLENAME = 'fingerprints'
    SONGS_TABLENAME = 'songs'
    FIELD_FINGERPRINTED = 'fingerprinted'
    CREATE_FINGERPRINTS_TABLE = '\n        CREATE TABLE IF NOT EXISTS `%s` (\n             `%s` binary(10) not null,\n             `%s` mediumint unsigned not null,\n             `%s` int unsigned not null,\n         INDEX (%s),\n         UNIQUE KEY `unique_constraint` (%s, %s, %s),\n         FOREIGN KEY (%s) REFERENCES %s(%s) ON DELETE CASCADE\n    ) ENGINE=INNODB;' % (
     FINGERPRINTS_TABLENAME, Database.FIELD_HASH,
     Database.FIELD_SONG_ID, Database.FIELD_OFFSET, Database.FIELD_HASH,
     Database.FIELD_SONG_ID, Database.FIELD_OFFSET, Database.FIELD_HASH,
     Database.FIELD_SONG_ID, SONGS_TABLENAME, Database.FIELD_SONG_ID)
    CREATE_SONGS_TABLE = '\n        CREATE TABLE IF NOT EXISTS `%s` (\n            `%s` mediumint unsigned not null auto_increment,\n            `%s` varchar(250) not null,\n            `%s` tinyint default 0,\n            `%s` binary(20) not null,\n        PRIMARY KEY (`%s`),\n        UNIQUE KEY `%s` (`%s`)\n    ) ENGINE=INNODB;' % (
     SONGS_TABLENAME, Database.FIELD_SONG_ID, Database.FIELD_SONGNAME, FIELD_FINGERPRINTED,
     Database.FIELD_FILE_SHA1,
     Database.FIELD_SONG_ID, Database.FIELD_SONG_ID, Database.FIELD_SONG_ID)
    INSERT_FINGERPRINT = '\n        INSERT IGNORE INTO %s (%s, %s, %s) values\n            (UNHEX(%%s), %%s, %%s);\n    ' % (FINGERPRINTS_TABLENAME, Database.FIELD_HASH, Database.FIELD_SONG_ID, Database.FIELD_OFFSET)
    INSERT_SONG = 'INSERT INTO %s (%s, %s) values (%%s, UNHEX(%%s));' % (
     SONGS_TABLENAME, Database.FIELD_SONGNAME, Database.FIELD_FILE_SHA1)
    SELECT = '\n        SELECT %s, %s FROM %s WHERE %s = UNHEX(%%s);\n    ' % (Database.FIELD_SONG_ID, Database.FIELD_OFFSET, FINGERPRINTS_TABLENAME, Database.FIELD_HASH)
    SELECT_MULTIPLE = '\n        SELECT HEX(%s), %s, %s FROM %s WHERE %s IN (%%s);\n    ' % (Database.FIELD_HASH, Database.FIELD_SONG_ID, Database.FIELD_OFFSET,
     FINGERPRINTS_TABLENAME, Database.FIELD_HASH)
    SELECT_ALL = '\n        SELECT %s, %s FROM %s;\n    ' % (Database.FIELD_SONG_ID, Database.FIELD_OFFSET, FINGERPRINTS_TABLENAME)
    SELECT_SONG = '\n        SELECT %s, HEX(%s) as %s FROM %s WHERE %s = %%s;\n    ' % (Database.FIELD_SONGNAME, Database.FIELD_FILE_SHA1, Database.FIELD_FILE_SHA1, SONGS_TABLENAME, Database.FIELD_SONG_ID)
    SELECT_NUM_FINGERPRINTS = '\n        SELECT COUNT(*) as n FROM %s\n    ' % FINGERPRINTS_TABLENAME
    SELECT_UNIQUE_SONG_IDS = '\n        SELECT COUNT(DISTINCT %s) as n FROM %s WHERE %s = 1;\n    ' % (Database.FIELD_SONG_ID, SONGS_TABLENAME, FIELD_FINGERPRINTED)
    SELECT_SONGS = '\n        SELECT %s, %s, HEX(%s) as %s FROM %s WHERE %s = 1;\n    ' % (Database.FIELD_SONG_ID, Database.FIELD_SONGNAME, Database.FIELD_FILE_SHA1, Database.FIELD_FILE_SHA1,
     SONGS_TABLENAME, FIELD_FINGERPRINTED)
    DROP_FINGERPRINTS = 'DROP TABLE IF EXISTS %s;' % FINGERPRINTS_TABLENAME
    DROP_SONGS = 'DROP TABLE IF EXISTS %s;' % SONGS_TABLENAME
    UPDATE_SONG_FINGERPRINTED = '\n        UPDATE %s SET %s = 1 WHERE %s = %%s\n    ' % (SONGS_TABLENAME, FIELD_FINGERPRINTED, Database.FIELD_SONG_ID)
    DELETE_UNFINGERPRINTED = '\n        DELETE FROM %s WHERE %s = 0;\n    ' % (SONGS_TABLENAME, FIELD_FINGERPRINTED)

    def __init__(self, **options):
        super(SQLDatabase, self).__init__()
        self.cursor = cursor_factory(**options)
        self._options = options

    def after_fork(self):
        Cursor.clear_cache()

    def setup(self):
        """
        Creates any non-existing tables required for dejavu to function.

        This also removes all songs that have been added but have no
        fingerprints associated with them.
        """
        with self.cursor() as (cur):
            cur.execute(self.CREATE_SONGS_TABLE)
            cur.execute(self.CREATE_FINGERPRINTS_TABLE)
            cur.execute(self.DELETE_UNFINGERPRINTED)

    def empty(self):
        """
        Drops tables created by dejavu and then creates them again
        by calling `SQLDatabase.setup`.

        .. warning:
            This will result in a loss of data
        """
        with self.cursor() as (cur):
            cur.execute(self.DROP_FINGERPRINTS)
            cur.execute(self.DROP_SONGS)
        self.setup()

    def delete_unfingerprinted_songs(self):
        """
        Removes all songs that have no fingerprints associated with them.
        """
        with self.cursor() as (cur):
            cur.execute(self.DELETE_UNFINGERPRINTED)

    def get_num_songs(self):
        """
        Returns number of songs the database has fingerprinted.
        """
        with self.cursor() as (cur):
            cur.execute(self.SELECT_UNIQUE_SONG_IDS)
            for count, in cur:
                return count

            return 0

    def get_num_fingerprints(self):
        """
        Returns number of fingerprints the database has fingerprinted.
        """
        with self.cursor() as (cur):
            cur.execute(self.SELECT_NUM_FINGERPRINTS)
            for count, in cur:
                return count

            return 0

    def set_song_fingerprinted(self, sid):
        """
        Set the fingerprinted flag to TRUE (1) once a song has been completely
        fingerprinted in the database.
        """
        with self.cursor() as (cur):
            cur.execute(self.UPDATE_SONG_FINGERPRINTED, (sid,))

    def get_songs(self):
        """
        Return songs that have the fingerprinted flag set TRUE (1).
        """
        with self.cursor(cursor_type=DictCursor) as (cur):
            cur.execute(self.SELECT_SONGS)
            for row in cur:
                yield row

    def get_song_by_id(self, sid):
        """
        Returns song by its ID.
        """
        with self.cursor(cursor_type=DictCursor) as (cur):
            cur.execute(self.SELECT_SONG, (sid,))
            return cur.fetchone()

    def insert(self, hash, sid, offset):
        """
        Insert a (sha1, song_id, offset) row into database.
        """
        with self.cursor() as (cur):
            cur.execute(self.INSERT_FINGERPRINT, (hash, sid, offset))

    def insert_song(self, songname, file_hash):
        """
        Inserts song in the database and returns the ID of the inserted record.
        """
        with self.cursor() as (cur):
            cur.execute(self.INSERT_SONG, (songname, file_hash))
            return cur.lastrowid

    def query(self, hash):
        """
        Return all tuples associated with hash.

        If hash is None, returns all entries in the
        database (be careful with that one!).
        """
        query = self.SELECT_ALL if hash is None else self.SELECT
        with self.cursor() as (cur):
            cur.execute(query)
            for sid, offset in cur:
                yield (
                 sid, offset)

        return

    def get_iterable_kv_pairs(self):
        """
        Returns all tuples in database.
        """
        return self.query(None)

    def insert_hashes(self, sid, hashes):
        """
        Insert series of hash => song_id, offset
        values into the database.
        """
        values = []
        for hash, offset in hashes:
            values.append((hash, sid, offset))

        with self.cursor() as (cur):
            for split_values in grouper(values, 1000):
                cur.executemany(self.INSERT_FINGERPRINT, split_values)

    def return_matches(self, hashes):
        """
        Return the (song_id, offset_diff) tuples associated with
        a list of (sha1, sample_offset) values.
        """
        mapper = {}
        for hash, offset in hashes:
            mapper[hash.upper()] = offset

        values = mapper.keys()
        with self.cursor() as (cur):
            for split_values in grouper(values, 1000):
                query = self.SELECT_MULTIPLE
                query = query % (', ').join(['UNHEX(%s)'] * len(split_values))
                cur.execute(query, split_values)
                for hash, sid, offset in cur:
                    yield (
                     sid, offset - mapper[hash])

    def __getstate__(self):
        return (
         self._options,)

    def __setstate__(self, state):
        self._options, = state
        self.cursor = cursor_factory(**self._options)


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return (filter(None, values) for values in izip_longest(fillvalue=fillvalue, *args))


def cursor_factory(**factory_options):

    def cursor(**options):
        options.update(factory_options)
        return Cursor(**options)

    return cursor


class Cursor(object):
    """
    Establishes a connection to the database and returns an open cursor.

    ```python
    # Use as context manager
    with Cursor() as cur:
        cur.execute(query)
    ```
    """
    _cache = Queue.Queue(maxsize=5)

    def __init__(self, cursor_type=mysql.cursors.Cursor, **options):
        super(Cursor, self).__init__()
        try:
            conn = self._cache.get_nowait()
        except Queue.Empty:
            conn = mysql.connect(**options)
        else:
            conn.ping(True)

        self.conn = conn
        self.conn.autocommit(False)
        self.cursor_type = cursor_type

    @classmethod
    def clear_cache(cls):
        cls._cache = Queue.Queue(maxsize=5)

    def __enter__(self):
        self.cursor = self.conn.cursor(self.cursor_type)
        return self.cursor

    def __exit__(self, extype, exvalue, traceback):
        if extype is mysql.MySQLError:
            self.cursor.rollback()
        self.cursor.close()
        self.conn.commit()
        try:
            self._cache.put_nowait(self.conn)
        except Queue.Full:
            self.conn.close()