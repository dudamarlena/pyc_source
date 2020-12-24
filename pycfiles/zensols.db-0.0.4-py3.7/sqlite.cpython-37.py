# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/db/sqlite.py
# Compiled at: 2019-09-28 20:01:03
# Size of source mod 2**32: 2575 bytes
"""Convenience wrapper for the Python DB-API library, and some specificly for
the SQLite library.

"""
__author__ = 'Paul Landes'
import logging
from pathlib import Path
import sqlite3
from zensols.db import DbPersister, ConnectionManager, ConnectionManagerConfigurer, DbPersisterFactory
logger = logging.getLogger(__name__)

class SqliteConnectionManager(ConnectionManager):
    __doc__ = 'An SQLite connection factory.\n\n    '

    def __init__(self, db_file, persister, create_db=True):
        """Initialize.

        :param db_file: the SQLite database file to read or create
        :param persister: the persister that will use this connection factory
                          (needed to get the initialization DDL SQL)

        """
        super(SqliteConnectionManager, self).__init__()
        self.db_file = db_file
        self.persister = persister
        self.create_db = create_db

    def create(self):
        db_file = self.db_file
        logger.debug(f"creating connection to {db_file}")
        created = False
        if not db_file.exists():
            if not self.create_db:
                raise ValueError(f"database file {db_file} does not exist")
            if not db_file.parent.exists():
                logger.info(f"creating sql db directory {db_file.parent}")
                db_file.parent.mkdir(parents=True)
            logger.info(f"creating sqlite db file: {db_file}")
            created = True
        types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        conn = sqlite3.connect((str(db_file.absolute())), detect_types=types)
        if created:
            logger.info('initializing database...')
            for sql in self.persister.parser.get_init_db_sqls():
                logger.debug(f"invoking sql: {sql}")
                conn.execute(sql)
                conn.commit()

        return conn

    def drop(self):
        """Delete the SQLite database file from the file system.

        """
        logger.info(f"deleting: {self.db_file}")
        if self.db_file.exists():
            self.db_file.unlink()
            return True
        return False


class SqliteConnectionManagerConfigurer(ConnectionManagerConfigurer):

    def configure(self, params):
        params['sql_file'] = Path(params['sql_file'])
        params['conn_manager'] = SqliteConnectionManager(Path(params['db_file']), None)
        del params['db_file']


DbPersisterFactory.register_connection_manager_configurer(SqliteConnectionManagerConfigurer, 'sqlite')