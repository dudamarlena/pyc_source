# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qqqfome/db.py
# Compiled at: 2016-02-12 05:03:09
# Size of source mod 2**32: 5256 bytes
import os, sqlite3, json, logging, datetime
from zhihu import Author, ZhihuClient
from . import common as c
from . import strings as s
L = logging.getLogger('qqqufome-db')

def set_logger_level(level):
    global L
    c.check_type(level, 'level', logging.NOTSET)
    L.setLevel(level)


def set_logger_handle(handle):
    L.addHandler(handle)


def author_to_db_filename(author):
    c.check_type(author, 'author', Author)
    return author.id + '.sqlite3'


def create_db(author):
    c.check_type(author, 'author', Author)
    filename = author_to_db_filename(author)
    L.info(s.log_get_user_id.format(filename))
    if os.path.isfile(filename):
        e = FileExistsError()
        e.filename = filename
        raise e
    L.info(s.log_db_not_exist_create.format(filename))
    db = sqlite3.connect(author_to_db_filename(author))
    L.info(s.log_connected_to_db.format(filename))
    return db


def connect_db(database):
    c.check_type(database, 'database', str)
    if not os.path.isfile(database):
        e = FileNotFoundError()
        e.filename = database
        raise e
    return sqlite3.connect(database)


def create_table(db: sqlite3.Connection):
    c.check_type(db, 'db', sqlite3.Connection)
    L.info(s.log_create_table_in_db)
    with db:
        db.execute('\n           CREATE TABLE followers\n           (\n           id       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\n           name     TEXT            NOT NULL,\n           in_name  TEXT            NOT NULL\n           );\n           ')
        db.execute('\n           CREATE TABLE meta\n           (\n           id       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\n           name     TEXT            NOT NULL,\n           in_name  TEXT            NOT NULL,\n           cookies  TEXT            NOT NULL\n           );\n            ')
        db.execute('\n           CREATE TABLE log\n           (\n           id               INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\n           time             DATETIME        NOT NULL,\n           follower_number  INT             NOT NULL,\n           increase         INT             NOT NULL,\n           message          TEXT            NOT NULL\n           );\n            ')
    L.info(s.success)


def add_user_to_db(db, author):
    c.check_type(db, 'db', sqlite3.Connection)
    c.check_type(author, 'author', Author)
    with db:
        L.debug(s.log_add_user_to_db.format(author.name))
        db.execute('\n            INSERT INTO followers\n            (name, in_name) VALUES\n            ( ?,      ?   );\n            ', (
         author.name, author.id))


def dump_init_data_to_db(db, author):
    c.check_type(db, 'db', sqlite3.Connection)
    c.check_type(author, 'author', Author)
    with db:
        name = author.name
        in_name = author.id
        cookies = json.dumps(author._session.cookies.get_dict())
        db.execute('\n            INSERT INTO meta\n            (name,    in_name,   cookies) VALUES\n            (  ?,        ?,         ?   );\n            ', (
         name, in_name, cookies))
    L.info(s.log_start_get_followers.format(author.name))
    with db:
        for _, follower in zip(range(100), author.followers):
            add_user_to_db(db, follower)

    with db:
        log_to_db(db, author.follower_num, s.log_db_init)


def is_db_closed(db):
    c.check_type(db, 'db', sqlite3.Connection)
    try:
        with db:
            db.execute("\n                SELECT name from sqlite_master where type = 'table';\n                ")
        return False
    except sqlite3.ProgrammingError:
        return True


def close_db(db):
    c.check_type(db, 'db', sqlite3.Connection)
    if not is_db_closed(db):
        db.close()
        L.info(s.log_close_db)


def get_cookies(db):
    c.check_type(db, 'db', sqlite3.Connection)
    cursor = db.execute('SELECT cookies from meta')
    row = cursor.fetchone()
    if row is None:
        return
    return row[0]


def log_to_db(db, follower_num, message):
    c.check_type(db, 'db', sqlite3.Connection)
    c.check_type(follower_num, 'follower_num', int)
    c.check_type(message, 'message', str)
    cursor = db.execute('\n        SELECT follower_number FROM log ORDER BY id DESC;\n        ')
    row = cursor.fetchone()
    if row:
        increase = follower_num - row[0]
    else:
        increase = 0
    with db:
        db.execute('\n            INSERT INTO log\n            (time, follower_number, increase, message) VALUES\n            ( ?,           ?,           ?,       ?   );\n            ', (
         datetime.datetime.now(), follower_num, increase, message))


def is_in_db(db, in_name):
    c.check_type(db, 'db', sqlite3.Connection)
    c.check_type(in_name, 'in_name', str)
    with db:
        cursor = db.execute('\n            SELECT * FROM followers WHERE in_name = ?;\n            ', (
         in_name,))
        row = cursor.fetchone()
        return row is not None