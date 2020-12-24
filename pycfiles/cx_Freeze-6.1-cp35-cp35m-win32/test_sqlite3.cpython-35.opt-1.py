# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\samples\sqlite\test_sqlite3.py
# Compiled at: 2020-01-04 18:05:46
# Size of source mod 2**32: 590 bytes
import sqlite3
con = sqlite3.connect(':memory:')
cur = con.cursor()
cur.executescript("\n    create table person(\n        firstname,\n        lastname,\n        age\n    );\n\n    create table book(\n        title,\n        author,\n        published\n    );\n\n    insert into book(title, author, published)\n    values (\n        'Dirk Gently''s Holistic Detective Agency',\n        'Douglas Adams',\n        1987\n    );\n    ")
with open('dump.sql', 'w') as (f):
    for line in con.iterdump():
        f.write('%s\n' % line)

print('dump.sql created')
con.close()