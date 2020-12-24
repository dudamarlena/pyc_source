# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/021_long_call.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Integer, MetaData, String, Table
from sqlalchemy import Table, Text

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    try:
        long_calls = Table('long_calls', meta, autoload=True)
        long_calls.drop()
    except Exception:
        pass


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine