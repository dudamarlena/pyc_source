# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\soccer\data_connectors\sqlite_connector.py
# Compiled at: 2017-09-06 14:29:24
# Size of source mod 2**32: 586 bytes
"""
SQLite Connector for soccer data. This connector
expects the european soccer dataset that can be found here:
https://www.kaggle.com/hugomathien/soccer
"""
import sqlite3
from .data_connector import DataConnector

class SQLiteConnector(DataConnector):
    __doc__ = '\n    SQLite Connector for soccer data. This connector\n    expects the european soccer dataset that can be found here:\n    https://www.kaggle.com/hugomathien/soccer\n    '

    def __init__(self, db_path):
        DataConnector.__init__(self)
        print('x')
        self.db = sqlite3.connect(db_path)