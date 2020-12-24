# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/dartui/sql.py
# Compiled at: 2012-03-17 14:27:54
import sqlite3

class Database:
    DEFAULT_VALUES = {'host': 'localhost', 
       'port': 80, 
       'path': '/RPC2', 
       'username': None, 
       'password': None, 
       'refresh_rate': 5, 
       'show_torrent_age': True, 
       'debug': False, 
       'show_welcome': True, 
       'du_path': '/'}
    DATA_TYPES = {'host': str, 
       'port': int, 
       'path': str, 
       'username': None, 
       'password': None, 
       'refresh_rate': int, 
       'show_torrent_age': bool, 
       'debug': bool, 
       'show_welcome': bool, 
       'du_path': str}

    def __init__(self, db_path):
        self.db_path = db_path
        self.settings_table = 'settings'
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()
        self.get_tables()
        if 'settings' not in self.tables:
            self.create_tables()
        self.get_settings()

    def get_tables(self):
        data = self.query("SELECT name FROM sqlite_master WHERE type='table'")
        if len(data) > 0:
            self.tables = data[0]
        else:
            self.tables = []
        return self.tables

    def create_tables(self):
        query = 'CREATE TABLE "settings" (\n        "key" text NOT NULL,\n        "value" text,\n        PRIMARY KEY("key")\n        );\n        \n        BEGIN;\n        COMMIT;\n        \n        CREATE UNIQUE INDEX "key" ON settings (key);\n        '
        self.c.executescript(query)
        self._insert_default_values()

    def get_settings(self):
        self.settings = {}
        for (key, value) in self.query('SELECT * FROM settings'):
            if Database.DATA_TYPES[key] == bool:
                if value == '0':
                    value = False
                elif value == '1':
                    value = True
            if Database.DATA_TYPES[key] == int:
                value = int(value)
            self.settings[key.encode()] = value

        return self.settings

    def _insert_default_values(self):
        self.settings = self.get_settings()
        for (key, value) in Database.DEFAULT_VALUES.items():
            if key not in self.settings.keys():
                query = ('INSERT INTO {0} VALUES (?, ?)').format(self.settings_table)
                self._execute(query, (key, value))

        self.settings = self.get_settings()
        self.conn.commit()

    def update_settings(self, **kwargs):
        new_settings = {}
        for key in Database.DATA_TYPES.keys():
            if key in kwargs:
                new_settings[key] = kwargs.get(key)

        new_settings['show_welcome'] = False
        query = ('UPDATE {0} SET value = ? WHERE key = ?').format(self.settings_table)
        self.c.executemany(query, zip(new_settings.values(), new_settings.keys()))
        self.conn.commit()
        self.get_settings()

    def _execute(self, query, values=()):
        self.c.execute(query, values)

    def query(self, query, values=()):
        self._execute(query, values)
        return self.c.fetchall()

    def close(self):
        self.conn.commit()
        self.conn.close()