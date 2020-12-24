# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/plugins/persistence.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 2397 bytes
import asyncio, sqlite3, pickle

class SQLitePlugin:

    def __init__(self, context):
        self.context = context
        self.conn = None
        self.cursor = None
        self.db_file = None
        try:
            self.persistence_config = self.context.config['persistence']
            self.init_db()
        except KeyError:
            self.context.logger.warning("'persistence' section not found in context configuration")

    def init_db(self):
        self.db_file = self.persistence_config.get('file', None)
        if not self.db_file:
            self.context.logger.warning("'file' persistence parameter not found")
        else:
            try:
                self.conn = sqlite3.connect(self.db_file)
                self.cursor = self.conn.cursor()
                self.context.logger.info("Database file '%s' opened" % self.db_file)
            except Exception as e:
                try:
                    self.context.logger.error("Error while initializing database '%s' : %s" % (self.db_file, e))
                finally:
                    e = None
                    del e

            else:
                if self.cursor:
                    self.cursor.execute('CREATE TABLE IF NOT EXISTS session(client_id TEXT PRIMARY KEY, data BLOB)')

    @asyncio.coroutine
    def save_session(self, session):
        if self.cursor:
            dump = pickle.dumps(session)
            try:
                self.cursor.execute('INSERT OR REPLACE INTO session (client_id, data) VALUES (?,?)', (session.client_id, dump))
                self.conn.commit()
            except Exception as e:
                try:
                    self.context.logger.error("Failed saving session '%s': %s" % (session, e))
                finally:
                    e = None
                    del e

    @asyncio.coroutine
    def find_session(self, client_id):
        if self.cursor:
            row = self.cursor.execute('SELECT data FROM session where client_id=?', (client_id,)).fetchone()
            if row:
                return pickle.loads(row[0])
            return

    @asyncio.coroutine
    def del_session(self, client_id):
        if self.cursor:
            self.cursor.execute('DELETE FROM session where client_id=?', (client_id,))
            self.conn.commit()

    @asyncio.coroutine
    def on_broker_post_shutdown(self):
        if self.conn:
            self.conn.close()
            self.context.logger.info("Database file '%s' closed" % self.db_file)