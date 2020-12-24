# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/migrate_repo/versions/015_monitor.py
# Compiled at: 2016-06-13 14:11:03
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Integer, MetaData, String, Table

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    monitors = Table('monitors', meta, Column('id', Integer, primary_key=True, nullable=False), Column('name', String(length=255), nullable=False), Column('address', String(length=255)), Column('health', String(length=255)), Column('details', String(length=255)), Column('skew', String(length=255)), Column('latency', String(length=255)), Column('kb_total', Integer), Column('kb_used', Integer), Column('kb_avail', Integer), Column('avail_percent', Integer), Column('created_at', DateTime(timezone=False)), Column('updated_at', DateTime(timezone=False)), Column('deleted_at', DateTime(timezone=False)), Column('deleted', Boolean(create_constraint=True, name=None)))
    try:
        monitors.create()
    except Exception:
        meta.drop_all(tables=[monitors])
        raise

    return


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    monitors = Table('monitors', meta, autoload=True)
    monitors.drop()