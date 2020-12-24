# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\miniworldmaker\tools\db_manager.py
# Compiled at: 2019-05-18 01:27:11
# Size of source mod 2**32: 1356 bytes
import logging, sqlite3

class DBManager:
    log = logging.getLogger('db_manager')

    def __init__(self, file):
        self.file = file
        try:
            self.connection = sqlite3.connect(self.file)
            self.cursor = self.connection.cursor()
        except:
            raise

    def insert(self, table: str, row: dict) -> bool:
        try:
            cols = ', '.join(('{}'.format(col) for col in row.keys()))
            vals = ''
            for col in row.values():
                if isinstance(col, str):
                    col = "'" + col + "'"
                vals = vals + str(col) + ','

            vals = vals[:-1]
            sql = 'INSERT INTO ' + table + '( ' + str(cols) + ') VALUES (' + str(vals) + ')'
            logging.info(sql)
            self.connection.execute(sql)
            return True
        except:
            self.close_connection()
            raise

    def close_connection(self):
        self.connection.close()

    def select_single_row(self, statement: str):
        self.cursor.execute(statement)
        return self.cursor.fetchone()

    def select_all_rows(self, statement: str):
        self.cursor.execute(statement)
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()