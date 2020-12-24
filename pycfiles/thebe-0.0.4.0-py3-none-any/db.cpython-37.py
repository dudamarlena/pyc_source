# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hairy/inlinepython/python_live/db.py
# Compiled at: 2019-10-23 02:36:51
# Size of source mod 2**32: 982 bytes
from pony.orm import *
from pony.options import CUT_TRACEBACK
CUT_TRACEBACK = False
set_sql_debug(True)
db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

class Ledger(db.Entity):
    datetime = Required(str)
    cells = Set('Cell')


class Cell(db.Entity):
    location = Required(int)
    code = Required(str)
    hashId = Required(str)
    datetime = Required(str)
    changed = Required(bool)
    owner = Required(Ledger)


def create():
    db.generate_mapping(create_tables=True)


def drop_all():
    db.drop_all_tables(with_all_data=True)


@db_session
def add_cell(location, code, hashId, datetime, changed):
    Cell(location=location, code=code, hashId=hashId, datetime=datetime, changed=changed)


@db_session
def get_ledger():
    return select((c for c in Cell))[:]


@db_session
def drop_and_reinitialize():
    drop_all_tables(with_all_data=True)
    bind(provider='sqlite', filename='database.sqlite', create_db=True)
    generate_mapping(create_tables=True)