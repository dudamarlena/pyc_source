# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ealesid\PycharmProjects\geekbrains_python\jimmer\jimmer\server\store.py
# Compiled at: 2017-11-22 11:36:48
# Size of source mod 2**32: 917 bytes
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os.path import isfile, getsize
SQLITE_HEADER_SIZE = 100
SQLITE_HEADER_STRING_LENGTH = 16
SQLITE_HEADER_DESCRIPTION = b'SQLite format 3\x00'

def is_sqlite_db(filename):
    if not isfile(filename) or getsize(filename) < SQLITE_HEADER_SIZE:
        return False
    with open(filename, 'rb') as (db_file):
        header = db_file.read(SQLITE_HEADER_SIZE)
    return header[:SQLITE_HEADER_STRING_LENGTH] == SQLITE_HEADER_DESCRIPTION


class Store:

    def __init__(self, db):
        self.engine = create_engine('sqlite:///' + db)

    def __enter__(self):
        self.session = sessionmaker(bind=self.engine)()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect_db()

    def disconnect_db(self):
        self.session.commit()
        self.session.close()