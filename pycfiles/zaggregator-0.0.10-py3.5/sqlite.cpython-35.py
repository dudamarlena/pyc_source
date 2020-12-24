# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zaggregator/sqlite.py
# Compiled at: 2018-08-01 11:48:18
# Size of source mod 2**32: 2019 bytes
import sqlite3
DBPATH = '/var/run/zaggregator/zaggregator.sqlite'
db = None

def __init__(dbpath=DBPATH) -> None:
    """ Initalize sqlite dataabase """
    global db
    db = sqlite3.connect(dbpath)
    create_table_str = '\n        CREATE TABLE\n        IF NOT EXISTS\n        samples (\n            ts DATETIME DEFAULT CURRENT_TIMESTAMP,\n            name TEXT,\n            rss INT,\n            vms INT,\n            ctxvol INT,\n            ctxinvol INT,\n            pcpu REAL\n        );\n        '
    create_trigger = '\n        CREATE TRIGGER IF NOT EXISTS\n        DELETE_TAIL\n        AFTER INSERT ON samples\n        BEGIN\n            DELETE FROM samples WHERE ts not in (select ts from samples order by ts desc\n            limit 300);\n        END;\n    '
    db.execute(create_table_str)
    db.execute(create_trigger)


class BadRecord(Exception):
    pass


def add_record(record) -> None:
    """
        Add record into sqlite database
    """
    if len(record) != 3 and hasattr(record, '__iter__'):
        query = "\n            INSERT INTO samples\n            ( name, rss, vms, ctxvol, ctxinvol, pcpu )\n            VALUES ('{}',{});".format(record[0], ','.join(map(str, record[1:])))
        db.execute(query)
        db.commit()
    else:
        raise BadRecord


def get_bundle_names() -> [str]:
    """
        Get list of bundle names from sqlite database
    """
    query = '\n        SELECT DISTINCT(name) FROM samples;\n        '
    return [row[0] for row in db.execute(query)]


def get(bname: str, check: str):
    """
        Get value of `check' variable for bundle with name `bname'
    """
    query = "\n        SELECT {} FROM samples\n        WHERE name='{}' AND\n            ( (julianday('now') - julianday(ts))*24*60*60 < 30 )\n        ORDER BY ts DESC\n        LIMIT 1;\n        ".format(check, bname)
    result = list(db.execute(query))
    if len(result) > 0:
        return result[0][0]


try:
    __init__(dbpath=DBPATH)
except sqlite3.OperationalError as e:
    pass