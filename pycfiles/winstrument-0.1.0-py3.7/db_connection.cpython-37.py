# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winstrument\db_connection.py
# Compiled at: 2020-02-05 20:03:04
# Size of source mod 2**32: 2689 bytes
import sqlite3
from winstrument.data.module_message import ModuleMessage
import sys
from datetime import datetime
import json, os, toml

class DBConnection:

    def __init__(self, dbpath):
        self._db = sqlite3.connect(dbpath, check_same_thread=False)
        self._dbpath = dbpath
        self._cursor = self._db.cursor()
        self._cursor.execute('CREATE TABLE IF NOT EXISTS output\n                            (id INTEGER PRIMARY KEY,\n                            modname TEXT NOT NULL,\n                            time TEXT NOT NULL,\n                            target TEXT NOT NULL,\n                            message BLOB)')
        self._db.commit()

    def write_message(self, message):
        """
        Insert the given message into the sqlite DB output table
        message - ModuleMessage object
        """
        self._cursor.execute('INSERT INTO "output" (modname, time, target, message) VALUES (?,?,?,?)', (message.module, message.time, message.target, json.dumps(message.data)))
        self._db.commit()

    def clear_output(self):
        """
        Truncates the output table
        """
        self._cursor.execute('DELETE FROM "output"')
        self._db.commit()

    def read_messages(self, modname):
        """
        Get a list of all messages for the given module name
        modname: str - Name of the module for which to retrieve messages
        Return: list of ModuleMessage objects
        """
        self._cursor.execute('SELECT "modname", "time", "target", "message" FROM "output" where modname= ? ', (modname,))
        messages = []
        for row in self._cursor.fetchall():
            module = row[0]
            time = row[1]
            target = row[2]
            data = json.loads(row[3])
            messages.append(ModuleMessage(module, target, data, time=time))

        return messages

    def close(self):
        self._db.close()
        os.remove(self._dbpath)